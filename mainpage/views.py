from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from openai import OpenAI
import pyttsx3

# Create your views here.
def homepage(request):
    if request.method == 'POST':    
        input = request.POST['q']
        analysis = analyseInterviewAns("Tell me about a time you communicated",input,"I communicated when i was at work")
        analysis_content = analysis.choices[0].message.content
        text_to_speech(analysis_content)
        return HttpResponse(f'The text submitted is: {analysis_content}')
    return render(request, "mainpage.html")

def analyseInterviewAns(question, answer, modelAns):
    api_key = '' #hidden for security reasons
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
                "content": "Analyzing the interview question answer."
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