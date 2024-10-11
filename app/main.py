from fastapi import FastAPI
from prometheus_client import Counter, generate_latest

app = FastAPI()

REQUEST_COUNT = Counter('request_count', 'App Request Count', ['method', 'endpoint'])

@app.middleware("http")
async def prometheus_middleware(request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    return response

@app.get("/metrics")
async def metrics():
    return generate_latest()
    
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
