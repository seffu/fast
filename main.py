from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# @app.get('/')
# def index():
#     return {'name':'Seffu'}

# @app.get('/about')
# def about():
#     return {'about':'About the Page'}

# @app.get('/')
@app.get('/blogs')#without params
# @app.get('/blogs?skip=0&limit=10&published=true') #skip 0 and get 10 published blogs the default values are 0 for skip and 10 for limit
# def index(limit,published):#without default values
def index(limit=10,published:bool=True,sort:Optional[str]=None):#with default values
    # return {'data':'bloglist'}
    if published:
        return {'data': f'limit is {limit} published items'}
    else:
        return {'data': f'limit is {limit} items'}

#make sure dynamic routes are after static routes
@app.get('/blog/unpublished')
def unpublished():
    return {'data':'all unpublished blogs'}

@app.get('/blog/{id}')
# def show(id):
def show(id:int): #define the type to make sure only integer value is allowed
    return {'data':id}

@app.get('/blog/{id}/comments')
def comments(id):
    return {'data':{"1","2"}}

class Blog(BaseModel):
    title:str
    body:str
    published:Optional[bool]

@app.post('/blogs')
def create_blog(blog:Blog):
    return {'data':'Blog is created'}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)