from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from langchain.messages import HumanMessage
from src.graph import graph_app

app = FastAPI(
    title="Oyun Bulma Ajanı",
    description="LangGraph + Tailwind UI"
)

# Template motorunu ayarla (templates klasörünü göster)
templates = Jinja2Templates(directory="templates")


# --- Veri Modelleri ---
class UserRequest(BaseModel):
    query: str


class AgentResponse(BaseModel):
    response: str
    tool_used: bool = False


# --- 1. Sayfa Endpoint'i (Frontend'i Sunar) ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # index.html dosyasını render et
    return templates.TemplateResponse("index.html", {"request": request})


# --- 2. Chat API Endpoint'i (Frontend buraya istek atar) ---
@app.post("/chat", response_model=AgentResponse)
async def chat_endpoint(request: UserRequest):
    try:
        initial_state = {"messages": [HumanMessage(content=request.query)]}
        print(f"📩 Web İstek: {request.query}")

        result = graph_app.invoke(initial_state)

        last_message = result["messages"][-1]
        content = last_message.content

        final_text = ""
        if isinstance(content, list):
            final_text = "".join([block.get("text", "") for block in content if "text" in block])
        else:
            final_text = str(content)

        return AgentResponse(
            response=final_text,
            tool_used=len(result["messages"]) > 2
        )

    except Exception as e:
        print(f"❌ Hata: {e}")
        raise HTTPException(status_code=500, detail=str(e))