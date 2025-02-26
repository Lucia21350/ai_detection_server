Build
```markdown
docker-compose up --build // 서버에서 docker 일괄 실행:
```

실행 중인 컨테이너 정리

```markdown
docker stop $(docker ps -q)
docker rm $(docker ps -aq)
```

기존의 캐시된 이미지와 볼륨 삭제

```markdown
docker system prune -a --volumes -f
```
