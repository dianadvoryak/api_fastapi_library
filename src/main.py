from fastapi import FastAPI

from library.router import router as router_library

app = FastAPI(
    title="Book App"
)

app.include_router(router_library)
