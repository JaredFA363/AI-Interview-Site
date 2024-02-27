from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Questions, Feedback
from openai import OpenAI
import random
import pyttsx3
from cryptography.fernet import Fernet

key = b'JBIKcN-tjOx96f3cgAOgOYbpgv8i0eQ4GlMPEBqK9nY='
cipher_suite = Fernet(key)

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
                analysis = analyseInterviewAns(random_question.question,input,random_question.model_answer)
                analysis_content = analysis.choices[0].message.content
                return render(request, 'custominterview.html', {'analysis_content': analysis_content, 'username': username})
        
        if 'save_feedback' in request.POST:
            feedback_text = request.POST.get('response', '')
            save_feedback(random_question.question,feedback_text,username)
            messages.success(request,"Feedback saved successfully")
    return render(request, "custominterview.html", {'random_question': random_question, 'username': username})

def homepage(request):
    username = request.session.get('username')
    random_question = get_random_question()
    if request.method == 'POST':
        if 'save_feedback' in request.POST:
            feedback_text = request.POST.get('response', '')
            save_feedback(random_question.question,feedback_text,username)
            messages.success(request,"Feedback saved successfully")
        else:   
            input = request.POST['q']
            analysis = analyseInterviewAns(random_question.question,input,random_question.model_answer)
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

    # Using the GPT-4 model to analyse the answer
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

    return response

def text_to_speech(text):
    # Initialising the text-to-speech engine
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-7)

    engine.say(text)
    engine.runAndWait()

def get_random_question():
    count = Questions.objects.count()

    if count > 0:
        random_offset = random.randint(0, count - 1)
        random_question = Questions.objects.all()[random_offset]
    else:
        random_question = "Cannot display question"
    
    return random_question

def get_question_by_skill(skill):
    # Get all questions with the specified skill
    questions_with_skill = Questions.objects.filter(skill=skill)

    if questions_with_skill.exists():
        random_question = random.choice(questions_with_skill)
    else:
        random_question = None
    return random_question

def logout(request):
    request.session.clear()
    return redirect('login')

def save_feedback(question, feedback_text, username):
    encrypted_feedback = encrypt_feedback(bytes(feedback_text,'utf-8'))
    feedback = Feedback(username=username, feedback_text=encrypted_feedback, question=question)
    feedback.save()

def get_user_feedback(username):
    user_feedback = []
    feedbacks = Feedback.objects.filter(username=username).order_by('-date')
    for feedback in feedbacks:
        decrypted_feedback = decrypt_feedback(feedback.feedback_text).decode("utf-8")
        user_feedback.append({'question': feedback.question, 'feedback_text':decrypted_feedback})
    return user_feedback

def encrypt_feedback(feedback_text):
    encrypted_text = cipher_suite.encrypt(feedback_text)
    return encrypted_text

def decrypt_feedback(encrypted_text):
    byte_encrypted_text = encrypted_text[2:-1].encode('utf-8')
    decrypted_text = cipher_suite.decrypt(byte_encrypted_text)
    return decrypted_text
    