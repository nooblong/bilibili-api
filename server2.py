import asyncio

import bilibili_api.video
from bilibili_api import video, Credential
from bilibili_api.tools.parser import get_fastapi

import uvicorn


async def main():
    v = video.Video(bvid="BV1r841167d9")
    # 获取视频下载链接
    download_url_data = await v.get_download_url(0)
    # 解析视频下载信息
    detecter = video.VideoDownloadURLDataDetecter(data=download_url_data)
    print(detecter.detect_best_streams(audio_max_quality=bilibili_api.video.AudioQuality.HI_RES))
    # streams = detecter.detect_best_streams()


if __name__ == "__main__":
    uvicorn.run(get_fastapi(), host="0.0.0.0", port=9000)
    # asyncio.run(main())
