aws 라이트세일  

![alt text](<images/markdown-Pasted image 20240702153050.png>)

dns 생성  





- 스테틱도 만들어야함

깃허브 디플로이 yml 설정할때
![alt text](<images/markdown-Pasted image 20240702153211.png>)

- WHIZ_SERVER_HOST = ip
- WHIZ_SERVER_SSH_KEY = pem key
- 브랜치 도 변경
  ![alt text](<images/markdown-Pasted image 20240702153338.png>)
- 깃액션 깃 풀 명령어 변경
  ![alt text](<images/markdown-Pasted image 20240702154936.png>)

---

# 맨처음 깃 푸쉬할때

[여기서 절차대로 해야함](https://github.com/bamjun/oz-test-miniproject-1)

깃허브 리드 비 키

```
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
```

- nginx.conf - 도메인변경 ( 24번째줄) 18번째줄
- 26 27 번째출 ssl 경로도 변경
  ![alt text](<images/markdown-Pasted image 20240702155024.png>)

![alt text](<images/markdown-Pasted image 20240702155625.png>)

[여기서 설명보고 ssl 발급](https://github.com/bamjun/catceo_coin)

# 채팅할때

```python
CSRF_TRUSTED_ORIGINS = [

    'https://colorwhiz.xyz',

]
```

config.ini 복사하기

---

---

---

- workflows 바꿔야함. 깃허브에 변수도 새로저장해야함..

#open ai 키넣어야함.

CSRF_TRUSTED_ORIGINS = [
'https://sangmodoge.com',
]

### SSL 인증서 설정 (선택 사항)

Let's Encrypt를 사용하여 SSL 인증서를 설정할 수 있습니다. Certbot을 사용하여 SSL 인증서를 자동으로 발급하고 갱신할 수 있습니다.

#### Certbot 설치 및 인증서 발급

```sh
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx
```

#### Certbot을 사용하여 SSL 인증서 발급

```sh
sudo certbot --nginx -d cat.ceo
```

Certbot은 Nginx 설정 파일을 자동으로 업데이트하여 SSL 설정을 추가합니다.

```sh
sudo lsof -i :80
```

```sh
sudo kill -9 [pid]
```

### 5. GitHub Actions 설정

배포 스크립트를 업데이트하여 Nginx를 재시작하도록 합니다.

#### `.github/workflows/deploy.yml`

```yaml
name: Deploy to Server

on:
  push:
    branches:
      - main  # 또는 배포하고 싶은 브랜치 이름

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SERVER_SSH_KEY }}
        port: ${{ secrets.AWS_SSH_PORT }}
        script: |
          cd ~/catceo_coin
          git stash
          git pull origin main
          sudo docker-compose -f docker-compose.yml up --build -d
          sudo systemctl restart nginx

    - name: Send notification to Discord
      run: |
        curl -X POST -H "Content-Type: application/json" \
          -d '{"content": "Deployment to server is complete!\nRepository: '${{ github.repository }}'\nCommit: '${{ github.sha }}'\nBranch: '${{ github.ref }}'"}' \
          ${{ secrets.DISCORD_WEBHOOK_URL }}
```

위 설정을 통해 `main` 브랜치에 푸시될 때마다 GitHub Actions가 실행되고, Nginx가 자동으로 재시작됩니다. 이를 통해 도메인 설정이 반영된 상태로 배포가 완료됩니다. 모든 설정이 제대로 되었는지 확인하면서 진행하시기 바랍니다.
