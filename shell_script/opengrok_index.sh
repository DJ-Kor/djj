#!/bin/bash
echo " ----------- Start OpenGrok_Index.sh ! $(date) ----------- "

# 사용자 정의 ctags 함수 정의
ctags() {
    command ctags "$@" 2> >(
        grep -Ev "^ctags: Warning: ignoring null tag in .+\.js\(line: .+\)$|^ctags: Warning: Unknown language \"XML:"
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
