from fastapi import FastAPI,status,HTTPException,Response,Depends,APIRouter
from typing import List,Optional
from sqlalchemy.orm import Session
from .. import models,schemas
from .. import oauth2
from ..database import get_db

router=APIRouter(prefix="/posts",tags=["Posts"])

@router.get("/",response_model=List[schemas.Post])
def get_posts(db:Session=Depends(get_db),curr_user:int=Depends(oauth2.get_current_user),limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""select * from posts""")
    # posts=cursor.fetchall()
    posts= db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    if not posts:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db:Session=Depends(get_db),curr_user:int=Depends(oauth2.get_current_user)) :
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title, post.content, post.published))
    # new_post = cursor.fetchone(),
    # conn.commit()
    new_post = models.Posts(owner_id=curr_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.Post)
def get_post(id: int,db:Session=Depends(get_db),curr_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * from posts WHERE id = %s""",(str(id)))
    # test_post = cursor.fetchone()
    test_post=db.query(models.Posts).filter(models.Posts.id==id).first()
    if not test_post:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return test_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session=Depends(get_db),curr_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""" ,(str(id)))
    # deleted_post = cursor.fetchone()
    deleted_post=db.query(models.Posts).filter(models.Posts.id==id)
    if deleted_post.first()== None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} does not exist")
    if deleted_post.first().owner_id != curr_user.id:
        raise HTTPException (status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Not authorized to Delete Posts {id}")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostUpdate,db:Session=Depends(get_db),curr_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s RETURNING *""",(post.title, post.content, post.published))
    # updated_post = cursor.fetchone()
    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()



