from fastapi import FastAPI
from routes import router
import uvicorn
from contextlib import asynccontextmanager
from app.clients import RedisClient,LLMClient,EmbeddingClient
app = FastAPI(title="Fashion Assistant", version="1.0")

app.include_router(router, prefix="")

@asynccontextmanager
async def lifespan(app: FastAPI):
    async def startup():
        RedisClient.initialize(host="localhost", port=6379, db=0)

        LLMClient.initialize(model_name="models/gemini-1.5-flash")

        EmbeddingClient.initialize(model_name="models/text-embedding-004")
        print("Clients initialized successfully.")

    async def shutdown():
        print("Shutting down clients.")

    yield startup, shutdown

app = FastAPI(lifespan=lifespan(app))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)