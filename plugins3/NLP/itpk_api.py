import json
from typing import Optional
import aiohttp
import nonebot
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from loguru import logger

async def call_NLP_api(bot: Bot, event: Event,text) -> Optional[str]:

    if not text:
        return None


    # 构造请求数据
    api_key = '86b7f3a08e1923c02726146d222bb2b0'
    api_secret = '23kjlsify7ys'
    url = "http://i.itpk.cn/api.php?question=%s&api_key=%s&api_secret=%s" %(text, api_key, api_secret)
    
    try:
        # 使用 aiohttp 库发送最终的请求
        async with aiohttp.ClientSession() as sess:
            async with sess.post(url) as response:

                if response.status != 200:
                    # 如果 HTTP 响应状态码不是 200，说明调用失败
                    await bot.send(event,"对话api调用发生错误 :(")
                    return None

                resp_text = await response.text()

                if resp_text:
                    return resp_text

    except (aiohttp.ClientError, json.JSONDecodeError, KeyError) as e:
        logger.error(f"An error occupied when calling api: {e}")
        await bot.send(event,"对话api调用发生错误 :(")
        return None
