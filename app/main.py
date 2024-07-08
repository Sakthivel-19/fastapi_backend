from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test")
def read_root():
    return {"Hello": "Test World"}

@app.get("/try")
def read_root():
    return {"Hello": "Try World"}

@app.get("/work")
def read_root():
    return {"Hello": "Work World"}