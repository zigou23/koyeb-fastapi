from typing import Union

# 运行 python -m uvicorn main:app --reload  --no-use-colors
import requests
import random
import platform # 获取系统类型/user
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()


@app.get("/")
async def read_root():
    return ["ip", "bing"]

# get icon
@app.get("/favicon.ico")
async def favicon():
    return RedirectResponse(url="https://qsim.top/favicon.ico", status_code=301)


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/user")
async def get_user_message(request: Request):
    headers = request.headers
    ip = request.client.host
    ua = request.headers.get("User-Agent")
    platforms = platform.uname()
    platform_list = ["system", "node", "release", "version", "machine", "processor"]
    platform_msg = {key: value for key, value in zip(platform_list, platforms)}
    return jsonable_encoder({
        "headers": headers,
        "method": request.method,
        "url": str(request.url),
        "ip":ip,
        "platform": platform_msg
        })

# bing_image start
def get_bing_images(num_days):
    mkt = ['de-DE', 'en-CA', 'en-GB', 'en-IN', 'en-US', 'fr-FR', 'it-IT', 'ja-JP', 'zh-CN']
    bing_url = "https://bing.com"
    url_api = f"/HPImageArchive.aspx?format=js&idx=0&n={num_days}&mkt={mkt[4]}"
    response = requests.get(bing_url + url_api)
    data = response.json()
    images = data["images"]
    for i in images:  # i 值为 data["images"][j]
        i["url"] = bing_url + i["url"]
        i["quiz"] = bing_url + i["quiz"]
        # 从字典{}中 删除的对象
        keys_to_remove = ["startdate", "fullstartdate", "drk", "top", "bot", "hs"]
        for remove_key in keys_to_remove:
            i.pop(remove_key, None)

        i["date"] = i.pop("enddate") # 更改enddate为date
    
    return images


@app.get("/bing")
def bing():
    return ["/bing/img", "/bing/img/(0-7)", "/bing/json"]

# bing/img(0-7)
# bing/img/random
# bing/json
@app.get("/bing/{subpath:path}")
def bing_image_all(subpath: str):
    images = get_bing_images(8)
    #/bing/img时,返回图片地址
    if subpath == "img":
        image_url = "https://bing.com" + images[0]["urlbase"] + "_1920x1080.jpg"
        return RedirectResponse(url=image_url, status_code=301)
    #path 以img/开始
    elif subpath.startswith("img/"):
        subpath_parts = subpath.split("/") # ["img", "path"] subpath_parts[1]="path"
        # if subpath_parts[1] !== "random" or 0 < int(subpath_parts[1]) < 7:
        #     return 0
        try:
            if subpath_parts[1] == "random":
                random_num = random.randint(0, 7)
                image_url = "https://bing.com" + images[int(random_num)]["urlbase"] + "_1920x1080.jpg"
                return RedirectResponse(url=image_url, status_code=301)
            elif 0 < int(subpath_parts[1]) < 7:
                image_url = "https://bing.com" + images[int(subpath_parts[1])]["urlbase"] + "_1920x1080.jpg"
                return RedirectResponse(url=image_url, status_code=301)
            else:
                return "0-7"
        except:
            return "error"
    #返回json格式
    elif subpath == "json":
        return images
    else:
        return "/bing"
# bing_image end


