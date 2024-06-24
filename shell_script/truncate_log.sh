#!/bin/bash
# 각 docker container folder을 순회하면서
# *-json.log file을 현재 날짜로 복사 & truncate하는 bash

# 실행하려면 ./truncatelog.sh 를 입력하세요.

# 실행 위치에서 -json.log로 끝나는 파일 찾기
files=$(find . -name "*-json.log" -type f -print)
echo "$file"

if [ -z "$files" ]; then
  echo "파일을 찾을 수 없습니다."
  exit 1
fi

# 오늘의 날짜 구하기
date=$(date +%Y-%m-%d)

for file in $files; do
  # 새로운 파일 경로 생성
  new_file=$(dirname "$file")/"${date}-json.log"

  # 원본 log 복사
  cp "$file" "$new_file"
  echo "log copy complete for $file."

  # 원본 log truncate
  truncate -s 0 "$file"
  echo "log truncate complete for $file."
done

# created 24-01-22 / dj
