from fastapi import FastAPI

app = FastAPI(
    title="Product Service",
    description="Manages the product catalog for Microshop",
    version="0.1.0",
)

@app.get("/")
def root():
    return {"service":"product-service", "status":"running"}


@app.get("/health")
def health():
    return {"status":"healthy", "service":"product-service"}