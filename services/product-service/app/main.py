from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import products

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Product Service",
    description="Manages the product catalog for Microshop",
    version="0.1.0",
)

app.include_router(products.router)


@app.get("/")
def root():
    return {"service": "product-service", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "product-service"}