from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
import nonebot
import json
import requests
from zhconv import convert

@on_command('whatanime', aliases=('whatanime', '识番', '識番'))
async def whatanime(session: CommandSession):
    anime_data = session.get('whatanime', prompt='图呢图呢图呢')
    if type(anime_data) == type(list()):
        anime_data = anime_data[0]
    #try:
    anime_data_report = await get_anime(anime_data)
    #except:
    #    await session.send("接口连接错误，请重新发送一次")
    if anime_data_report:
        await session.send(convert(anime_data_report, 'zh-hans'))
    else:
        await session.send("找不到嗷")


@whatanime.args_parser
async def _(session: CommandSession):
    image_arg = session.current_arg_images

    if session.is_first_run:
        if image_arg:
            session.state['whatanime'] = image_arg[0]
        return

    if not image_arg:
        session.pause('图呢图呢图呢')

    session.state[session.current_key] = image_arg

@on_natural_language(keywords={'whatanime', '识番', '識番'})
async def _(session: NLPSession):
    msg = session.msg
    return IntentCommand(90.0, 'whatanime', current_arg=msg or '')


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
