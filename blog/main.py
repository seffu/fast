from fastapi import FastAPI,Depends,status,Response,HTTPException
from sqlalchemy.orm import Session
from . import schemas,models,database

app = FastAPI()

models.Base.metadata.create_all(database.engine)


def get_db_session():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.post('/blogs',status_code=201)
@app.post('/blogs',status_code=status.HTTP_201_CREATED)#status using the status package
def create(request:schemas.Blog,db:Session = Depends(get_db_session)):
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blogs')
def all(db:Session = Depends(get_db_session)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=200)
def show(id,response:Response,db:Session = Depends(get_db_session)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details':'Does not exist'}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail='Does not exist')
    return blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,response:Response,db:Session = Depends(get_db_session)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail='Blog not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'Complete'

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request:schemas.Blog,db:Session = Depends(get_db_session)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail='Blog not found')
    blog.update(request)
    db.commit()
    return 'updated'