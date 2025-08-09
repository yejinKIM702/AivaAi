#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
콘솔 기반 OpenAI API 채팅 애플리케이션
사용자 질문을 입력받아 OpenAI API에 전송하고 답변을 받습니다.
"""

import json
import requests
from dotenv import load_dotenv
import os

def load_environment_variables():
    """
    .env 파일에서 환경변수를 로드합니다.
    Returns:
        dict: 환경변수 딕셔너리
    """
    load_dotenv(dotenv_path='.env', encoding='utf-8-sig')
    required_vars = ['OPENAI_API_URL', 'OPENAI_API_KEY', 'OPENAI_MODEL']
    env_vars = {}
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            raise ValueError(f"필수 환경변수가 설정되지 않았습니다: {var}")
        env_vars[var] = value
    return env_vars

def load_fewshot_examples():
    """
    .prompts/fewshot_examples.json 파일에서 few-shot 예시를 로드합니다.
    Returns:
        dict: few-shot 예시 데이터
    """
    try:
        with open('.prompts/fewshot_examples.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise FileNotFoundError("파일을 찾을 수 없습니다: .prompts/fewshot_examples.json")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"JSON 파싱 오류: {e}")

def build_messages(system_instruction, examples, user_question):
    """
    OpenAI messages 포맷으로 변환
    """
    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    for ex in examples:
        q = ex.get("question", "")
        a = ex.get("answer", "")
        if q and a:
            messages.append({"role": "user", "content": q})
            messages.append({"role": "assistant", "content": a})
    messages.append({"role": "user", "content": user_question})
    return messages

def call_openai_api(env_vars, messages):
    headers = {
        "Authorization": f"Bearer {env_vars['OPENAI_API_KEY']}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": env_vars["OPENAI_MODEL"],
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 256
    }
    resp = requests.post(env_vars["OPENAI_API_URL"], headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()

def extract_answer(response_json):
    try:
        return response_json["choices"][0]["message"]["content"].strip()
    except Exception:
        return json.dumps(response_json, ensure_ascii=False, indent=2)

def main():
    try:
        env_vars = load_environment_variables()
        fewshot = load_fewshot_examples()
        system_instruction = fewshot.get("system_instruction", "")
        examples = fewshot.get("examples", [])
    except Exception as e:
        print(f"초기화 오류: {e}")
        return
    print("="*50)
    print("OpenAI API Q&A 콘솔")
    print("질문을 입력하세요. (종료: quit/exit/종료)")
    print("="*50)
    
    is_first_interaction = True
    
    while True:
        user_question = input("\n질문: ").strip()
        if user_question.lower() in ["quit", "exit", "종료"]:
            print("종료합니다.")
            break
        if not user_question:
            print("질문을 입력해주세요.")
            continue
        
        # 첫 번째 상호작용인 경우 요약을 포함한 응답 생성
        if is_first_interaction:
            # 요약을 위한 추가 프롬프트 생성
            summary_prompt = f"다음 질문을 간결하게 요약해주세요: {user_question}"
            summary_messages = [{"role": "user", "content": summary_prompt}]
            
            try:
                # 요약 생성
                summary_response = call_openai_api(env_vars, summary_messages)
                summary = extract_answer(summary_response)
                
                # 원래 질문에 대한 답변 생성
                messages = build_messages(system_instruction, examples, user_question)
                response_json = call_openai_api(env_vars, messages)
                answer = extract_answer(response_json)
                
                # 출처 정보 생성
                sources_prompt = f"다음 답변의 출처가 될 수 있는 문서, URL, 데이터베이스 등을 배열 형태로 나열해주세요. 답변: {answer}"
                sources_messages = [{"role": "user", "content": sources_prompt}]
                sources_response = call_openai_api(env_vars, sources_messages)
                sources = extract_answer(sources_response)
                
                # 응답에 summarized와 sources 필드 포함
                final_response = {
                    "answer": answer,
                    "summarized": summary,
                    "sources": sources
                }
                
                print("\n" + "-"*40)
                print("답변:")
                print(f"요약: {summary}")
                print(f"답변: {answer}")
                print(f"출처: {sources}")
                print("-"*40)
                
                is_first_interaction = False
                
            except Exception as e:
                print(f"API 호출 오류: {e}")
        else:
            # 두 번째 상호작용부터는 일반적인 응답
            messages = build_messages(system_instruction, examples, user_question)
            try:
                response_json = call_openai_api(env_vars, messages)
                answer = extract_answer(response_json)
                
                # 출처 정보 생성
                sources_prompt = f"다음 답변의 출처가 될 수 있는 문서, URL, 데이터베이스 등을 배열 형태로 나열해주세요. 답변: {answer}"
                sources_messages = [{"role": "user", "content": sources_prompt}]
                sources_response = call_openai_api(env_vars, sources_messages)
                sources = extract_answer(sources_response)
                
                print("\n" + "-"*40)
                print("답변:")
                print(answer)
                print(f"출처: {sources}")
                print("-"*40)
            except Exception as e:
                print(f"API 호출 오류: {e}")

if __name__ == "__main__":
    main() 