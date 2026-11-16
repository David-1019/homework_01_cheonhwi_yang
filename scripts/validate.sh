#!/bin/bash
#서버 응답 확인
sleep 5                             # 서버가 뜰 때까지 대기
# /docs 응답이 200이 아니면 실패 → CodeDeploy에서 배포 실패로 표시
curl -f http://localhost:8000/docs