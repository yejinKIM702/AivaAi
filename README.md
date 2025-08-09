# Aiva AI 프로젝트

이 프로젝트는 Python 가상환경으로 설정된 기본 프로젝트입니다.

## 설치 및 실행

### 1. 가상환경 활성화
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows Command Prompt
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
pip install fastapi uvicorn openai python-dotenv
```

### 3. 환경 변수 설정
`.env` 파일을 생성하고 OpenAI API 키를 설정하세요:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. FastAPI 서버 실행
```bash
# 방법 1: uvicorn 직접 실행
uvicorn server:app --host 0.0.0.0 --port 8000 --reload

# 방법 2: Python 스크립트 실행
python run_server.py
```

### 5. Flutter 앱과 연동
1. FastAPI 서버가 실행 중인지 확인
2. Flutter 앱 실행: `flutter run`
3. 앱에서 채팅 기능 사용

## API 엔드포인트

- `GET /` - 서버 상태 확인
- `POST /chat` - AI 채팅 API
  - Request: `{"message": "사용자 메시지"}`
  - Response: `{"response": "AI 응답"}`

## 프로젝트 구조
```
test01/
├── venv/           # Python 가상환경
├── server.py       # FastAPI 서버
├── run_server.py   # 서버 실행 스크립트
├── chat_app.py     # 콘솔 채팅 앱
├── requirements.txt # 패키지 의존성
├── .env            # 환경 변수
└── README.md       # 프로젝트 설명
```

## Flutter 앱 연동

Flutter 앱(`aiva_app`)은 `http://10.0.2.2:8000` 주소로 FastAPI 서버에 연결됩니다.

- Android 에뮬레이터: `10.0.2.2:8000`
- 실제 디바이스: 실제 서버 IP 주소로 변경 필요 
