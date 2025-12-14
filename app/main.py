from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.assistant_router import router as assistant_router
from app.routers.document_router import router as document_router
from app.routers.dataset_router import router as dataset_router
from app.routers.auth_router import router as auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/helath")
def health_check():
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(dataset_router)
app.include_router(document_router)
app.include_router(assistant_router)