#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON 파일 로딩 테스트
"""

import json

def test_json_loading():
    try:
        with open('.prompts/fewshot_examples.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("JSON 파일 로딩 성공!")
        print("시스템 지침:", data.get("system_instruction"))
        print("예시 개수:", len(data.get("examples", [])))
        
        for i, example in enumerate(data.get("examples", []), 1):
            print(f"예시 {i}:")
            print(f"  질문: {example.get('question')}")
            print(f"  답변: {example.get('answer')}")
            print()
            
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_json_loading() 