from django.shortcuts import render
from django.http import JsonResponse
from .models import BaseFirstChat
from django.utils import timezone
import requests
import json
from datetime import datetime, timedelta
import pytz
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def index(request):
    if request.method == 'GET':
        messages = BaseFirstChat.objects.all().order_by('time')[:20]
        response_list = []
        for message in messages:
            ny_time = message.time.astimezone(pytz.timezone('America/New_York'))
            nickname_index = message.nickname
            if nickname_index == 'GPTs_Answer_Assistant':
                nickname_index = '🐱CATCEO🐾'
            
            response_list.append({
                'Nickname': nickname_index,
                'Content': message.content,
                'Time': ny_time.strftime('%Y-%m-%d %H:%M:%S %Z')
            })
        return render(request, 'index.html', {'messages': response_list})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def send_message(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        content = request.POST.get('content')
        
        if len(nickname) > 10:
            return JsonResponse({'message': 'Nickname exceeds 10 characters'}, status=400)
        if len(content) > 50:
            return JsonResponse({'message': 'Content exceeds 50 characters'}, status=400)
        
        last_message = BaseFirstChat.objects.last()
        if last_message and (timezone.now() - last_message.time).total_seconds() < 5:
            messages = BaseFirstChat.objects.all().order_by('-time')[:20]
            response_list = format_messages(messages)
            return JsonResponse(response_list, safe=False)
        
        new_message = BaseFirstChat.objects.create(nickname=nickname, content=content)
        
        recent_messages = BaseFirstChat.objects.all().order_by('time')[:20]
        recent_rows = format_messages(recent_messages)
        
        response_text = send_openai_request(recent_rows)
        
        BaseFirstChat.objects.create(nickname='GPTs_Answer_Assistant', content=response_text)
        
        updated_messages = BaseFirstChat.objects.all().order_by('time')[:20]
        updated_rows = format_messages(updated_messages)
        
        return JsonResponse(updated_rows, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def format_messages(messages):
    response_list = []
    for message in messages:
        ny_time = message.time.astimezone(pytz.timezone('America/New_York'))
        nickname_index = message.nickname
        if nickname_index == 'GPTs_Answer_Assistant':
            nickname_index = '🐱CATCEO🐾'
        
        response_list.append({
            'Nickname': nickname_index,
            'Content': message.content,
            'Time': ny_time.strftime('%Y-%m-%d %H:%M:%S %Z')
        })
    return response_list

def send_openai_request(recent_rows):
    prompt_text = 'The Nickname GPT_you is you. You are CATCEO. CATCEO is a service for sharing charming and adorable cats. You can get random cat photos through an API. The following sentences are what people are saying to you. Respond in a fun way.'
    system_message = {"role": "system", "content": prompt_text}
    messages = [system_message]
    
    for row in recent_rows:
        nickname_index = "assistant" if row['Nickname'] == "GPTs_Answer_Assistant" else "user"
        messages.append({
            "role": nickname_index,
            "content": row['Content']
        })
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + config['OPENAI']['API_KEY']
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'temperature': 0.5,
        'messages': messages
    }
    
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    result = response.json()
    
    cat_image_url = fetch_cat_image_url()
    
    return result['choices'][0]['message']['content'] + '\n' + cat_image_url

def fetch_cat_image_url():
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    result = response.json()
    return result[0]['url']
