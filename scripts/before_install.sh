#!/bin/bash
# 기존 배포 폴더 삭제 후 새로 생성 (이전 파일 찌꺼기 방지)
rm -rf /home/ubuntu/2.structure
mkdir -p /home/ubuntu/2.structure
chown ubuntu:ubuntu /home/ubuntu/2.structure