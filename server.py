from sanic import Sanic
from sanic.response import text
import asyncio

import bilibili_api.video
from bilibili_api import *

app = Sanic("MyHelloWorldApp")


@app.get("/<i>/<j>")
async def hello_world(request, i, j):
    print(i)
    print(j)
    print(type("video", (object, ), {}))
    clazz = type("bilibili_api.video.Video", (), dict(bvid="asd1"))
    print(hasattr(clazz, "get_info"))
    print(clazz())
    print(bilibili_api.video.Video)
    return text("Hello, world.")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, dev=True)
