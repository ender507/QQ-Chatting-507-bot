from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, Event

import json
import requests
from zhconv import convert

whatanime = on_command('whatanime', aliases=set(('whatanime', '识番', '識番')))

@whatanime.handle()
async def __(bot: Bot, event: Event, state: T_State):
    image_arg = str(event.get_message()).strip()
    if image_arg:
        state['whatanime'] = image_arg[0]


@whatanime.got("whatanime",prompt="图呢图呢图呢")
async def _(bot: Bot, event: Event, state: T_State):
    anime_data = state['whatanime']
    if type(anime_data) == type(list()):
        anime_data = anime_data[0]
    #try:
    anime_data_report = await get_anime(anime_data)
    #except:
    #    await session.send("接口连接错误，请重新发送一次")
    if anime_data_report:
        await whatanime.send(convert(anime_data_report, 'zh-hans'))
    else:
        await whatanime.send("找不到嗷")


async def get_anime(anime: str) -> str:
    url = 'https://api.trace.moe/search?anilistInfo&url={}'.format(anime)
    response = requests.get(url)
    print(url)
    try:
        # anime_json = json.loads(response.text)
        anime_json = response.json()
    except:
        print('-----------')
        print(str(response.text))
        print('-----------')
    if anime_json == 'Error reading imagenull': return "图像源错误，注意必须是静态图片哦"
    repass = ""
    for anime in anime_json["result"][:3]:
        anime_name = ""
        for each in anime['anilist']['synonyms']:
            for ch in each:
                if u'\u4e00' <= ch <= u'\u9fff':
                    anime_name = each
                    break
        if anime_name == "":
            anime_name = anime["anilist"]["title"]["native"]
        episode = anime["episode"]
        at = int(anime["to"])
        m, s = divmod(at, 60)
        similarity = anime["similarity"]

        putline = "【{}】第{}集{}分{}秒处 相似度:{:.2%}".format(anime_name, episode if episode else '?', m, s, similarity)
        if repass:
            repass = "\n".join([repass, putline])
        else:
            repass = putline
    return repass
