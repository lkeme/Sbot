#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lkeme

from typing import Type, Union, Literal, Mapping, Iterable, Optional

from .message import BaseMessage, BaseMessageSegment

__all__ = ["T_CQMSG", "AdapterMessage", "AdapterMessageSegment", "escape"]

T_CQMSG = Union[
    str, Mapping, Iterable[Mapping], "AdapterMessageSegment", "AdapterMessage"
]


class AdapterMessage(BaseMessage["AdapterMessageSegment"]):
    """Adapter 消息。"""

    @property
    def _message_segment_class(self) -> Type["AdapterMessageSegment"]:
        return AdapterMessageSegment

    def _str_to_message_segment(self, msg) -> "AdapterMessageSegment":
        return AdapterMessageSegment.text(msg)


class AdapterMessageSegment(BaseMessageSegment["AdapterMessage"]):
    """Adapter 消息字段。"""

    @property
    def _message_class(self) -> Type["AdapterMessage"]:
        return AdapterMessage

    def __str__(self) -> str:
        if self.type == "text":
            return self.data.get("text", "")
        return self.get_cqcode()

    def get_cqcode(self) -> str:
        """
        Returns:
            此消息字段的 CQ 码形式。
        """
        if self.type == "text":
            return escape(self.data.get("text", ""), escape_comma=False)

        params = ",".join(
            [f"{k}={escape(str(v))}" for k, v in self.data.items() if v is not None]
        )
        return f'[CQ:{self.type}{"," if params else ""}{params}]'

    @classmethod
    def text(cls, text: str) -> "AdapterMessageSegment":
        """纯文本"""
        return cls(type="text", data={"text": text})

    @classmethod
    def face(cls, id_: int) -> "AdapterMessageSegment":
        """
        QQ表情，ID可能的值详见：
        https://github.com/richardchien/coolq-http-api/wiki/%E8%A1%A8%E6%83%85-CQ-%E7%A0%81-ID-%E8%A1%A8
        """
        return cls(type="face", data={"id": str(id_)})

    @classmethod
    def image(
            cls,
            file: str,
            type_: Optional[Literal["flash"]] = None,
            cache: bool = True,
            proxy: bool = True,
            timeout: Optional[int] = None,
    ) -> "AdapterMessageSegment":
        # 绝对路径，例如 file:///C:\\Users\Alice\Pictures\1.png，格式使用 file URI
        # 网络 URL，例如 https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png
        # Base64 编码，例如 base64://iQAAAAABJRU5ErkJggg==
        # 示例: [CQ:image,file=http://baidu.com/1.jpg,type=show,id=40004]
        """
        图片
         file: 文件来源，可以是网址，也可以是文件所在的路径
        type_: flash 表示闪照, show 表示秀图, 默认普通图片
        cache: 只在通过网络 URL 发送时有效, 表示是否使用已缓存的文件, 默认 1
        id_: 发送秀图时的特效id, 默认为40000
            可用的特效ID:
            40000(普通)  40001(幻影)  40002(抖动)
            40003(生日)  40004(爱你)  40005(征友)
        """
        return cls(
            type="image",
            data={
                "file": file,
                "type": type_,
                "cache": cache,
                "proxy": proxy,
                "timeout": timeout,
            },
        )

    @classmethod
    def record(
            cls,
            file: str,
            magic: bool = False,
            cache: bool = True,
            proxy: bool = True,
            timeout: Optional[int] = None,
    ) -> "AdapterMessageSegment":
        """语音"""
        return cls(
            type="record",
            data={
                "file": file,
                "magic": magic,
                "cache": cache,
                "proxy": proxy,
                "timeout": timeout,
            },
        )

    @classmethod
    def video(
            cls,
            file: str,
            cache: bool = True,
            proxy: bool = True,
            timeout: Optional[int] = None,
    ) -> "AdapterMessageSegment":
        """短视频"""
        return cls(
            type="video",
            data={"file": file, "cache": cache, "proxy": proxy, "timeout": timeout},
        )

    @classmethod
    def at(cls, qq: Union[list, int, Literal["all"]]) -> Union["AdapterMessageSegment", list["AdapterMessageSegment"]]:
        """@某人"""
        if isinstance(qq, list):
            text = ''.join([str(cls(type="at", data={"qq": str(q)})) for q in qq])
            return cls(type="text", data={"text": text})
        else:
            return cls(type="at", data={"qq": str(qq)})

    @classmethod
    def rps(cls) -> "AdapterMessageSegment":
        """猜拳魔法表情"""
        return cls(type="rps", data={})

    @classmethod
    def dice(cls) -> "AdapterMessageSegment":
        """掷骰子魔法表情"""
        return cls(type="dice", data={})

    @classmethod
    def shake(cls) -> "AdapterMessageSegment":
        """窗口抖动（戳一戳）"""
        return cls(type="shake", data={})

    @classmethod
    def poke(cls, type_: str, id_: int) -> "AdapterMessageSegment":
        """戳一戳"""
        return cls(type="poke", data={"type": type_, "id": str(id_)})

    @classmethod
    def anonymous(cls, ignore: Optional[bool] = None) -> "AdapterMessageSegment":
        """匿名发消息"""
        return cls(type="anonymous", data={"ignore": ignore})

    @classmethod
    def share(
            cls,
            url: str,
            title: str,
            content: Optional[str] = None,
            image: Optional[str] = None,
    ) -> "AdapterMessageSegment":
        """链接分享"""
        return cls(
            type="share",
            data={"url": url, "title": title, "content": content, "image": image},
        )

    @classmethod
    def contact(cls, type_: Literal["qq", "group"], id_: int) -> "AdapterMessageSegment":
        """推荐好友/推荐群"""
        return cls(type="contact", data={"type": type_, "id": str(id_)})

    @classmethod
    def contact_friend(cls, id_: int) -> "AdapterMessageSegment":
        """推荐好友"""
        return cls(type="contact", data={"type": "qq", "id": str(id_)})

    @classmethod
    def contact_group(cls, id_: int) -> "AdapterMessageSegment":
        """推荐好友"""
        return cls(type="contact", data={"type": "group", "id": str(id_)})

    @classmethod
    def location(
            cls, lat: float, lon: float, title: Optional[str], content: Optional[str] = None
    ) -> "AdapterMessageSegment":
        """位置"""
        return cls(
            type="location",
            data={"lat": str(lat), "lon": str(lon), "title": title, "content": content},
        )

    @classmethod
    def music(
            cls, type_: Literal["qq", "163", "xm"], id_: int
    ) -> "AdapterMessageSegment":
        """音乐分享"""
        return cls(type="music", data={"type": type_, "id": str(id_)})

    @classmethod
    def music_custom(
            cls,
            url: str,
            audio: str,
            title: str,
            content: Optional[str] = None,
            image: Optional[str] = None,
    ) -> "AdapterMessageSegment":
        """音乐自定义分享"""
        return cls(
            type="music",
            data={
                "type": "custom",
                "url": url,
                "audio": audio,
                "title": title,
                "content": content,
                "image": image,
            },
        )

    @classmethod
    def reply(cls, id_: int) -> "AdapterMessageSegment":
        """回复"""
        return cls(type="reply", data={"id": str(id_)})

    @classmethod
    def tts(cls, text: str) -> "AdapterMessageSegment":
        """
        文字转语音
        通过TX的TTS接口, 采用的音源与登录账号的性别有关
        """
        return cls(type="tts", data={"text": text})

    @classmethod
    def node(cls, id_: int) -> "AdapterMessageSegment":
        """合并转发节点"""
        return cls(type="node", data={"id": str(id_)})

    @classmethod
    def node_custom(
            cls, user_id: int, nickname, content: "AdapterMessage"
    ) -> "AdapterMessageSegment":
        """合并转发自定义节点"""
        return cls(
            type="node",
            data={
                "user_id": str(user_id),
                "nickname": str(nickname),
                "content": content,
            },
        )

    @classmethod
    def xml_message(cls, data: str) -> "AdapterMessageSegment":
        """XML 消息"""
        return cls(type="xml", data={"data": data})

    @classmethod
    def json_message(cls, data: str) -> "AdapterMessageSegment":
        """JSON 消息"""
        return cls(type="json", data={"data": data})


def escape(s: str, *, escape_comma: bool = True) -> str:
    """对 CQ 码中的特殊字符进行转义。
    Args:
        s: 待转义的字符串。
        escape_comma: 是否转义 `,`。
    Returns:
        转义后的字符串。
    """
    s = s.replace("&", "&amp;").replace("[", "&#91;").replace("]", "&#93;")
    if escape_comma:
        s = s.replace(",", "&#44;")
    return s


# 防CQ码注入 TODO
def anti_injection():
    pass
