from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import create_session
from ..models import User,Blogs
from ..oauth import get_current_user
from ..schemas import BlogCreate,ShowUsers

router = APIRouter(tags=['Blogs'])

#blog routes
@router.post('/blogs/{user_id}')
def create_blog(blog: BlogCreate, user_id:int, session: Session=Depends(create_session),get_current_user: User =Depends(get_current_user)):
    if (user_id!=get_current_user.id):
        raise HTTPException(status_code=404,detail="Not authenticated")
    new_blog=Blogs(
        title=blog.title,
        content=blog.content,
        user_id=user_id
    )
    session.add(new_blog)
    session.commit()
    session.refresh(new_blog)
    return {"message":"blog created"}


@router.get('/blogs',response_model=List[ShowUsers])
def get_all_blogs(session: Session=Depends(create_session),get_current_user: User =Depends(get_current_user)):
    blogs=session.query(User).all()
    return blogs


@router.get('/blogs/{user_id}',response_model=List[ShowUsers])
def get_user_blogs(user_id: int,session:Session=Depends(create_session),get_current_user: User =Depends(get_current_user)):
    blogs=session.query(User).filter(User.id==user_id).all()
    return blogs

@router.delete('/blogs/{blog_id}')
def delete_blog(blog_id: int, session: Session=Depends(create_session),get_current_user: User =Depends(get_current_user)):
    blog=session.query(Blogs).filter(Blogs.id==blog_id).first()
    if not blog:
        raise HTTPException(status_code=404,detail="blog not found")
    if (blog.user_id!=get_current_user.id):
        raise HTTPException(status_code=404,detail="Not authenticated")
    session.delete(blog)
    session.commit()
    return {"message": "blog deleted"}

@router.put('/blogs/{blog_id}')
def update_blog(blog:BlogCreate,blog_id: int, session:Session=Depends(create_session),get_current_user: User =Depends(get_current_user)):
    current_blog=session.query(Blogs).filter(Blogs.id==blog_id).first()
    for key,value in blog.dict().items():
        setattr(current_blog,key,value)
    
    session.commit()
    session.refresh(current_blog)
    return {"message": "blog updated"}