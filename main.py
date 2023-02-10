from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
def index():
    return {'message': 'Hello, Sir,'}

@app.get('/Welcome')
def get_name(name: str):
    return {'Welcome to my Project':f'{name}'}

if __name__ == '__main__':
    uvicorn.run(app, host ='127.0.0.1',port=8000)