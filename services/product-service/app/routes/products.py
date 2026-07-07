from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from app.database import get_db
from app.cache import get_redis, CACHE_TTL
from app.schemas import ProductCreate, ProductUpdate, ProductResponse
from app import crud

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

PRODUCTS_CACHE_KEY = "products:all"


@router.get("/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    r = get_redis()
    cached = r.get(PRODUCTS_CACHE_KEY)
    if cached:
        return json.loads(cached)
    products = crud.get_products(db, skip=skip, limit=limit)
    products_data = [ProductResponse.from_orm(p).model_dump() for p in products]
    r.setex(PRODUCTS_CACHE_KEY, CACHE_TTL, json.dumps(products_data, default=str))
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id=product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    r = get_redis()
    r.delete(PRODUCTS_CACHE_KEY)
    return crud.create_product(db=db, product=product)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    r = get_redis()
    r.delete(PRODUCTS_CACHE_KEY)
    updated = crud.update_product(db=db, product_id=product_id, product=product)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return updated


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    r = get_redis()
    r.delete(PRODUCTS_CACHE_KEY)
    deleted = crud.delete_product(db=db, product_id=product_id)
    if deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )