#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAI API 콘솔 Q&A 애플리케이션
"""
import os
import json
import requests
from dotenv import load_dotenv

def load_env_vars():
    load_dotenv(dotenv_path='.env', encoding='utf-8-sig')
    api_url = os.getenv("OPENAI_API_URL")
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")
    if not api_url or not api_key or not model:
        raise RuntimeError("환경변수(.env)에서 OPENAI_API_URL, OPENAI_API_KEY, OPENAI_MODEL을 모두 불러와야 합니다.")
    return api_url, api_key, model

def load_fewshot():
    with open(".prompts/fewshot_examples.json", encoding="utf-8") as f:
        data = json.load(f)
    system_instruction = data.get("system_instruction", "")
    examples = data.get("examples", [])
    return system_instruction, examples

def build_messages(system_instruction, examples, user_question):
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

def call_openai_api(api_url, api_key, model, messages):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 256
    }
    resp = requests.post(api_url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()

def extract_answer(response_json):
    try:
        return response_json["choices"][0]["message"]["content"].strip()
    except Exception:
        return json.dumps(response_json, ensure_ascii=False, indent=2)

def main():
    try:
        api_url, api_key, model = load_env_vars()
        system_instruction, examples = load_fewshot()
    except Exception as e:
        print(f"초기화 오류: {e}")
        return
    print("="*50)
    print("OpenAI API Q&A 콘솔")
    print("질문을 입력하세요. (종료: quit/exit/종료)")
    print("="*50)
    while True:
        user_question = input("\n질문: ").strip()
        if user_question.lower() in ["quit", "exit", "종료"]:
            print("종료합니다.")
            break
        if not user_question:
            print("질문을 입력해주세요.")
            continue
        messages = build_messages(system_instruction, examples, user_question)
        try:
            response_json = call_openai_api(api_url, api_key, model, messages)
            answer = extract_answer(response_json)
            print("\n" + "-"*40)
            print("답변:")
            print(answer)
            print("-"*40)
        except Exception as e:
            print(f"API 호출 오류: {e}")

if __name__ == "__main__":
    main() 