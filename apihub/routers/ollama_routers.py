from fastapi import APIRouter, HTTPException, Depends, status, Request
import os, json, re
import httpx
import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from sqlalchemy.future import select
from models import OllamaModel, TaskModel
from schema import TaskSchema
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
OLLAMA_URL = os.getenv("OLLAMA_URL")

# Get all Ollama Models
@router.get("/models", tags=["Ollama"], summary="Get all Ollama Models")
async def get_ollama_models(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(OllamaModel))
        models = result.scalars().all()
        if not models:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No found any models")
        return models
    except Exception as e:
        logging.error(f"Error fetching models: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get models list",
            headers={"X-Error": str(e)}
        )

# @router.post("/pull", tags=["Ollama"], summary="Pull Ollama Model from Ollama", status_code=status.HTTP_201_CREATED)
# async def pull_ollama_model(name: str, db: AsyncSession = Depends(get_db)):
#     # Check if a chatbot with the same name already exists
#     existing_model = await db.execute(select(OllamaModel).where(OllamaModel.name == name))
#     existing_model = existing_model.scalars().first()
#     if existing_model:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Model with the same name already exists"
#         )
#     new_model = OllamaModel(
#                 name=name, 
#             )
#     async with httpx.AsyncClient(timeout=30.3) as client:
#         try:
#             response = await client.post(f"{OLLAMA_URL}/api/pull",json={"name":name})
#             if "error" in response.text:
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     detail="Model is not exists"
#                 )
#             try:
#                 db.add(new_model)
#                 await db.commit()
#                 await db.refresh(new_model)
#                 return new_model
#             except Exception as e:
#                 await db.rollback()
#                 logging.error(f"Error creating chatbot: {str(e)}")
#                 raise HTTPException(
#                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                     detail="Failed to create chatbot",
#                     headers={"X-Error": str(e)}
#                 )
#         except HTTPException as e:
#             raise e
    

@router.post("/pull", tags=["Ollama"], summary="Pull Ollama Model from Ollama", status_code=status.HTTP_201_CREATED)
async def pull_ollama_model(name: str, db: AsyncSession = Depends(get_db)):
    existing_model = await db.execute(select(OllamaModel).where(OllamaModel.name == name))
    if existing_model.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Model with the same name already exists"
        )
    new_model = OllamaModel(name=name)
    async with httpx.AsyncClient(timeout=30.3) as client:
        response = await client.post(f"{OLLAMA_URL}/api/pull", json={"name": name})
        if response.status_code != 200 or "error" in response.text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Model does not exist in Ollama"
            )
    try:
        db.add(new_model)
        await db.commit()
        await db.refresh(new_model)
        return new_model
    except Exception as e:
        await db.rollback()
        logging.error(f"Error dowload model: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to download model",
            headers={"X-Error": str(e)}
        )

@router.post("/task", tags=["Ollama"], summary="Give a Simple Task to a Model")
async def give_task(data: TaskSchema, db: AsyncSession = Depends(get_db)):
                    async with httpx.AsyncClient(timeout=60.0) as client:
                        try:
                            await client.post(f"{OLLAMA_URL}/api/generate", json=data.dict())
                            new_task = TaskModel(
                                 name = data.model,
                                 task = data.prompt,
                            )
                            try:
                                db.add(new_task)
                                await db.commit()
                                await db.refresh(new_task)
                                return new_task
                            except Exception as e:
                                await db.rollback()
                                logging.error(f"Error dowload model: {str(e)}")
                                raise HTTPException(
                                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Failed to download model",
                                    headers={"X-Error": str(e)}
                                )
                        except HTTPException as e:
                            raise e
                        except Exception as e:
                            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
