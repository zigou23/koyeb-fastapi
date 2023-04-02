from typing import Union

from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/ip")
def get_ip_details(request: Request):
    ip_address = request.client.host
    return {"client_ip": ip_address}


    