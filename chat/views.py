# chat/views.py
from django.shortcuts import render
from django.http import JsonResponse
import requests
import json
from datetime import datetime
import pytz


def index(request):
    if request.method == 'GET':
        # API로 메시지 전송
        response = requests.get('https://script.google.com/macros/s/AKfycbzk2zzEfZivjKRwPz9-u_cIaSGo9tzkQ9gW4XXfc_FEWW_He8G7bMCDFdaP0AfL08qVMg/exec')

        response_list = []

        if response.status_code == 200:
            try:
                json_data = response.json()
                for x in json_data['json']:
                    nickname_index = x['Nickname']

                    if nickname_index == 'GPTs_Answer_Assistant':
                        nickname_index = '🐱CATCEO🐾'

                    utc_time = datetime.strptime(x['Time'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    utc_time = utc_time.replace(tzinfo=pytz.utc)
                    ny_time = utc_time.astimezone(pytz.timezone('America/New_York'))

                    response_list.append({
                        'Nickname': nickname_index,
                        'Content': x['Content'],
                        'Time': ny_time.strftime('%Y-%m-%d %H:%M:%S %Z')
                    })

            except ValueError:
                # JSONDecodeError 처리
                return JsonResponse({'error': 'Invalid JSON response'}, status=500)

        return render(request, 'index.html', {'messages': response_list})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def send_message(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        content = request.POST.get('content')

        # API로 메시지 전송
        response = requests.post('https://script.google.com/macros/s/AKfycbzk2zzEfZivjKRwPz9-u_cIaSGo9tzkQ9gW4XXfc_FEWW_He8G7bMCDFdaP0AfL08qVMg/exec', json={
            'Nickname': nickname,
            'Content': content
        })


        response_list = []
        for x in response.json():
            nickname_index = x['Nickname']

            if nickname_index == 'GPTs_Answer_Assistant':
                nickname_index = '🐱CATCEO🐾'

            response_list.append({
                'Nickname': nickname_index,
                'Content': x['Content'],
                'Time': x['Time']
            })

        
        return JsonResponse(response_list, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)
