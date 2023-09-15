import sys

from sanic import Sanic, json
from sanic.response import text
import asyncio

from bilibili_api import *

app = Sanic("MyHelloWorldApp")


@app.get("/<package:str>/<clazz:str>/<func:str>")
async def hello_world(request, package, clazz, func):
    arg = dict()
    for i in request.args:
        arg[i] = request.args[i][0]

    print(dir(sys.modules[__name__]))
    b = getattr(sys.modules[__name__], package)
    e = getattr(b, clazz)
    f = e(**arg)
    result = await getattr(f, func)()
    return json(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, dev=True)
