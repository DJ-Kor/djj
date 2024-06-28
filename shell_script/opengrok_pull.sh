#!/bin/bash

echo " ----------- Start OpenGrok_Pull.sh ! $(date) ----------- "

cd /raid5s4/opengrok/src || { echo "Failed to change directory"; exit 1; }
echo $PWD

# 하위 모든 디렉토리를 순회
find . -type d -name ".git" | while read -r git_dir; do
    # .git 디렉토리의 부모 디렉토리로 이동
    repo_dir=$(dirname "$git_dir")
    echo "Repository: $repo_dir"
    # git pull 수행
    cd "$repo_dir" || { echo "디렉토리로 이동할 수 없습니다: $repo_dir"; continue; }
    git pull
    
    # master 브랜치로 체크아웃 (존재하는 경우에만)
    # if git branch --list master > /dev/null; then
    #     git checkout master
    # else
    #     echo "master 브랜치가 존재하지 않습니다: $repo_dir"
    # fi

    cd - > /dev/null || { echo "이전 디렉토리로 돌아갈 수 없습니다."; exit 1; }
done

echo " ----------- Done OpenGrok_Pull.sh ! $(date) ----------- "
