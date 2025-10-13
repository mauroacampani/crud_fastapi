from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreateModel, ReviewModel
from src.db.models import User
from .service import ReviewService
from src.auth.dependencies import get_current_user, RoleChecker
from typing import List

review_service = ReviewService()

review_router = APIRouter()

admin_role_checker = Depends(RoleChecker(["admin"]))
user_role_checker = Depends(RoleChecker(["user", "admin"]))


@review_router.get('/', response_model=List[ReviewModel], dependencies=[user_role_checker])
async def get_all_reviews(session: AsyncSession = Depends(get_session)):
    
    reviews = await review_service.get_all_review(session=session)

    return reviews


@review_router.get('/{review_uid}', dependencies=[user_role_checker])
async def get_review_by_uid(review_uid: str, session: AsyncSession = Depends(get_session)):
    
    review = await review_service.get_review_by_uid( review_uid=review_uid, session=session)

    if review:
        return review
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    

@review_router.post('/book/{book_uid}', dependencies=[user_role_checker])
async def add_review_to_book(book_uid: str, review_data: ReviewCreateModel, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    
    new_review = await review_service.add_review_to_book(user_email=current_user.email, book_uid=book_uid, review_data=review_data, session=session)

    return new_review


@review_router.delete('/{review_uid}', dependencies=[user_role_checker])
async def delete_review(review_uid: str, curremt_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    
    await review_service.delete_review(review_uid=review_uid, user_email= curremt_user.email, session=session)

    return {}



