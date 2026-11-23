from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def check():
    return {'status': 'ok', 'message': 'Hello, World!'}
