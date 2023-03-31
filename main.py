from typing import Union

import requests
import random
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/favicon.ico")
def favicon():
    return RedirectResponse(url="https://qsim.top/favicon.ico", status_code=301)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/ip")
def get_ip_details(request: Request):
    ip_address = request.client.host
    return {"client_ip": ip_address}


def get_bing_images(num_days):
    url = f"https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n={num_days}&mkt=en-US"
    response = requests.get(url)
    data = response.json()
    images = [(f"https://www.bing.com{image['url']}", image['title']) for image in data['images']]
    return images


@app.get("/bing")
def bing_image(day: int = 0, randomize: bool = False, json: bool = False):
    """
    Get the Bing daily image for a specific day, or a random day.
    """
    images = get_bing_images(7)
    num_images = len(images)
    if randomize:
        random_day = random.randint(0, num_images - 1)
        image_url, image_desc = images[random_day]
    elif json:
        # 有问题
        image_url, image_desc = images[0]
        return {"url": image_url, "description": image_desc}
    else:
        day = max(0, min(day, num_images - 1))
        image_url, image_desc = images[day]
    return RedirectResponse(url=image_url, status_code=301, headers={"Content-Disposition": f"inline; filename={image_desc}.jpg"})
