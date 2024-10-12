from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Instrument Prometheus
Instrumentator().instrument(app).expose(app)
    
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

@app.get("/testing")
def read_root():
    return {"Hello": "Testing World"}

@app.get("/ansible")
def read_root():
    return {"Ansible": "Deployment using Ansible done successfully"}
