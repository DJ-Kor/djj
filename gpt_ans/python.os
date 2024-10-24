os 모듈
파일 및 디렉토리 작업
os.getcwd(): 현재 작업 디렉토리를 반환합니다.
os.chdir(path): 현재 작업 디렉토리를 변경합니다.
os.listdir(path): 지정된 디렉토리의 파일 및 디렉토리 목록을 반환합니다.
os.mkdir(path): 디렉토리를 생성합니다.
os.makedirs(path): 중첩된 디렉토리를 생성합니다.
os.remove(path): 파일을 삭제합니다.
os.rmdir(path): 디렉토리를 삭제합니다.
os.rename(src, dst): 파일 또는 디렉토리의 이름을 변경합니다.
환경 변수
os.getenv(key, default=None): 환경 변수의 값을 반환합니다. 환경 변수가 존재하지 않으면 default 값을 반환합니다.
os.environ: 모든 환경 변수를 포함하는 딕셔너리 객체입니다.
경로 조작
os.path.join(path, *paths): 여러 경로 요소를 결합하여 하나의 경로를 만듭니다.
os.path.abspath(path): 절대 경로를 반환합니다.
os.path.basename(path): 경로의 마지막 구성 요소를 반환합니다.
os.path.dirname(path): 경로의 디렉토리 이름을 반환합니다.
os.path.exists(path): 경로가 존재하는지 확인합니다.
os.path.isfile(path): 경로가 파일인지 확인합니다.
os.path.isdir(path): 경로가 디렉토리인지 확인합니다.
os.path.expanduser(path): 사용자 홈 디렉토리를 확장합니다.
sys 모듈
시스템 관련 정보
sys.argv: 명령줄 인수 목록을 반환합니다.
sys.exit([arg]): 프로그램을 종료합니다.
sys.path: 모듈 검색 경로를 나타내는 리스트입니다.
sys.platform: 현재 플랫폼의 이름을 반환합니다.
sys.version: Python 인터프리터의 버전 정보를 반환합니다.
sys.modules: 현재 로드된 모듈을 나타내는 딕셔너리입니다.