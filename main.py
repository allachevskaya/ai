from g4f.client import Client
from starlette.responses import JSONResponse
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

app = FastAPI(
  title="KM AI",
  summary="KM gpt",
  version="0.0.1",
)
client = Client()

# Схема OAuth2 для работы с токеном
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AIModel(BaseModel):
  prompt: str = Field(default=None, examples=["Сколько букв в слове мама"])


@app.post("/ai")
def generate(request: AIModel, token: str = Depends(oauth2_scheme)):
  # Проверка токена (можно добавить логику валидации)
  if token != "expected_token":
    raise HTTPException(
      status_code=401,
      detail="Invalid or expired token"
    )

  try:
    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[{"role": "user", "content": request.prompt}],
    )
    result = response.choices[0].message.content
    return JSONResponse(
      content={
        "data": result,
        "detail": "success",
        "status": 200
      }
    )
  except Exception as e:
    return JSONResponse(
      content={
        "data": None,
        "detail": str(e),
        "status": 500
      }
    )
