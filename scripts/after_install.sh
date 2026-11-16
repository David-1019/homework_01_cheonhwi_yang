#!/bin/bash
#가상환경 + 패키지 설치
set -e                              # 명령 하나라도 실패하면 즉시 중단(배포 실패 처리)
cd /home/ubuntu/2.structure
python3 -m venv .venv                # EC2에서 가상환경 생성
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt