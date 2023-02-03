from fastapi import APIRouter, Depends, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import BehiveOut, CreateBehiveModel, UpdateBehiveModel, to_behive_out

from apps.user.auth import User, get_current_active_user

router = APIRouter()


@router.post("/", response_description="Add new behive", response_model=BehiveOut)
async def create_behive(*, current_user: User = Depends(get_current_active_user), request: Request, behive: CreateBehiveModel = Body(...)):
    mock_metrics = {k: { "value": "Not set", "unit": None } for k in ("temperature", "humidity", "weight", "battery", "alert" )}
    behive = jsonable_encoder(behive.dict() | {"owner_id": current_user.id, " metrics": mock_metrics})

    new_behive = await request.app.mongodb["behives"].insert_one(behive)
    created_behive = await request.app.mongodb["behives"].find_one({
        "_id": new_behive.inserted_id
    })

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=to_behive_out(created_behive))


@router.get("/", response_description="List all behives", response_model=list[BehiveOut])
async def list_behives(*, current_user: User = Depends(get_current_active_user), request: Request):
    return [
        to_behive_out(doc)
        for doc in await request.app.mongodb["behives"]
            .find({"owner_id": current_user.id})
            .to_list(length=100)
    ]


@router.get("/{id}", response_description="Get a single behive", response_model=BehiveOut)
async def show_behive(*, current_user: User = Depends(get_current_active_user), id: str, request: Request):
    # TODO add auth middleware
    if (behive := await request.app.mongodb["behives"].find_one({"_id": id, "owner_id": current_user.id})) is not None:
        return to_behive_out(behive)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Behive {id} not found")


@router.put("/{id}", response_description="Update a behive", response_model=BehiveOut)
async def update_task(*, current_user: User = Depends(get_current_active_user), id: str, request: Request, behive: UpdateBehiveModel = Body(...)):
    behive_update = {k: v for k, v in behive.dict().items() if v is not None}

    if len(behive_update) >= 1:
        update_result = await request.app.mongodb["behives"].update_one({"_id": id, "owner_id": current_user.id}, {"$set": behive_update})

        if update_result.modified_count == 1 and (
            updated_behive := await request.app.mongodb["behives"].find_one({"_id": id, "owner_id": current_user.id})
        ) is not None:
            return to_behive_out(updated_behive)

    if (existing_behive := await request.app.mongodb["behives"].find_one({"_id": id, "owner_id": current_user.id})) is not None:
        return to_behive_out(existing_behive)

    raise HTTPException(status_code=404, detail=f"Behive {id} not found")


@router.delete("/{id}", response_description="Delete behive")
async def delete_user(*, current_user: User = Depends(get_current_active_user), id: str, request: Request):
    delete_result = await request.app.db["behives"].delete_one({"_id": id, "owner_id": current_user.id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})

    raise HTTPException(status_code=404, detail=f"Behive {id} not found")
