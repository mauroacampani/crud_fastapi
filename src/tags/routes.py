from fastapi import HTTPException, status, APIRouter, Depends
from .schemas import TagModel, TagCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from .service import TagService
from typing import List


tags_router = APIRouter()

tag_service = TagService()

user_role_checker = Depends(RoleChecker(["user", "admin"]))


@tags_router.get('/', response_model=List[TagModel], dependencies=[user_role_checker])
async def get_tags(session: AsyncSession = Depends(get_session)):

    tags = await tag_service.get_all_tags(session)

    return tags


@tags_router.get('/{tag_uid}', response_model=TagModel, dependencies=[user_role_checker])
async def get_tag(tag_uid: str, session: AsyncSession = Depends(get_session)):

    tag = await tag_service.get_tag_by_uid(tag_uid=tag_uid, session=session)

    if tag:
        return tag
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Tag no encontrado"
    )


@tags_router.post('/', status_code=status.HTTP_201_CREATED, response_model=TagModel, dependencies=[user_role_checker])
async def create_tag(tag_data: TagCreateModel, session: AsyncSession = Depends(get_session)) -> TagModel:

    new_tag = await tag_service.create_tag(tag_data=tag_data, session=session)

    return new_tag


@tags_router.put('/{tag_uid}', response_model=TagModel, dependencies=[user_role_checker])
async def update_tag(tag_uid: str, tag_data: TagCreateModel, session: AsyncSession = Depends(get_session)):

    tag = await tag_service.update_tag(tag_uid=tag_uid, tag_data=tag_data, session=session)

    return tag


@tags_router.delete('/{tag_uid}', dependencies=[user_role_checker])
async def update_tag(tag_uid: str, session: AsyncSession = Depends(get_session)):

    tag = await tag_service.delete_tag(tag_uid=tag_uid, session=session)

    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    else:
        return {}