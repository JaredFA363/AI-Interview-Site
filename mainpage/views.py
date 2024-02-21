from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Questions, Feedback
from openai import OpenAI
import random
import pyttsx3

# Create your views here.
def custominterviewpage(request):
    username = request.session.get('username')
    random_question = get_random_question()
    if request.method == 'POST':
        if 'skills' in request.POST:
            skills = request.POST['skills']
            if skills != '':
                print(skills)
                question = get_question_by_skill(skills)
                random_question = question
                print(get_question_by_skill(skills))
                if question != None:
                    return render(request, "custominterview.html", {'random_question': question, 'username': username})
            else:
                input = request.POST['q']
                analysis = analyseInterviewAns("Tell me about a time you communicated",input,"I communicated when i was at work")
                analysis_content = analysis.choices[0].message.content
                return render(request, 'custominterview.html', {'analysis_content': analysis_content, 'username': username})
        
        if 'save_feedback' in request.POST:
            feedback_text = request.POST.get('response', '')
            save_feedback(random_question,feedback_text,username)
            messages.success(request,"Feedback saved successfully")
    return render(request, "custominterview.html", {'random_question': random_question, 'username': username})

def homepage(request):
    username = request.session.get('username')
    random_question = get_random_question()
    if request.method == 'POST':
        if 'save_feedback' in request.POST:
            feedback_text = request.POST.get('response', '')
            save_feedback(random_question,feedback_text,username)
            messages.success(request,"Feedback saved successfully")
        else:   
            input = request.POST['q']
            analysis = analyseInterviewAns("Tell me about a time you communicated",input,"I communicated when i was at work")
            analysis_content = analysis.choices[0].message.content
            #text_to_speech(analysis_content)
            return render(request, 'mainpage.html', {'analysis_content': analysis_content, 'username': username})
    return render(request, "mainpage.html", {'random_question': random_question, 'username': username})

def yourfeedback(request):
    username = request.session.get('username')
    user_feedback = get_user_feedback(username)
    return render(request, 'yourfeedback.html', {'user_feedback': user_feedback, 'username': username})

def analyseInterviewAns(question, answer, modelAns):
    api_key = '' #hidden for security reasons
    client = OpenAI(api_key=api_key) 
    
    prompt = f"""Compare the user's answer to this model answer: {modelAns}.
            Highlight the pros and cons to the user's answer if any.
            Highlight if the user has used the STAR method.
            Highlight if they have used these skills: Communication
            The tone should be conversational and spartan, Say well done after the answer is recieved.
            Do not say the user instead say You. Address the user personally."""  

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
        max_tokens=300,
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
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-7)

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

def logout(request):
    request.session.clear()
    return redirect('login')

def save_feedback(question, feedback_text, username):
    feedback = Feedback(username=username, feedback_text=feedback_text, question=question)
    feedback.save()

def get_user_feedback(username):
    feedbacks = Feedback.objects.filter(username=username).order_by('-date')
    return feedbacks
