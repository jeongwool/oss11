# 🚀Operator API: 
실습 1 - Rate Limit 시스템 구축본 프로젝트는 AI 에이전트의 폭발적인 트래픽으로부터 플랫폼을 보호하는 '운영자(Operator)'의 관점에서 설계되었습니다. 특히 AI가 사람보다 100배 빠른 속도로 코드를 생성하고 호출하는 Software 3.0 시대의 병목 문제를 해결하기 위한 호출 제어(Rate Limiting) 기술을 실습합니다.  

# 🏗️아키텍처 (Architecture)
본 시스템은 유저의 요청이 실제 비즈니스 로직에 도달하기 전, 운영 미들웨어 층(Operator Layer)에서 트래픽을 먼저 필터링하는 구조를 가집니다.  Client: AI 에이전트 또는 사용자.Operator Layer (Rate Limiter): slowapi를 이용한 톨게이트 역할. 요청의 IP를 식별하여 허용 범위를 체크합니다.  App Logic: 실제 서비스를 제공하는 FastAPI 엔드포인트.

# 🛠️적용 알고리즘 (Algorithm)선택한 알고리즘: 
Token Bucket (토큰 버킷)   작동 원리:시스템은 분당 10개의 토큰을 발급합니다.  요청이 들어올 때마다 버킷에서 토큰 1개를 소비합니다.  버킷이 비어 있으면(토큰이 없으면) 즉시 429 Too Many Requests 응답을 보내 시스템 부하를 차단합니다.  

# 💻실습 코드 (Code)Python

from fastapi import FastAPI, Request

from slowapi import Limiter

from slowapi.util import get_remote_address

# 1. 운영자 설정: 접속자 IP 기반의 Limiter 인스턴스 생성 [cite: 440]

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

app.state.limiter = limiter

@app.get("/hello")

# 2. 운영 통제: 분당 10회 호출 제한 적용 [cite: 444]

@limiter.limit("10/minute")

async def hello(request: Request):

    return {"message": "Hello World"}

# 🧪테스트 방법 (Test Method)환경 구축: 
1. 터미널에 `uvicorn main:app --reload`를 입력하여 서버를 실행합니다.
2. 브라우저에서 `http://127.0.0.1:8000/hello`에 접속합니다.
3. 부하 테스트: 브라우저 혹은 터미널에서 http://127.0.0.1:8000/hello 주소를 1분 이내에 11회 이상 연속 호출합니다.  

# 📊실행 결과 (Rate Limit 확인)1~10회 호출: 
정상적으로 {"message": "Hello World"} 메시지 반환 (HTTP 200 OK).11회 호출 시: 서버가 요청을 거부하며 아래와 같은 에러 응답을 반환합니다.  Response Body: {"detail": "10 per 1 minute"}Status Code: 429 Too Many Requests (터미널 로그에서 확인 가능).
