from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import urllib.request
import urllib.parse
import json

PROVINCE = {"北京市":"ABJ","天津市":"ATJ","河北省":"AHE","山西省":"ASX","内蒙古自治区":"ANM","辽宁省":"ALN","吉林省":"AJL","黑龙江省":"AHL","上海市":"ASH","江苏省":"AJS","浙江省":"AZJ","安徽省":"AAH","福建省":"AFJ","江西省":"AJX","山东省":"ASD","河南省":"AHA","湖北省":"AHB","湖南省":"AHN","广东省":"AGD","广西壮族自治区":"AGX","海南省":"AHI","重庆市":"ACQ","四川省":"ASC","贵州省":"AGZ","云南省":"AYN","西藏自治区":"AXZ","陕西省":"ASN","甘肃省":"AGS","青海省":"AQH","宁夏回族自治区":"ANX","新疆维吾尔自治区":"AXJ","香港特别行政区":"AXG","澳门特别行政区":"AAM","台湾省":"ATW"}

@on_command('天气')
async def weather(session: CommandSession):
    # 格式解析
    city = session.state.get('message') or session.current_arg
    city = city.split()
    if len(city) != 2:
        await session.send("格式输错啦！请输入：天气 省份 城市")
    province = city[0]
    city = city[1]
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
            city_code = each['code']
            break
    if city_code == '':
        await session.send("查询的城市不存在哦")
    url = "http://www.nmc.cn/f/rest/real/" + city_code
    response = urllib.request.Request(url)
    response = urllib.request.urlopen(response)
    html=response.read().decode('utf-8')
    html = json.loads(html)
    temp = html['weather']['temperature']
    wtr = html['weather']['info']
    rain = html['weather']['rain']
    await session.send(province+city+'的实时天气状况:\r\n'+'气温：'+str(temp)+'摄氏度\r\n'+'天气：'+str(wtr)\
                       +'\r\n之后下雨概率：'+str(rain))

