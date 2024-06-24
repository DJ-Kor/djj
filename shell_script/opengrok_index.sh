#!/bin/bash

echo " ----------- Start OpenGrok_Pull.sh ! ----------- "

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
    cd - > /dev/null || { echo "이전 디렉토리로 돌아갈 수 없습니다."; exit 1; }
done

echo " ----------- Done OpenGrok_Pull.sh ! ----------- "

iddx@iddx-server4:~/bin$ ^C
iddx@iddx-server4:~/bin$ cat opengrok_index.sh
#!/bin/bash
echo " ----------- Start OpenGrok_Index.sh ! $(date) ----------- "

# 사용자 정의 ctags 함수 정의
ctags() {
    command ctags "$@" 2> >(
        grep -Ev "^ctags: Warning: ignoring null tag in .+\.js\(line: .+\)$"
    )
}

# Docker 컨테이너가 실행 중인지 확인
CONTAINER_NAME="OpenGrok"
INDEXING_CMD="java \
            -Djava.util.logging.config.file=/opengrok/doc/logging.properties \
            -jar /opengrok/lib/opengrok.jar \
            -c ctags \
            -s /opengrok/src -d /opengrok/data -H -P -S -G \
            -W /opengrok/etc/configuration.xml -U http://localhost:8080 \
            -i node_modules -i .cache -i .config -i site-packages -i bin"

if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}\$"; then
    echo "Docker container ${CONTAINER_NAME} is running."

    # Docker 컨테이너 내부에서 명령어 실행
    docker exec -i ${CONTAINER_NAME} bash -c "$INDEXING_CMD"
else
    echo "Docker container ${CONTAINER_NAME} is not running."
fi

echo " ----------- Done OpenGrok_Index.sh ! $(date) ----------- "
