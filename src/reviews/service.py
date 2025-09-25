from src.db.models import Review
from sqlmodel import SQLModel, select, desc
from src.books.service import BookService
from src.auth.service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreateModel
from fastapi.exceptions import HTTPException
from fastapi import status


book_service = BookService()
user_service = UserService()

class ReviewService:

    async def add_review_to_book(self, user_email: str, book_uid: str, review_data: ReviewCreateModel, session: AsyncSession):
        
        try:
            book = await book_service.get_book(book_uid, session)
            user = await user_service.get_user_by_email(user_email, session)

            review_data_dict = review_data.model_dump()
            new_review = Review(
                **review_data_dict
            )

            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found"
                )
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )


            new_review.user = user
            new_review.book = book

            session.add(new_review)

            await session.commit()

            return new_review

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Oops.. Something went wrong"
            )
        
    async def get_review_by_uid(self, review_uid: str, session: AsyncSession):
        statement = select(Review).where(Review.uid == review_uid)

        result = await session.exec(statement)

        review = result.first()
        
        return review if review is not None else None
    

    async def get_all_review(self, session: AsyncSession):
        statement = select(Review).order_by(desc(Review.created_at))

        result = await session.exec(statement)
        
        return result.all()
    

    async def delete_review(self, review_uid: str, user_email:str, session: AsyncSession):

        review = await self.get_review_by_uid(review_uid, session)
        user = await user_service.user_exists(user_email, session)

        if not review and (review.user != user):

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot delete this review"
            )
        
        await session.delete(review)

        await session.commit()

        return {}