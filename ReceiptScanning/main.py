import asyncio
import uvicorn
from fastapi import FastAPI
app = FastAPI()

async def start_api():
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8000,
        loop="asyncio",
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(start_api())
