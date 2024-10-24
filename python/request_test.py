import requests


def test_url_blocked(url):
    try:
        # HTTP 요청 보내기
        response = requests.get(url, timeout=11)

        # 성공적인 응답
        if response.status_code == 200:
            print(f"접속 성공: {url}")
        else:
            print(f"접속 실패: {url}, 상태 코드: {response.status_code}")

    except requests.exceptions.Timeout:
        print(f"타임아웃 발생: {url}")
    except requests.exceptions.ConnectionError:
        print(f"연결 오류: {url}. 차단되었을 가능성이 있습니다.")
    except requests.exceptions.RequestException as e:
        # 기타 예외 처리
        print(f"요청 중 오류 발생: {e}")


# 테스트할 URL 입력
test_url = 'https://huggingface.co'
u2 = "http://www.lge.com"
u3 = "http://iddx.lge.com"
u4 = "http://www.naver.com"

urls = [test_url, u2, u3, u4]
# 함수 호출
for url in urls:
    test_url_blocked(url)
