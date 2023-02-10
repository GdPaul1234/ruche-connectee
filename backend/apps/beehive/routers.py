from fastapi import APIRouter, Depends, Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder

from .models import BehiveOut, CreateBehiveModel, UpdateBehiveModel, to_behive_out

from apps.user.auth import User, get_current_active_user

router = APIRouter()


def get_behives_db(request: Request):
    return request.app.mongodb["behives"]


def get_mongo_db_client(request: Request):
    return request.app.mongodb_client


@router.post("/", response_description="Add new behive", status_code=status.HTTP_201_CREATED, response_model=BehiveOut)
async def create_behive(
    *,
    current_user: User = Depends(get_current_active_user),
    behive: CreateBehiveModel = Body(...),
    request: Request,
):
    behives_db = get_behives_db(request)
    mock_metrics = {k: { "value": "Not set", "unit": None } for k in ("temperature", "humidity", "weight", "battery", "alert" )}
    behive = jsonable_encoder(behive.dict() | {"owner_id": current_user.id, "last_metrics": mock_metrics})

    async with await get_mongo_db_client(request).start_session() as s:
        async with s.start_transaction():
            new_behive = await behives_db.insert_one(behive, session=s)
            created_behive = await behives_db.find_one({"_id": new_behive.inserted_id}, session=s)

            return to_behive_out(created_behive)


@router.get("/", response_description="List all your behives", response_model=list[BehiveOut])
async def list_behives(
    *,
    current_user: User = Depends(get_current_active_user),
    request: Request
):
    behives_db = get_behives_db(request)
    return [
        to_behive_out(doc)
        for doc in await behives_db
            .find({"owner_id": current_user.id})
            .to_list(length=100)
    ]


@router.get("/{id}", response_description="Get a single behive", response_model=BehiveOut)
async def show_behive(
    *,
    current_user: User = Depends(get_current_active_user),
    request: Request,
    id: str
):
    behives_db = get_behives_db(request)

    if (behive := await behives_db.find_one({"_id": id, "owner_id": current_user.id})) is not None:
        return to_behive_out(behive)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Behive {id} not found")


@router.put("/{id}", response_description="Update a behive", response_model=BehiveOut)
async def update_behive(
    *,
    current_user: User = Depends(get_current_active_user),
    request: Request,
    id: str,
    behive: UpdateBehiveModel = Body(...)
):
    behive_update = {k: v for k, v in behive.dict().items() if v is not None}
    behives_db = get_behives_db(request)

    async with await get_mongo_db_client(request).start_session() as s:
        async with s.start_transaction():
            if len(behive_update) >= 1:
                update_result = await behives_db.update_one(
                    {"_id": id, "owner_id": current_user.id},
                    {"$set": behive_update},
                    session=s
                )

                if update_result.modified_count == 1 and (
                    updated_behive := await behives_db.find_one({"_id": id, "owner_id": current_user.id}, session=s)
                ) is not None:
                    return to_behive_out(updated_behive)

            if (existing_behive := await behives_db.find_one({"_id": id, "owner_id": current_user.id}, session=s)) is not None:
                return to_behive_out(existing_behive)

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Behive {id} not found")


@router.delete("/{id}", response_description="Delete behive", status_code=status.HTTP_204_NO_CONTENT)
async def delete_behive(
    *,
    current_user: User = Depends(get_current_active_user),
    request: Request,
    id: str
):
    behives_db = get_behives_db(request)
    delete_result = await behives_db.delete_one({"_id": id, "owner_id": current_user.id})

    if delete_result.deleted_count == 1:
        return {}

    raise HTTPException(status_code=404, detail=f"Behive {id} not found")
