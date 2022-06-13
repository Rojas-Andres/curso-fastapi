from fastapi import FastAPI 
import uvicorn 
from app.db.database import Base,engine
from app.routers import user,auth

app = FastAPI()
app.include_router(user.router)

app.include_router(auth.router)

if __name__=="__main__":
    uvicorn.run("main:app",port=8000,reload=True)