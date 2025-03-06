from dotenv import load_dotenv
import os
from fastapi import FastAPI

from app.controller.auth_controller import router as auth_router
from app.controller.category_controller import router as category_router
from app.controller.product_controller import router as product_router


app = FastAPI(title="API Food Market")
load_dotenv()

print(f"MONGODB_URL from os: {os.getenv('MONGODB_URL')}")
app.include_router(auth_router)
app.include_router(category_router)

app.include_router(product_router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",port=8000,reload=True)


