import asyncio
import sys

from bilibili_api import *


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


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main2())
    c = getattr(video, "Video")(bvid="BV1cF411D7x4")
    d = getattr(video, "Video")(bvid="BV1cF411D7x4")

    print(dir(sys.modules[__name__]))
    b = getattr(sys.modules[__name__], "video")
    e = getattr(b, "Video")(bvid="BV1cF411D7x4")
    asyncio.run(getVideo(e))
