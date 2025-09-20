from AstrBot.astrbot.core.message.components import BaseMessageComponent,ComponentType
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
import astrbot.api.message_components as Comp
from astrbot.api import logger

@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.event_message_type(filter.EventMessageType.ALL)
    async def helloworld(self, event: AstrMessageEvent):
        """这是一个 hello world 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        flag=0
        out_message_chain=[
            Comp.At(qq=event.get_sender_id()),
            Comp.Plain(f"你好，{event.get_sender_name()},你发送了：")
        ]
        for comp in message_chain:
            if comp.type==ComponentType.At:
                if str(comp.qq)==str(event.get_self_id()):
                    flag=1
            else:
                out_message_chain.append(comp)
        if flag==0:
            return
        logger.info(message_chain)
        out_message_chain.extend(message_chain)
        if event.is_at_or_wake_command:
            yield event.chain_result(out_message_chain) # 发送一条纯文本消息

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
