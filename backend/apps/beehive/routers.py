from typing import Any
from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from .models import BehiveModel, UpdateBehiveModel

router = APIRouter()


class BehiveOut(BaseModel):
    id: str
    name: str


@router.post("/", response_description="Add new behive")
async def create_behive(request: Request, behive: BehiveModel = Body(...)):
    behive = jsonable_encoder(behive)
    new_behive = await request.app.mongodb["behives"].insert_one(behive)
    created_behive = await request.app.mongodb["behives"].find_one({
        "_id": new_behive.inserted_id
    })

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=to_behive_out(created_behive))


@router.get("/", response_description="List all behives", response_model=list[BehiveOut])
async def list_behives(request: Request):
    # TODO only show user behive
    return [to_behive_out(doc) for doc in await request.app.mongodb["behives"].find().to_list(length=100)]


@router.get("/{id}", response_description="Get a single behive")
async def show_behive(id: str, request: Request):
    # TODO add auth middleware
    # TODO return behive metrics
    if (behive := await request.app.mongodb["behives"].find_one({"_id": id})) is not None:
        return to_behive_out(behive)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Behive {id} not found")


@router.put("/{id}", response_description="Update a behive", response_model=BehiveOut)
async def update_task(id: str, request: Request, behive: UpdateBehiveModel = Body(...)):
     # TODO add auth middleware
    behive_update = {k: v for k, v in behive.dict().items() if v is not None}

    if len(behive_update) >= 1:
        update_result = await request.app.mongodb["behives"].update_one({"_id": id}, {"$set": behive_update})

        if update_result.modified_count == 1 and (
            updated_task := await request.app.mongodb["behives"].find_one({"_id": id})
        ) is not None:
            return to_behive_out(updated_task)

    if (existing_behive := await request.app.mongodb["behives"].find_one({"_id": id})) is not None:
        return to_behive_out(existing_behive)

    raise HTTPException(status_code=404, detail=f"Behive {id} not found")


def to_behive_out(behive: Any) -> BehiveOut:
    return BehiveOut(
        id=behive["_id"],
        name=behive["name"]
    )
