from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import urllib.request
import urllib.parse
import json
import time

star = {"白羊座":"aries","金牛座":"taurus","双子座":"gemini",
        "巨蟹座":"cancer","狮子座":"leo","处女座":"virgo",
        "天秤座":"libra","天蝎座":"scorpio","射手座":"sagittarius",
        "摩羯座":"capricorn","水瓶座":"aquarius","双鱼座":"pisces"}

@on_command('运势')
async def luck(session: CommandSession):
    st = session.state.get('message') or session.current_arg
    if st == "":
        return 
    if st not in star.keys():
       await session.send('没有'+st+'这个星座哦！')
    localtime = time.localtime(time.time())
    year = str(localtime.tm_year)
    mon = str(localtime.tm_mon)
    day = str(localtime.tm_mday)
    url = "https://app.data.qq.com/?umod=astro"+\
    "&act=astro&jsonp=1&func=TodatTpl&t=3&a="+str(star[st])+"&y=2015&m="+mon+"&d="+day
    response = urllib.request.Request(url)
    response = urllib.request.urlopen(response)
    html=response.read().decode('unicode_escape')
    html = html[9:-2].replace('\r\n','').replace('\n','')
    res = year+'.'+mon+'.'+day+st+"的运势:\n"
    res = res + json.loads(html)["fortune"][0]["content"]
    await session.send(res)
