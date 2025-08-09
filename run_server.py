#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastAPI 서버 실행 스크립트
"""

import uvicorn
import os
from dotenv import load_dotenv

def main():
    # 환경 변수 로드
    load_dotenv()
    
    # 서버 설정
    host = "0.0.0.0"  # 모든 IP에서 접근 가능
    port = 8000
    
    print(f"🚀 AIVA AI Chat API 서버를 시작합니다...")
    print(f"📍 서버 주소: http://{host}:{port}")
    print(f"🔗 API 엔드포인트: http://{host}:{port}/chat")
    print(f"📊 상태 확인: http://{host}:{port}/")
    print("=" * 50)
    
    # 서버 실행
    uvicorn.run(
        "server:app",
        host=host,
        port=port,
        reload=True,  # 개발 모드에서 자동 재시작
        log_level="info"
    )

if __name__ == "__main__":
    main() 