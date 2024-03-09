from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from src.schemas.user import User, UserCreate
from src.schemas.user_roles import UserRolesPatch
from src.services import repository
from src.services.database import get_db
from src.utils.exceptions import is_business_logic_exception, UserNotFoundException
from src.utils.json_response import PrettyJSONResponse

users_router = APIRouter()


@users_router.get("/users", response_model=list[User], response_class=PrettyJSONResponse)
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        users = repository.get_users(db, skip=skip, limit=limit)
        return users
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@users_router.get("/users/{user_id}", response_model=User, response_class=PrettyJSONResponse)
async def get_user(user_id: UUID, db: Session = Depends(get_db)):
    try:
        user = repository.get_user(db, user_id)
        return user
    except Exception as e:
        http_status_code = HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(e, UserNotFoundException):
            http_status_code = HTTP_404_NOT_FOUND

        raise HTTPException(status_code=http_status_code, detail=str(e))


@users_router.post("/users", status_code=201, response_class=PrettyJSONResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        repository.create_user(db, user)
    except Exception as e:
        http_status_code = HTTP_400_BAD_REQUEST if is_business_logic_exception(e) else HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code=http_status_code, detail=str(e))

    return {"message": "User successfully created."}


@users_router.patch("/users/{user_id}/roles", status_code=200, response_class=PrettyJSONResponse)
async def update_user_roles(user_id: UUID, user_roles: UserRolesPatch, db: Session = Depends(get_db)):
    try:
        repository.update_user_roles(db, user_id, user_roles)
    except Exception as e:
        http_status_code = HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(e, UserNotFoundException):
            http_status_code = HTTP_404_NOT_FOUND
        elif is_business_logic_exception(e):
            http_status_code = HTTP_400_BAD_REQUEST

        raise HTTPException(status_code=http_status_code, detail=str(e))

    return {"message": "User successfully created."}


@users_router.delete("/users/{user_id}", status_code=200, response_class=PrettyJSONResponse)
async def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    try:
        repository.delete_user(db, user_id)
    except Exception as e:
        http_status_code = HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(e, UserNotFoundException):
            http_status_code = HTTP_404_NOT_FOUND

        raise HTTPException(status_code=http_status_code, detail=str(e))

    return {"message": "User successfully deleted."}
