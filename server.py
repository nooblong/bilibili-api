import enum
import inspect
import sys

import httpx
from sanic import Sanic, json
from bilibili_api import *

app = Sanic("SimpleNetworkAccess")


def enum_to_value(obj):
    if isinstance(obj, enum.Enum):
        return obj.value
    elif isinstance(obj, dict):
        return {key: enum_to_value(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [enum_to_value(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return {key: enum_to_value(value) for key, value in vars(obj).items()}
    else:
        return obj


def parse_param(param_map):
    for key, value in param_map.items():
        if key == "credential":
            continue
        if ":parse" in value:
            process = value.replace(":parse", "")
            param_map[key] = eval(process)


@app.get("/<package:str>/<clazz:str>/<func:str>")
async def req_by_clazz(request, package, clazz, func):
    try:
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

        parse_param(clazz_dict)

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

        parse_param(func_dict)

        if inspect.isasyncgenfunction(func_attr) or inspect.iscoroutinefunction(func_attr):
            result = await func_attr(**func_dict)
        else:
            result = func_attr(**func_dict)
        result_no_enum = enum_to_value(result)

    except Exception as e:
        wrap_result = dict()
        wrap_result["code"] = -1
        wrap_result["message"] = str(e)
        return json(wrap_result)

    wrap_result = dict()
    wrap_result["code"] = 0
    wrap_result["data"] = result_no_enum
    return json(wrap_result)


@app.get("/<package:str>/<func:str>")
async def req_by_static(request, package, func):
    try:
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

        parse_param(func_dict)

        if inspect.isasyncgenfunction(func_attr) or inspect.iscoroutinefunction(func_attr):
            result = await func_attr(**func_dict)
        else:
            result = func_attr(**func_dict)
        result_no_enum = enum_to_value(result)

    except Exception as e:
        wrap_result = dict()
        wrap_result["code"] = -1
        wrap_result["message"] = str(e)
        return json(wrap_result)

    wrap_result = dict()
    wrap_result["code"] = 0
    wrap_result["data"] = result_no_enum
    return json(wrap_result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, dev=False)
