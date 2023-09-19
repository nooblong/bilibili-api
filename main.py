import asyncio
import inspect
import sys
import socketserver as SocketServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from sys import argv

from bilibili_api import *
from bilibili_api.session import Session, Event, get_at


async def main1() -> None:
    # 实例化 Video 类
    v = video.Video(bvid="BV1cF411D7x4")
    # 获取信息
    info = await v.get_info()
    # 打印信息
    print(info)


async def main2() -> None:
    # 实例化 Credential 类
    credential = Credential(
        sessdata="",
        bili_jct="", buvid3="")
    # 实例化 Video 类
    v = video.Video(bvid="BV1TP411a7op", credential=credential)
    info = await v.get_info()
    print(info)
    # 给视频点赞
    await v.like(True)


async def getVideo(obj):
    info = await obj.get_info()
    print(info)


credential = Credential(

v = video.VideoOnlineMonitor(bvid="BV1Z94y1H718", credential=credential)

# @v.on('ONLINE')
# async def on_online_update(event):
#     """
#     在线人数更新
#     """
#     print(event)
#
#
# @v.on('DANMAKU')
# async def on_danmaku(event):
#     """
#     收到实时弹幕
#     """
#     print(event)

session = Session(credential=credential)


@session.on(Event.PICTURE)
async def pic(event: Event):
    img: Picture = event.content
    await img.download("./")


async def reply(event: Event = None):
    print(event.content)
    if event.content == "/close":
        session.close()
    elif event.content == "来张涩图":
        img = await Picture.from_file("test.png").upload_file(session.credential)
        await session.reply(event, img)
    else:
        await session.reply(event, "你好李鑫")


def a_new_decorator(a_func):
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
        asyncio.get_event_loop().create_task(a_func("fuck"))
        print("I am doing some boring work after executing a_func()")

    return wrapTheFunction


@a_new_decorator
async def a_function_requiring_decoration(text=None):
    """Hey yo! Decorate me!"""
    print("text: ", text)


def logit(func):
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called ", args, kwargs)
        return func(*args, **kwargs)

    return with_logging


@logit
def addition_func(x):
    """Do some math."""
    return x + x


def simpleFunc():
    print("simple")


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self._set_headers()
        print(post_data)
        print(post_data.decode("unicode_escape"))


def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


if __name__ == '__main__':
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

    result = addition_func(4)
    print(result)
    a_function_requiring_decoration()
    session.add_event_listener(Event.TEXT, reply())
    asyncio.get_event_loop().run_until_complete(session.start())
    # asyncio.get_event_loop().run_until_complete(
    #     asyncio.wait([
    #         sync(v.connect())
    #     ]))
