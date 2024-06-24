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