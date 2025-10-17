from astrbot.core.message.components import BaseMessageComponent,ComponentType,Plain,Reply
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
import astrbot.api.message_components as Comp
from astrbot.api import logger,AstrBotConfig
import re,random
import pypinyin
from . import jie

@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context,config:AstrBotConfig):
        super().__init__(context)
        self.config=config

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    @filter.command("ai")
    async def call_llm(self, event:AstrMessageEvent,text:str):
        '''ai回复功能'''
        if not self.config.llm:
            return
        logger.info(len(text))
        logger.info(text)
        if len(text)>300:
            yield event.plain_result("too long!")
            return
        provider=self.context.get_using_provider()
        try:
            if provider==None:
                raise Exception
            llm_response = await provider.text_chat(
                prompt="",
                contexts=[
                    {"role": "system", "content": "你是一个有机化学教授，你将看到学生提问的一些有机化学问题，你需要对它们做出简明且准确的解答，尽量不要超过150字。但是，对于你不能确定的理论，你需要明确指出，而非自行编造。对于与有机化学无关的问题，你可以用一句话简要回答或者拒绝回答。"},
                    {"role": "user", "content": text}
                ]
            )
            out_text = llm_response.completion_text
            yield event.plain_result(out_text)
            event.stop_event()
        except Exception as e:
            logger.error(f"LLM调用失败: {e}")
    @filter.command("杰")
    async def order_jie(self,event:AstrMessageEvent):
        '''智能下单杰哥炒饭命令'''
        if not self.config.order_jie:
            return
        
        yield event.plain_result(jie.random_jie())
    @filter.event_message_type(filter.EventMessageType.ALL)
    async def beng_kabuda(self,event:AstrMessageEvent):
        """将对话中所有“卡布达”替换为发送者名字，并在末尾加上“~卡布”"""
        if not self.config.kabuda:
            return
        if random.random() >0.3 :
            return
        text=event.get_message_str()
        logger.info(text)
        if not re.search('卡布达',text):
            event.stop_event()
            return
        logger.info(re.match('卡布达',text))
        segs=event.get_messages()
        i=0
        for _ in range(0,len(segs)):
            if isinstance(segs[i],Reply):
                del segs[i]
            else:
                i+=1
        for raw in segs:
            if isinstance(raw,Plain):
                raw.text=re.sub('卡布达',event.get_sender_name(),raw.text)
        segs.append(Plain('~卡布'))
        yield event.chain_result(segs)
    @filter.event_message_type(filter.EventMessageType.ALL)
    async def search_name(self,event:AstrMessageEvent):
        '''查找名字的拼音首字母'''
        if not self.config.name:
            return
        assert isinstance(self.config.name_probability,float)
        if random.random() >self.config.name_probability:
            return
        assert isinstance(self.config.name_list,list)
        name_list:list[str]=self.config.name_list
        character_list:list[str]=[]
        segs=event.get_messages()
        raw_texts:list[str]=[]
        for seg in segs:
            if isinstance(seg,Plain):
                line=''
                for char in seg.text:
                    if '\u4e00' <= char <= '\u9fa5':
                        line+=char
                    else:
                        if len(line)>0:
                            raw_texts.append(line)
                            line=''
                if len(line)>0:
                    raw_texts.append(line)
                    line=''
        logger.info(raw_texts)
        for line in raw_texts:
            sm1=pypinyin.pinyin(line,pypinyin.Style.FIRST_LETTER)
            sm2=''.join([char for sublist in sm1 for char in sublist])
            character_list.append(sm2)
        for _ in range(len(character_list)):
            for name in name_list:
                if match:=re.search(name,character_list[_]):
                    return event.plain_result(raw_texts[_][match.start():match.end()])
    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
