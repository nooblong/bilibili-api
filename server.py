import inspect
import sys

import httpx
from sanic import Sanic, json
from bilibili_api import *
from bilibili_api.channel_series import ChannelSeriesType, ChannelOrder
from bilibili_api.comment import CommentResourceType
from bilibili_api.search import SearchObjectType

app = Sanic("SimpleNetworkAccess")


@app.get("/<package:str>/<clazz:str>/<func:str>")
async def req_by_clazz(request, package, clazz, func):
    package_attr = getattr(sys.modules[__name__], package)
    clazz_attr = getattr(package_attr, clazz)
    clazz_params = inspect.signature(clazz_attr).parameters
    cred_obj = None
    cred_dict = dict()
    clazz_dict = dict()
    for i in request.args:
        if i == "sessdata" or i == "bili_jct" or i == "buvid3" or i == "ac_time_value":
            cred_dict[i] = request.args[i][0]
            # continue
        if i in clazz_params.keys():
            clazz_dict[i] = request.args[i][0]

    special_param(clazz_dict, clazz)

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

    special_param(func_dict, func)

    if inspect.isasyncgenfunction(func_attr) or inspect.iscoroutinefunction(func_attr):
        result = await func_attr(**func_dict)
    else:
        result = func_attr(**func_dict)
    return json(result)


@app.get("/<package:str>/<func:str>")
async def req_by_static(request, package, func):
    package_attr = getattr(sys.modules[__name__], package)
    func_attr = getattr(package_attr, func)
    func_params = inspect.signature(func_attr).parameters
    cred_obj = None
    cred_dict = dict()
    func_dict = dict()

    for i in request.args:
        if i == "sessdata" or i == "bili_jct" or i == "buvid3" or i == "ac_time_value":
            cred_dict[i] = request.args[i][0]
            # continue
        if i in func_params:
            func_dict[i] = request.args[i][0]

    if cred_dict:
        cred_obj = Credential(**cred_dict)

    if package == "Credential":
        func_attr = getattr(cred_obj, func)

    if "credential" in func_params.keys():
        func_dict["credential"] = cred_obj

    special_param(func_dict, package)

    if inspect.isasyncgenfunction(func_attr) or inspect.iscoroutinefunction(func_attr):
        result = await func_attr(**func_dict)
    else:
        result = func_attr(**func_dict)

    return json(result)


@app.get("addListener/<package:str>/<clazz:str>/<event_type:str>")
async def add_listener(request, package, clazz, event_type):
    call_back_url = request.args["url"][0]
    del request.args["url"]
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
    func_attr = getattr(clazz_obj, "add_event_listener")

    async def call_back(event):
        httpx.post(call_back_url, json=event.__dict__)
        print("event: ", event)

    func_dict["name"] = event_type
    func_dict["handler"] = call_back
    func_attr(**func_dict)
    run = getattr(clazz_obj, "run")
    asyncio.create_task(run())
    return json({"result": "ok"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, dev=False)

    # 生成一个 Credential 对象
    # credential = Credential(sessdata="",
    #                         bili_jct="", ac_time_value="")
    #
    # # 检查 Credential 是否需要刷新
    # print(sync(credential.check_refresh()))
    #
    # print(sync(credential.check_valid()))
    #
    # # 刷新 Credential
    # # sync(credential.refresh())
    #
    # print(credential.ac_time_value)
    # print(credential.sessdata)
    # print(credential.bili_jct)
    # print(credential.buvid3)


def special_param(param_map, function_name):
    # 处理评论
    if function_name.lower() == "comment" and "type_" in param_map:
        val = int(param_map["type_"])
        obj = CommentResourceType(val)
        param_map["type_"] = obj

    if function_name.lower() == "search_by_type" and "search_type" in param_map:
        val = int(param_map["search_type"])
        obj = SearchObjectType(val)
        param_map["search_type"] = obj

    if function_name.lower() == "channelseries" and "type_" in param_map:
        val = int(param_map["type_"])
        obj = ChannelSeriesType(val)
        param_map["type_"] = obj

    if function_name.lower() == "get_videos" and "sort" in param_map:
        val = (param_map["sort"])
        obj = ChannelOrder(val)
        param_map["sort"] = obj
