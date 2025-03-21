"""
bilibili_api.utils.Danmaku

弹幕类。
"""

import time
from enum import Enum
from typing import Union

from .utils import crack_uid as _crack_uid


class DmFontSize(Enum):
    """
    字体大小枚举。

    - EXTREME_SMALL
    - SUPER_SMALL
    - SMALL
    - NORMAL
    - BIG
    - SUPER_BIG
    - EXTREME_BIG
    """

    EXTREME_SMALL = 12
    SUPER_SMALL = 16
    SMALL = 18
    NORMAL = 25
    BIG = 36
    SUPER_BIG = 45
    EXTREME_BIG = 64


class DmMode(Enum):
    """
    弹幕模式枚举。

    - FLY: 飞行弹幕
    - TOP: 置顶弹幕
    - BOTTOM: 底部弹幕
    - REVERSE: 反向弹幕
    - ADVANCE: 高级弹幕
    - CODE: 代码弹幕 (基于 flash 实现)
    - SPECIAL: BAS 弹幕
    """

    FLY = 1
    TOP = 5
    BOTTOM = 4
    REVERSE = 6
    ADVANCE = 7
    CODE = 8
    SPECIAL = 9


class Danmaku:
    """
    弹幕类。
    """

    def __init__(
        self,
        text: str,
        dm_time: float = 0.0,
        send_time: float = time.time(),
        crc32_id: str = "",
        color: str = "ffffff",
        weight: int = -1,
        id_: int = -1,
        id_str: str = "",
        action: str = "",
        mode: Union[DmMode, int] = DmMode.FLY,
        font_size: Union[DmFontSize, int] = DmFontSize.NORMAL,
        is_sub: bool = False,
        pool: int = 0,
        attr: int = -1,
        uid: int = -1,
    ):
        """
        大会员专属颜色文字填充：http://i0.hdslb.com/bfs/dm/9dcd329e617035b45d2041ac889c49cb5edd3e44.png

        大会员专属颜色背景填充：http://i0.hdslb.com/bfs/dm/ba8e32ae03a0a3f70f4e51975a965a9ddce39d50.png

        Args:
            text      (str)                             : 弹幕文本。

            dm_time   (float, optional)                 : 弹幕在视频中的位置，单位为秒。Defaults to 0.0.

            send_time (float, optional)                 : 弹幕发送的时间。Defaults to time.time().

            crc32_id  (str, optional)                   : 弹幕发送者 UID 经 CRC32 算法取摘要后的值。Defaults to "".

            color     (str, optional)                   : 弹幕十六进制颜色。Defaults to "ffffff" (如果为大会员专属的颜色则为"special").

            weight    (int, optional)                   : 弹幕在弹幕列表显示的权重。Defaults to -1.

            id_       (int, optional)                   : 弹幕 ID。Defaults to -1.

            id_str    (str, optional)                   : 弹幕字符串 ID。Defaults to "".

            action    (str, optional)                   : 暂不清楚。Defaults to "".

            mode      (Union[DmMode, int], optional)    : 弹幕模式。Defaults to Mode.FLY.

            font_size (Union[DmFontSize, int], optional): 弹幕字体大小。Defaults to FontSize.NORMAL.

            is_sub    (bool, optional)                  : 是否为字幕弹幕。Defaults to False.

            pool      (int, optional)                   : 池。Defaults to 0.

            attr      (int, optional)                   : 暂不清楚。 Defaults to -1.

            uid       (int, optional)                   : 弹幕发送者 UID。Defaults to -1.
        """
        self.text = text
        self.dm_time = dm_time
        self.send_time = send_time
        self.crc32_id = crc32_id
        self.color = color
        self.weight = weight
        self.id_ = id_
        self.id_str = id_str
        self.action = action
        self.mode = mode.value if isinstance(mode, DmMode) else mode
        self.font_size = (
            font_size.value if isinstance(font_size, DmFontSize) else font_size
        )
        self.is_sub = is_sub
        self.pool = pool
        self.attr = attr
        self.uid = uid

    def __str__(self):
        ret = "%s, %s, %s" % (self.send_time, self.dm_time, self.text)
        return ret

    def __len__(self):
        return len(self.text)

    @staticmethod
    def crack_uid(crc32_id: str):
        """
        (@staticmethod)

        暴力破解 UID，可能存在误差，请慎重使用。

        精确至 UID 小于 10000000 的破解。

        Args:
            crc32_id (str): crc32 id

        Returns:
            int: 真实 UID。
        """
        return int(_crack_uid(crc32_id))

    def to_xml(self):
        """
        将弹幕转换为 xml 格式弹幕

        Returns:
            str: xml
        """
        txt = self.text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        string = f'<d p="{self.dm_time},{self.mode},{self.font_size},{int(self.color, 16)},{self.send_time},{self.pool},{self.crc32_id},{self.id_},11">{txt}</d>'
        return string


class SpecialDanmaku:
    def __init__(
        self,
        content: str,
        id_: int = -1,
        id_str: str = "",
        mode: Union[DmMode, int] = DmMode.SPECIAL,
        pool: int = 2,
    ):
        """
        Args:
            content (str)               : 弹幕内容

            id_     (int)               : 弹幕 id. Defaults to -1.

            id_str  (str)               : 弹幕 id (string 类型). Defaults to "".

            mode    (Union[DmMode, int]): 弹幕类型. Defaults to DmMode.SPECIAL.

            pool    (int)               : 弹幕池. Defaults to 2.
        """
        self.content = content
        self.id_ = id_
        self.id_str = id_str
        self.mode = mode.value if isinstance(mode, DmMode) else mode
        self.pool = pool

    def __str__(self):
        return f"{self.content}"
