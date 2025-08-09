from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatRequest(BaseModel):
    message: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_fewshot_examples():
    """
    .prompts/fewshot_examples.json 파일에서 few-shot 예시를 로드합니다.
    """
    try:
        with open('.prompts/fewshot_examples.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        # 파일이 없으면 기본값 반환
        return {
            "system_instruction": "당신은 아이를 키우는 부모님들을 위한 AI 육아 비서입니다. 친근하고 전문적인 조언을 제공해주세요.",
            "examples": []
        }
    except json.JSONDecodeError:
        return {
            "system_instruction": "당신은 아이를 키우는 부모님들을 위한 AI 육아 비서입니다. 친근하고 전문적인 조언을 제공해주세요.",
            "examples": []
        }

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

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        # few-shot 예시 로드
        fewshot = load_fewshot_examples()
        system_instruction = fewshot.get("system_instruction", "")
        examples = fewshot.get("examples", [])
        
        # 메시지 구성
        messages = build_messages(system_instruction, examples, req.message)
        
        # OpenAI API 호출
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        answer = resp.choices[0].message.content.strip()
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "AIVA AI Chat API is running"} 