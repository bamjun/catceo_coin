from django.shortcuts import render
from django.http import JsonResponse
from .models import BaseFirstChat
from django.utils import timezone
import requests
from asgiref.sync import async_to_sync
import pytz
import configparser
from channels.layers import get_channel_layer



config = configparser.ConfigParser()
config.read('config.ini')


def index(request):
    if request.method == 'GET':
        messages = BaseFirstChat.objects.all().order_by('-time')[:20][::-1]
        response_list = format_messages(messages)
        return render(request, 'index.html', {'messages': response_list})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def send_message(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        content = request.POST.get('content')
        
        if len(nickname) > 10:
            return JsonResponse({'message': 'Nickname exceeds 10 characters'}, status=412)
        if len(content) > 500:
            return JsonResponse({'message': 'Content exceeds 50 characters'}, status=413)
        
        last_message = BaseFirstChat.objects.last()
        if last_message and (timezone.now() - last_message.time).total_seconds() < 5:
            return JsonResponse({'message': 'You must wait 5 seconds between messages'}, status=400)
        
        new_message = BaseFirstChat.objects.create(nickname=nickname, content=content)
        
        # GPT에게 메시지 요청
        recent_messages = BaseFirstChat.objects.all().order_by('-time')[:20][::-1]
        recent_rows = format_messages(recent_messages)

        
        response_text = send_openai_request(recent_rows)
        
        gpt_message = BaseFirstChat.objects.create(nickname='GPTs_Answer_Assistant', content=response_text)
        
        # WebSocket을 통해 메시지 전송
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'chat_group',
            {
                'type': 'chat_message',
                'nickname': nickname,
                'content': content,
                'timestamp': new_message.time.astimezone(pytz.timezone('America/New_York')).strftime('%Y-%m-%d %H:%M:%S %Z')
            }
        )
        async_to_sync(channel_layer.group_send)(
            'chat_group',
            {
                'type': 'chat_message',
                'nickname': '🐱CATCEO🐾',
                'content': response_text,
                'timestamp': gpt_message.time.astimezone(pytz.timezone('America/New_York')).strftime('%Y-%m-%d %H:%M:%S %Z')
            }
        )
        
        updated_messages = BaseFirstChat.objects.all().order_by('-time')[:2][::-1]
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
        nickname_index = "assistant" if row['Nickname'] == "🐱CATCEO🐾" else "user"
        messages.append({
            "role": nickname_index,
            "content": row['Content'],
            "Nickname": row['Nickname'],
            "Time": row['Time']
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