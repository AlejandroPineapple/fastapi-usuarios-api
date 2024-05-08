from fastapi import FastAPI, HTTPException
from db.db import client
import uvicorn
from controller.usuarioCRUD import router as usuarios_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios_router, tags=["usuarios"], prefix="/usuarios")
# MongoDB connection URL
@app.on_event("shutdown")
def shutdown_db_client():
    client.close()



