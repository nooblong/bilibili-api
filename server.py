import inspect
import sys

from sanic import Sanic, json
from bilibili_api import *

app = Sanic("SimpleNetworkAccess")


@app.get("/<package:str>/<clazz:str>/<func:str>")
async def reqByClazz(request, package, clazz, func):
    package_attr = getattr(sys.modules[__name__], package)
    clazz_attr = getattr(package_attr, clazz)
    clazz_params = inspect.signature(clazz_attr).parameters
    cred_obj = None
    cred_dict = dict()
    clazz_dict = dict()
    for i in request.args:
        if i == "sessdata" or i == "bili_jct" or i == "buvid3":
            cred_dict[i] = request.args[i][0]
            continue
        if i in clazz_params.keys():
            clazz_dict[i] = request.args[i][0]

    if cred_dict:
        cred_obj = Credential(**cred_dict)

    if "credential" in clazz_params.keys():
        clazz_dict["credential"] = cred_obj

    func_dict = dict()
    clazz_obj = clazz_attr(**clazz_dict)
    func_attr = getattr(clazz_obj, func)
    func_params = inspect.signature(func_attr).parameters

    if "credential" in func_params.keys():
        func_dict["credential"] = cred_obj

    for i in request.args:
        if i in func_params.keys():
            func_dict[i] = request.args[i][0]

    result = await func_attr(**func_dict)
    return json(result)


@app.get("/<package:str>/<func:str>")
async def reqByStatic(request, package, func):
    package_attr = getattr(sys.modules[__name__], package)
    func_attr = getattr(package_attr, func)
    func_params = inspect.signature(func_attr).parameters
    cred_obj = None
    cred_dict = dict()
    func_dict = dict()

    for i in request.args:
        if i == "sessdata" or i == "bili_jct" or i == "buvid3":
            cred_dict[i] = request.args[i][0]
            continue
        if i in func_params:
            func_dict[i] = request.args[i][0]

    if cred_dict:
        cred_obj = Credential(**cred_dict)

    if "credential" in func_params.keys():
        func_dict["credential"] = cred_obj

    result = await func_attr(**func_dict)
    return json(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, dev=True)
