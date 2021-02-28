from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
import random

AVAILABLE = True
BLACK_LIST = []


six = ["棘刺","铃兰","早露","温蒂","傀影","风笛",
       "刻俄柏","阿","煌","莫斯提马","麦哲伦","赫拉格",
       "黑","陈","斯卡蒂","银灰","塞雷娅","星熊","夜莺",
       "闪灵","安洁莉娜","艾雅法拉","伊芙利特","推进之王",
       "能天使","森蚺","史尔特尔","瑕光","泥岩","山","空弦","嵯峨"]
five = ["安哲拉","贾维","蜜蜡","断崖","莱恩哈特",
        "月禾","石棉","极境","巫恋","慑砂",
        "惊蛰","吽","灰喉","布洛卡","苇草","槐琥",
        "送葬人","星极","格劳克斯","诗怀雅",
        "夜魔","食铁兽","狮蝎","空","真理","初雪",
        "崖心","守林人","普罗旺斯","可颂","雷蛇","红",
        "临光","华法琳","赫默","梅尔","天火","陨星","白金",
        "蓝毒","幽灵鲨","拉普兰德","芙兰卡","德克萨斯",
        "凛冬","白面鸮","燧石","四月","奥斯塔","絮雨","卡夫卡",
        "爱丽丝","乌有"]
four = ["孑","卡达","波登可","刻刀","宴","安比尔",
        "梅","红云","桃金娘","苏苏洛","格雷伊","猎蜂",
        "阿消","地灵","深海色","古米","蛇屠箱","角峰","调香师","嘉维尔",
        "末药","暗索","砾","慕斯","霜叶","缠丸","杜宾","红豆",
        "清道夫","讯使","白雪","流星","杰西卡","远山","夜烟","酸糖",
        "芳汀","泡泡","杰克","松果","豆苗"]
three = ["斑点","泡普卡","月见夜","空爆","梓兰","史都华德",
         "安塞尔","芙蓉","炎熔","安德切尔",
         "克洛斯","米格鲁","卡缇","梅兰莎","翎羽","香草","芬"]

# https://blog.csdn.net/weixin_50000392/article/details/109302310
@on_command('ark启用', permission=SUPERUSER)
async def arkSetUp(session: CommandSession):
    global AVAILABLE
    AVAILABLE = True
    await session.send('ark已启用！博士们来抽卡吧')

@on_command('ark禁用', permission=SUPERUSER)
async def arkShutDown(session: CommandSession):
    global AVAILABLE
    AVAILABLE = False
    await session.send('ark禁用了...是不是脸太黑了？')

@on_command('ark黑名单', permission=SUPERUSER)
async def arkBlackListPush(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if uid in BLACK_LIST:
        await session.send('这个人已经在ark黑名单里了')
    elif '1419626179' in uid:
        await session.send('我才不会把507加到黑名单里呢！')
    else:
        BLACK_LIST.append(uid)
        await session.send(uid+'的ark功能已禁用')

@on_command('ark出狱', permission=SUPERUSER)
async def arkBlackListPop(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if '1419626179' in uid:
        await session.send('507怎么可能在黑名单里呢！')
    if uid not in BLACK_LIST:
        await session.send('这个人不在ark黑名单里哦')
    else:
        for i in range(len(BLACK_LIST)):
            if uid in BLACK_LIST[i] or BLACK_LIST[i] in uid:
                del BLACK_LIST[i]
                break
        await session.send(uid+'的ark功能已启用')


@on_command('明日方舟抽卡')
async def gacha(session: CommandSession):
    global AVAILABLE
    if not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return

    six_count = 0
    five_count = 0
    four_count = 0
    three_count = 0
    res = ""
    for i in range(10):
        roll = random.randint(1,100)
        if roll <= 3:
            roll = random.randint(0,len(six)-1)
            six_count += 1
            res = res + '【6】'+six[roll] + '\r\n'
        elif roll <= 10:
            roll = random.randint(0,len(five)-1)
            five_count += 1
            res = res + '【5】'+five[roll] + '\r\n'
        elif roll <= 58:
            roll = random.randint(0,len(four)-1)
            four_count += 1
            res = res + '【4】'+four[roll] + '\r\n'
        else:
            roll = random.randint(0,len(three)-1)
            three_count += 1
            res = res + '【3】'+three[roll] + '\r\n'
    res = res + '共有' + str(six_count) + '个6星，' + str(five_count) + '个5星，' + str(four_count) + '个4星，' + str(three_count) + '个3星'
    await session.send(res)
    if six_count > 1:
        await session.send('你就是天选之人？能不能把运气借点给507用？')
    elif six_count == 1:
        await session.send('出货啦！可喜可贺可喜可贺')
    elif five_count >=1:
        await session.send('下次十连一定能更好！')
    elif four_count >= 1:
        await session.send('啊这')
    else:
        await session.send('从某种意义上说，你也算是欧皇了')

    
@on_natural_language(keywords={'明日方舟抽卡','明日方舟十连'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'gacha')
