from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
import urllib.request
import urllib.parse
import json

PROVINCE = {"北京市":"ABJ","天津市":"ATJ","河北省":"AHE","山西省":"ASX","内蒙古自治区":"ANM","辽宁省":"ALN","吉林省":"AJL","黑龙江省":"AHL","上海市":"ASH","江苏省":"AJS","浙江省":"AZJ","安徽省":"AAH","福建省":"AFJ","江西省":"AJX","山东省":"ASD","河南省":"AHA","湖北省":"AHB","湖南省":"AHN","广东省":"AGD","广西壮族自治区":"AGX","海南省":"AHI","重庆市":"ACQ","四川省":"ASC","贵州省":"AGZ","云南省":"AYN","西藏自治区":"AXZ","陕西省":"ASN","甘肃省":"AGS","青海省":"AQH","宁夏回族自治区":"ANX","新疆维吾尔自治区":"AXJ","香港特别行政区":"AXG","澳门特别行政区":"AAM","台湾省":"ATW"}

AVAILABLE = True
BLACK_LIST = []

@on_command('weather启用', permission=SUPERUSER)
async def weatherSetUp(session: CommandSession):
    global AVAILABLE
    AVAILABLE = True
    await session.send('weather已启用！让507bot帮你们预测天气吧')

@on_command('weather禁用', permission=SUPERUSER)
async def weatherShutDown(session: CommandSession):
    global AVAILABLE
    AVAILABLE = False
    await session.send('weather禁用了...有这么不准么吗？')

@on_command('weather黑名单', permission=SUPERUSER)
async def weatherBlackListPush(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if uid in BLACK_LIST:
        await session.send('这个人已经在weather黑名单里了')
    elif '1419626179' in uid:
        await session.send('我才不会把507加到黑名单里呢！')
    else:
        BLACK_LIST.append(uid)
        await session.send(uid+'的weather功能已禁用')

@on_command('weather出狱', permission=SUPERUSER)
async def weatherBlackListPop(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if '1419626179' in uid:
        await session.send('507怎么可能在黑名单里呢！')
    elif uid not in BLACK_LIST:
        await session.send('这个人不在weather黑名单里哦')
    else:
        for i in range(len(BLACK_LIST)):
            if uid in BLACK_LIST[i] or BLACK_LIST[i] in uid:
                del BLACK_LIST[i]
                break
        await session.send(uid+'的weather功能已启用')

@on_command('天气')
async def weather(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global AVAILABLE
    if not AVAILABLE:
        return
    # 格式解析
    city = session.state.get('message') or session.current_arg
    city = city.split()
    if len(city) == 1:
        province = city[0]
        city = city[0]
    elif len(city) != 2:
        await session.send("格式输错啦！请输入：天气 省份 城市")
        return
    else:
        province = city[0]
        city = city[1]
    if '台' in province:
        await session.send("天气不知道，但是大的要来了")
        return
    # 查询省份代码
    flag = True
    for each in PROVINCE.keys():
        if province in each:
            province = each
            flag = False
            break
    if flag:
        await session.send("查询的省份不存在哦")
        return
    province_code = PROVINCE[province]
    url = 'http://www.nmc.cn/f/rest/province/'+str(province_code)
    response = urllib.request.Request(url)
    response = urllib.request.urlopen(response)
    html=response.read().decode('utf-8')
    html = json.loads(html)
    city_code = ''
    for each in html:
        if city in each['city']:
            city = each['city']
            city_code = each['code']
            break
    if city_code == '':
        if city != province:
            await session.send("查询的城市不存在哦")
            return
        else:
            await session.send("格式输错啦！请输入：天气 省份 城市，或者：天气 直辖市 具体地名")
            return   
    url = "http://www.nmc.cn/f/rest/real/" + city_code
    response = urllib.request.Request(url)
    response = urllib.request.urlopen(response)
    html=response.read().decode('utf-8')
    html = json.loads(html)
    temp = html['weather']['temperature']
    wtr = html['weather']['info']
    rain = html['weather']['rain']
    await session.send(province+city+'的实时天气状况:\r\n'+'气温：'+str(temp)+'摄氏度\r\n'+'天气：'+str(wtr)\
                       +'\r\n雨水等级：'+str(rain))
    if str(wtr) == '晴':
        await session.send('[CQ:image,file=cc356f2a4e9f19e2ce62b977c67c3f12.image]')

