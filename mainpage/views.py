from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import Questions
from openai import OpenAI
import random
import pyttsx3

# Create your views here.
def custominterviewpage(request):
    random_question = get_random_question()
    if request.method == 'POST':
        skills = request.POST['skills']
        if skills != '':
            print(skills)
            question = get_question_by_skill(skills)
            print(get_question_by_skill(skills))
            if question != None:
                return render(request, "custominterview.html", {'random_question': question})
        else:
            input = request.POST['q']
            analysis = analyseInterviewAns("Tell me about a time you communicated",input,"I communicated when i was at work")
            analysis_content = analysis.choices[0].message.content
            return render(request, 'custominterview.html', {'analysis_content': analysis_content})
    return render(request, "custominterview.html", {'random_question': random_question})

def homepage(request):
    random_question = get_random_question()
    if request.method == 'POST':    
        input = request.POST['q']
        analysis = analyseInterviewAns("Tell me about a time you communicated",input,"I communicated when i was at work")
        analysis_content = analysis.choices[0].message.content
        text_to_speech(analysis_content)
        #return HttpResponse(f'The text submitted is: {analysis_content}')
        return render(request, 'mainpage.html', {'analysis_content': analysis_content})
    return render(request, "mainpage.html", {'random_question': random_question})

def analyseInterviewAns(question, answer, modelAns):
    api_key = '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' #hidden for security reasons
    client = OpenAI(api_key=api_key)

    prompt = f"""Compare the user's answer to this model answer: {modelAns}.
            Highlight the pros and cons to the user's answer if any.
            Highlight if the user has used the STAR method.
            Highlight if they have used these skills: Communication"""  

    # Use the GPT-4 model to analyze the answer
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Analysing the interview question answer."
            },
            {
                "role": "user",
                "content": f"Question: {question}\nAnswer: {answer}"
            },
            {
                "role": "assistant",
                "content" : prompt
            }
        ],
        temperature=0.7,
        max_tokens=150,
        top_p=1
    )

    #return response.choices[0].message['content']
    return response

def text_to_speech(text):
    """
    Reads out a given string aloud.

    Parameters:
    - text (str): The string to be read aloud.
    """
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties of the speech engine (optional)
    # You can set properties such as speaking rate, volume, voice, etc.
    # For example:
    # engine.setProperty('rate', 150)  # Speed of speech
    # engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

    # Speak the provided text
    engine.say(text)

    # Wait for the speech to finish
    engine.runAndWait()

def get_random_question():
    # Get the count of questions in the database
    count = Questions.objects.count()

    # If there are questions in the database
    if count > 0:
        # Get a random question using offset and limit
        random_offset = random.randint(0, count - 1)
        random_question = Questions.objects.all()[random_offset]
    else:
        random_question = "Cannot display question"
    
    return random_question

def get_question_by_skill(skill):
    # Get all questions with the specified skill
    questions_with_skill = Questions.objects.filter(skill=skill)

    # If there are questions with the specified skill
    if questions_with_skill.exists():
        # Get a random question from the filtered set
        random_question = random.choice(questions_with_skill)
    else:
        random_question = None
    return random_question