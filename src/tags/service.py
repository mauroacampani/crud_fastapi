from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Tag
from sqlmodel import select, desc
from fastapi import status, HTTPException
from .schemas import TagCreateModel


class TagService:

    async def get_all_tags(self, session: AsyncSession):

        statement = select(Tag).order_by(desc(Tag.created_at))

        result = await session.exec(statement)

        return result.all()
    

    async def get_tag_by_uid(self, tag_uid: str, session: AsyncSession):

        statement = select(Tag).where(Tag.uid == tag_uid)

        result = await session.exec(statement)

        return result.first()
    
        

    async def create_tag(self, tag_data: TagCreateModel, session: AsyncSession):

        tag_data_dict = tag_data.model_dump()

        new_tag = Tag(
            **tag_data_dict
        )
        print(tag_data_dict)
        session.add(new_tag)

        await session.commit()

        return new_tag
    

    async def update_tag(self, tag_uid: str, tag_data: TagCreateModel, session: AsyncSession):

        tag = await self.get_tag_by_uid(tag_uid, session)

        if tag:

            tag_data_dict = tag_data.model_dump()

            for k, v in tag_data_dict.items():
                setattr(tag, k, v)

            await session.commit()

            await session.refresh(tag)

            return tag
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag no encontado"
            )
        

    async def delete_tag(self, tag_uid: str, session: AsyncSession):

        tag = await self.get_tag_by_uid(tag_uid, session)

        if tag:

            await session.delete(tag)

            await session.commit()

            return {}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag no encontado"
            )