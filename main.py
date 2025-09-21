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
    
    @filter.command("ai")
    async def call_llm(self, event:AstrMessageEvent,text:str):
        '''ai回复功能'''
        logger.info(len(text))
        logger.info(text)
        if len(text)>300:
            yield event.plain_result("too long!")
            return
        provider=self.context.get_using_provider()
        try:
            llm_response = await provider.text_chat(
                prompt="",
                contexts=[
                    {"role": "system", "content": "你是一个有机化学教授，你将看到学生提问的一些有机化学问题，你需要对它们做出简明且准确的解答，尽量不要超过150字。但是，对于你不能确定的理论，你需要明确指出，而非自行编造。对于与有机化学无关的问题，你可以用一句话简要回答或者拒绝回答。"},
                    {"role": "user", "content": text}
                ]
            )
            out_text = llm_response.completion_text
            yield event.plain_result(out_text)
        except Exception as e:
            logger.error(f"LLM调用失败: {e}")
    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
