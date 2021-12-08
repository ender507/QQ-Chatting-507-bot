from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, Event
from nonebot.permission import SUPERUSER

import random
import time
import numpy as np

TIMETICK = None
SHUT_UP = False

# 防止和其他机器人复读死循环
def replyBreaker(t):
    global TIMETICK
    if TIMETICK is None:
        TIMETICK = time.time()
        return False
    tmp = time.time()
    if tmp - TIMETICK >=t:
        TIMETICK = tmp
        return False
    return True



# mes1：全字匹配
# mes2：部分匹配
# mes3：过滤器
mes1 = dict()
mes2 = dict()
mes3 = []
mes1['507bot']=[\
'\
我是507bot！我的常用指令有：\r\n\
# 通用指令\r\n\
【识番】发送图片，让bot识别番剧名\r\n\
【说话】文本转语音（女声）\r\n\
【单词】发送"单词"查看相关说明\r\n\
【nlp】发送"nlp xxx"，bot会根据你的发送内容进行智能回复\r\n\
【roll】如"roll 6"\r\n\
【天气】如"天气 上海 浦东"、"天气 广东 番禺"\r\n\
【备忘】备忘录功能，输入"备忘 菜单"查看详细内容\r\n\
【戳】如"戳 507"\r\n\
【翻译】如"翻译 hello"\r\n\
【运势】如"运势 水瓶座"\r\n\
【学习】"学习 群友发送内容 bot回复内容"\r\n\
【对联】如"对联 一去二三里"\r\n\
【抽象】如"抽象 爬"\r\n\
【百度】如"百度 今天晚上吃什么"\r\n\
【其他】聊天回复和彩蛋\r\n\
# lu群专属\r\n\
【lulu语录】\r\n\
【来点怪歌】【来点鬼歌】\r\n\
【来点怪叫】【来点鬼叫】\r\n\
# 管理员权限\r\n\
【管理员菜单】查看具体权限指令\r\n\
']
mes1['晚安']=['晚安❤']
mes1['lulu语录']=mes1['るる语录']=mes1['来点lulu']=mes1['来点るる']=['我知道没有单推，但是有点悲伤',
           '我爱你，想抱紧你\r\n你什么时候才能紧紧的拥抱我呢',
           '为什么会爱上不存在的二次元女人？'
           '你没有锁骨','为什么最近大家一直在击剑呢？这是中国文化吗',
           '麻衣，为什么一直抱着桃树不放开？',
           '我也喜欢lol弱的麻衣，不需要改变自己',
           '你先刷牙再说','你先dt毕业吧',
           '变态冰糖也可爱','帅哥哥 我想要兰博基尼❤\r\n谢谢你❤',
           '对不起，我是天才','吐了口臭不行你先爬',
           '久违地吐了','///////爬//////',
           '用手机到底能做什么？只能和沙雕网友说话',
           '有一说一，你的胸部确实比我大',
            '[CQ:record,file=kichiku1.amr]']
mes2['白学']=mes2['和纱']=mes2['北原']=mes2['东马']=mes2['雪菜']=['白学家能不能爬啊']
mes2['去学习']=mes2['学习去']=mes2['自习']=mes2['考试']=mes2['作业']=mes2['上课']=['这就是国家栋梁吧']
mes1['走']=['当舔狗去了']
mes1['走，当舔狗去了']=['发错了']
mes1['laji爬']=['[CQ:image,file=laji爬_0.gif]']
mes2['沙口']=['[CQ:image,file=沙口_0.jpg]',
           '[CQ:image,file=沙口_1.jpg]',
           '[CQ:image,file=沙口_2.jpg]']
mes1['差不多得了']=['[CQ:image,file=差不多得了_0.gif]',
           '[CQ:image,file=差不多得了_1.gif]',
           '[CQ:image,file=差不多得了_2.gif]',
           '[CQ:image,file=差不多得了_0.jpg]',
           '[CQ:image,file=差不多得了_1.jpg]',
           '[CQ:image,file=差不多得了_2.jpg]',
           '[CQ:image,file=差不多得了_3.jpg]']
mes1['基本信息']=['项目名称：507bot\r\n出生日期：2021.2.24\r\n\
版本号：v2.0\r\n项目地址：\r\n\
github地址：https://github.com/ender507/QQ-Chatting-507-bot\r\n\
活跃群聊：3']
mes1['你好']=['你好呀','hello world']
mes1['今天吃啥方便面']=['红烧牛肉','老坛酸菜','红油爆椒牛肉','鲜虾鱼板','香菇炖鸡','雪笋肉丝','泡椒牛肉','咖喱海鲜','香浓叉烧','猪骨浓汤']
mes1['mua']=['(脸红)']
mes2['呀，这是火星语吧']=['我翻译得出来！我厉害吧']
mes2['507爬']=['我不爬，要爬你让laji爬']
mes2['507bot爬']=['我不爬，要爬你让laji爬']
mes2['二次元']=['[CQ:image,file=二次元_0.jpg]',
           '[CQ:image,file=二次元_1.jpg]',
           '[CQ:image,file=二次元_2.jpg]',
           '[CQ:image,file=二次元_3.jpg]']
mes2['二刺猿']=mes2['二刺螈']=mes2['二次猿']=mes2['二次元'][:]
mes2['发情']=['他不是一直都在发情吗？']
mes2['里道骸']=mes2['lidaohai']=['里道骸来点○图']
mes2['好耶']=['[CQ:image,file=好耶_0.jpg]',
           '[CQ:image,file=好耶_1.jpg]',
           '[CQ:image,file=好耶_2.jpg]']
mes2['色图']=mes2['涩图']=mes2['渋図']=mes2['ghs']=['[CQ:image,file=涩图_0.jpg]',
           '[CQ:image,file=涩图_0.png]',
           '[CQ:image,file=涩图_1.png]']
mes3.append("不许ghs！（半恼）")
mes3.append("雾宝来啦")
mes3.append("来点二次元")
mes2['学不完']=['已经是国家栋梁了']

mes2['嘉然']=mes2['然然']=['[CQ:image,file=嘉然_0.gif]',
                       '[CQ:image,file=嘉然_0.jpg]',
                       '[CQ:image,file=嘉然_1.jpg]',
                       '[CQ:image,file=嘉然_2.jpg]',
                       '[CQ:image,file=嘉然_3.jpg]']
mes2['三点']=['[CQ:image,file=三点_0.jpg]',
            '[CQ:image,file=三点_1.jpg]']
mes2['审核']=['[CQ:image,file=审核_0.png]']
mes2['罕见']=['[CQ:image,file=罕见_0.png]',
            '[CQ:image,file=罕见_0.jpg]',
            '[CQ:record,file=罕见_0.amr]']
mes2['吃啥']=['吃屁']

#######################来点系列
mes1['来点lly']=['[CQ:image,file=来点lly_0.png]',
    '[CQ:image,file=来点lly_0.jpg]',
    '[CQ:image,file=来点lly_1.jpg]']
mes1['来点油条']=mes1['来点老油条']=mes1['来点油批']=['[CQ:record,file=来点油条_0.amr]',
            '[CQ:record,file=来点油条_1.amr]',
            '[CQ:record,file=来点油条_2.amr]',
            '[CQ:record,file=来点油条_3.amr]',
            '[CQ:record,file=来点油条_4.amr]',
            '[CQ:record,file=来点油条_5.amr]',
            '[CQ:record,file=来点油条_6.amr]',
            '[CQ:image,file=来点油条_0.jpg]',
            '[CQ:image,file=来点油条_1.jpg]',
            '[CQ:image,file=来点油条_2.jpg]',
            '[CQ:image,file=来点油条_3.jpg]',
            '[CQ:image,file=来点油条_4.jpg]',
            '[CQ:image,file=来点油条_0.png]',
            '[CQ:image,file=来点油条_1.png]',
            '[CQ:image,file=来点油条_2.png]',
            '[CQ:image,file=来点油条_3.png]',
            '[CQ:image,file=来点油条_4.png]',
            '[CQ:image,file=来点油条_5.png]',
            '[CQ:image,file=来点油条_6.png]',
            '[CQ:image,file=来点油条_7.png]',
            '[CQ:image,file=来点油条_8.png]',
            '[CQ:image,file=来点油条_9.png]',
            '[CQ:image,file=来点油条_10.png]',
            '[CQ:image,file=来点油条_11.png]',
            '[CQ:image,file=来点油条_12.png]',
            '[CQ:image,file=来点油条_13.png]',
            '[CQ:image,file=来点油条_14.png]',
            '[CQ:image,file=来点油条_15.png]',
            '[CQ:image,file=来点油条_16.png]',
            '[CQ:image,file=来点油条_17.png]',
            '[CQ:image,file=来点油条_18.png]']
mes1['来点柚子']=mes1['来点yozuki']=['[CQ:image,file=来点柚子_0.png]',
           '[CQ:image,file=来点柚子_1.png]',
           '[CQ:image,file=来点柚子_2.png]',
           '[CQ:image,file=来点柚子_3.png]',
           '[CQ:image,file=来点柚子_4.png]',
           '[CQ:image,file=来点柚子_5.png]',
           '[CQ:image,file=来点柚子_0.jpg]',
           '[CQ:image,file=来点柚子_1.jpg]',
           '[CQ:image,file=来点柚子_2.jpg]',
           '[CQ:image,file=来点柚子_3.jpg]',
           '[CQ:image,file=来点柚子_4.jpg]',
           '[CQ:image,file=来点柚子_5.jpg]']
mes1['来点红炎']=mes1['来点炎子哥']=['[CQ:image,file=来点红炎_0.jpg]',
                            '[CQ:image,file=来点红炎_0.png]',
                            '[CQ:image,file=来点红炎_1.png]',
                            '[CQ:image,file=来点红炎_2.png]',
                            '[CQ:image,file=来点红炎_3.png]',
                            '[CQ:image,file=来点红炎_4.png]',
                            '[CQ:image,file=来点红炎_5.png]']
mes1['来点crylins']=mes1['来点cryl1ns']=mes1['来点cry']=['[CQ:image,file=来点cry_0.jpg]',
            '[CQ:image,file=来点cry_1.jpg]',
            '[CQ:image,file=来点cry_0.png]',
            '[CQ:image,file=来点cry_1.png]']
mes1['来点507']=mes1['来点507bot']=['[CQ:image,file=来点507_0.jpg]',
            '[CQ:image,file=来点507_0.png]',
            '[CQ:image,file=来点507_1.png]']
mes1['来点rikka']=['[CQ:image,file=来点rikka_0.jpg]',
                 '[CQ:image,file=来点rikka_1.jpg]',
                 '[CQ:image,file=来点rikka_0.png]']
mes1['来点雾宝']=mes1['来点雾妹']=['[CQ:image,file=来点雾妹_0.png]',
            '[CQ:image,file=来点雾妹_1.png]',
            '[CQ:image,file=来点雾妹_2.png]']
mes1['来点鸭子']=mes1['来点鸭子哥']=['[CQ:image,file=来点鸭子哥_0.jpg]']
mes1['来点laji']=mes1['来点垃圾']=['[CQ:image,file=来点laji_0.jpg]',
            '[CQ:image,file=来点laji_1.jpg]',
            '[CQ:image,file=来点laji_2.jpg]',
            '[CQ:image,file=来点laji_0.png]',
            '[CQ:image,file=来点laji_1.png]',
            '[CQ:image,file=来点laji_2.png]',
            '[CQ:image,file=来点laji_3.png]',
            '[CQ:image,file=来点laji_4.png]',
            '[CQ:image,file=来点laji_5.png]',
            '[CQ:image,file=来点laji_6.png]',
            '[CQ:image,file=来点laji_7.png]',
            '[CQ:image,file=来点laji_8.png]']
mes1['来点馨妹']=mes1['来点白神馨']=mes1['来点狐狸']=['[CQ:image,file=来点白神馨_0.jpg]',
           '[CQ:image,file=来点白神馨_0.png]',
            '[CQ:image,file=来点白神馨_1.png]',
            '[CQ:image,file=来点白神馨_2.png]']
mes1['来点母鸡']=mes1['来点母狗']=mes1['来点母鸡太太']=mes1['来点母狗太太']=[
            '[CQ:image,file=来点母鸡_0.png]',
            '[CQ:image,file=来点母鸡_1.png]']
mes1['来点CL']=mes1['来点cl']=['[CQ:image,file=来点cl_0.jpg]',
            '[CQ:image,file=来点cl_0.png]',
            '[CQ:image,file=来点cl_1.png]',
            '[CQ:image,file=来点cl_2.png]',
            '[CQ:image,file=来点cl_3.png]',
            '[CQ:image,file=来点cl_4.png]']
mes1['来点akira']=mes1['来点ak']=mes1['来点AK']=['[CQ:image,file=来点akira_0.png]',
                 '[CQ:image,file=来点akira_1.1.png][CQ:image,file=来点akira_1.2.jpg]']
mes1['来点wx']=['[CQ:image,file=来点wx_0.jpg]',
              '[CQ:image,file=来点wx_0.png]']
mes1['来点mana']=['[CQ:image,file=来点mana_0.jpg]',
            '[CQ:image,file=来点mana_0.png]']
mes1['来点疫苗']=['[CQ:image,file=来点疫苗_0.jpg]']
mes1['来点as']=['[CQ:image,file=来点as_0.jpg]']
mes1['来点吴京']=['[CQ:image,file=来点吴京_0.jpg]',
              '[CQ:image,file=来点吴京_1.jpg]',
              '[CQ:image,file=来点吴京_2.jpg]']
mes1['来点阿喵喵']=['[CQ:image,file=来点阿喵喵_0.jpg]',
               '[CQ:image,file=来点阿喵喵_1.jpg]',
               '[CQ:image,file=来点阿喵喵_0.gif]',
               '[CQ:image,file=来点阿喵喵_0.png]',
               '[CQ:image,file=来点阿喵喵_1.png]',
               '[CQ:image,file=来点阿喵喵_2.png]',
               '[CQ:image,file=来点阿喵喵_3.png]']
mes1['来点莲宝']=['[CQ:image,file=来点莲宝_0.png]']
mes1['来点ldh']=mes1['来点里道骸']=['[CQ:image,file=来点ldh_0.jpg]',
        '[CQ:image,file=来点ldh_0.png]']
mes1['来点高质量男性']=['[CQ:image,file=来点高质量男性_0.jpg]']
mes1['来点海豹']=['[CQ:image,file=来点海豹_0.gif]']
mes1['来点猫猫']=['[CQ:image,file=来点猫猫_0.jpg]']
mes1['来点猫诺']=['[CQ:image,file=来点猫诺_0.jpg]']
mes1['来点Bebe']=mes1['来点bebe']=['[CQ:image,file=来点bebe_0.png']
mes1['来点李银河']=['[CQ:image,file=来点银河_0.png]',
    '[CQ:image,file=来点银河_1.png]',
    '[CQ:image,file=来点银河_2.png]']
mes1['来点银河']=mes1['来点hentai']=['[CQ:image,file=来点hentai_0.jpg]',
                  '[CQ:image,file=来点hentai_0.png]',
                  '[CQ:image,file=来点hentai_1.png]',
                  '[CQ:image,file=来点hentai_2.png]',
                  '[CQ:image,file=来点hentai_3.png]',
                  '[CQ:image,file=来点hentai_4.png]',
                  '[CQ:image,file=来点hentai_5.png]',
                  '[CQ:image,file=来点hentai_6.png]']
mes1['来点加菲猫']=mes1['来点北原春希']=['[CQ:image,file=来点加菲猫_0.jpg]',
            '[CQ:image,file=来点加菲猫_1.jpg]',
            '[CQ:image,file=来点加菲猫_2.jpg]',
            '[CQ:image,file=来点加菲猫_3.jpg]',
            '[CQ:image,file=来点加菲猫_0.png]']
mes1['来点fyy']=mes1['来点ふゆゆ']=['[CQ:record,file=来点fyy_0.amr]',
                                '[CQ:record,file=来点fyy_1.amr]',
                                '[CQ:image,file=来点fyy_0.jpg]',
                                '[CQ:image,file=来点fyy_0.png]']
mes2['666']=mes2['六六六']=['[CQ:record,file=666.amr]']
mes1['az']=mes1['啊这']=['[CQ:record,file=az.amr]']
mes2['谢谢']=['[CQ:record,file=xiexie.amr]']
mes1['菜']=['[CQ:record,file=cai.amr]','','']
mes1['来点鬼叫']=['[CQ:record,file=guaijiao1.amr]',
                     '[CQ:record,file=guaijiao2.amr]',
                     '[CQ:record,file=guaijiao3.amr]',
                     '[CQ:record,file=guaijiao4.amr]',
                     '[CQ:record,file=guaijiao5.amr]',
                     '[CQ:record,file=guaijiao6.amr]',
                     '[CQ:record,file=guaijiao7.amr]',
                     '[CQ:record,file=guaijiao8.amr]',
                     '[CQ:record,file=guaijiao9.amr]',
                     '[CQ:record,file=guaijiao10.amr]',
                     '[CQ:record,file=kichiku1.amr]','[CQ:record,file=kichiku1.amr]','[CQ:record,file=kichiku1.amr]','[CQ:record,file=kichiku1.amr]','[CQ:record,file=kichiku1.amr]']
mes1['来点怪叫']=mes1['来点鬼叫'][:]
mes1['来点鬼歌']=['[CQ:record,file=g1.amr]',
                     '[CQ:record,file=g2.amr]',
                     '[CQ:record,file=g3.amr]',
                     '[CQ:record,file=g4.amr]',
                     '[CQ:record,file=g5.amr]',
                     '[CQ:record,file=g6.amr]',
                     '[CQ:record,file=g7.amr]',
                     '[CQ:record,file=g8.amr]',
                     '[CQ:record,file=g9.amr]',
                     '[CQ:record,file=g10.amr]',
                     '[CQ:record,file=kichiku1.amr]','[CQ:record,file=kichiku1.amr]','[CQ:record,file=kichiku1.amr]','[CQ:record,file=kichiku1.amr]','[CQ:record,file=kichiku1.amr]']
mes1['来点怪歌']=mes1['来点鬼歌'][:]
mes2['怎么办']=['[CQ:record,file=zenmeban1.amr]',
                    '[CQ:record,file=zenmeban2.amr]']
mes2['绝了']=['[CQ:record,file=juele.amr]']
mes2['别走']=['[CQ:record,file=biezou.amr]']
mes2['nice']=['[CQ:record,file=nice.amr]']
mes2['奈斯']=['[CQ:record,file=nice.amr]']
mes2['求饶']=['[CQ:record,file=qiurao.amr]']
mes2['这波']=['[CQ:record,file=zhebo.amr]']
mes2['急了']=['[CQ:record,file=jile.amr]']
mes2['爬']=mes2['爪巴']=['[CQ:record,file=pa.amr]','']
mes2['又开始了']=['[CQ:record,file=youkaishile.amr]']
mes2['不会吧']=['[CQ:record,file=不会吧.amr]']
mes2['摩多']=mes2['もっと']=['[CQ:record,file=もっと.amr]']
mes2['ybb']=mes2['有病吧']=mes2['有病病']=['[CQ:record,file=ybb_0.amr]',
                                                          '[CQ:record,file=ybb_1.amr]',
                                                          '[CQ:record,file=ybb_2.amr]',
                                                          '[CQ:record,file=ybb_3.amr]',
                                                          '[CQ:record,file=ybb_4.amr]',
                                                          '[CQ:record,file=ybb_5.amr]',
                                                          '[CQ:record,file=ybb_6.amr]',
                                                          '[CQ:record,file=ybb_7.amr]',
                                                          '[CQ:record,file=ybb_8.amr]',
                                                          '[CQ:record,file=ybb_9.amr]',
                                                          '[CQ:record,file=ybb_10.amr]',
                                                          '[CQ:record,file=ybb_11.amr]',
                                                          '[CQ:record,file=ybb_12.amr]',
                                                          '[CQ:record,file=ybb_13.amr]',
                                                          '[CQ:record,file=ybb_14.amr]',
                                                          '[CQ:record,file=ybb_15.amr]',
                                                          '[CQ:record,file=ybb_16.amr]',
                                                          '[CQ:record,file=ybb_17.amr]']
mes2['op']=mes2['原神']=mes2['原批']=['[CQ:record,file=op_0.amr]',
                                                       '[CQ:record,file=op_1.amr]']



mes=""
replyer = on_command("")

@replyer.handle()
async def _(bot: Bot, event: Event, state: T_State):
    message = str(event.get_message()).strip()
    global mes, mes1, mes2, mes3
    for each in mes3:
        if each in message:
            return None
    for each in mes1.keys():
        if each == message:
            mes = each
            await sendMes1(bot,event)
    for each in mes2.keys():
        if each in message:
            mes = each
            await sendMes2(bot,event)



async def sendMes1(bot,event):
    global mes1, mes
    global SHUT_UP
    if SHUT_UP or replyBreaker(5):
        return
    await bot.send(event,Message(mes1[mes][random.randint(0,len(mes1[mes])-1)]))


async def sendMes2(bot,event):
    global mes2, mes
    global SHUT_UP
    if SHUT_UP or replyBreaker(5):
        return
    await bot.send(event,Message(mes2[mes][random.randint(0,len(mes2[mes])-1)]))


#---------------------------------------------------------------------------
# 以下是不需要权限的开关

# 关
shut_up = on_command('闭嘴')
@shut_up.handle()
async def _(bot: Bot, event: Event, state: T_State):
    global SHUT_UP
    SHUT_UP = True
    await shut_up.send('唔——唔——')

# 查
say_something = on_command('说话啊')
@say_something.handle()
async def _(bot: Bot, event: Event, state: T_State):
    global SHUT_UP
    if SHUT_UP:
        await say_something.send('可是他们都让我闭嘴...(委屈)')
    else:
        await say_something.send('那你来陪我聊天吧！')

# 开
no_shut_up = on_command('回来吧')
@no_shut_up.handle()
async def _(bot: Bot, event: Event, state: T_State):
    global SHUT_UP
    SHUT_UP = False
    await no_shut_up.send('507bot又回来啦！')


laidian_list = on_command('来点来点')
@laidian_list.handle()
async def _(bot: Bot, event: Event, state: T_State):
    global mes1
    mes = "使用指令【来点 xxx n】可以查看【来点xxx】的第n个内容（从0开始计数）\r\n\
来点指令统计:\r\n"
    last = None
    for each in mes1.keys():
        if '来点' in each:
            if last == mes1[each] or last == None:
                last = mes1[each]
                mes = mes + '【' + str(each) + '】'
                continue
            if np.sum(['record' in e for e in last])!= 0:
                mes = mes + str(len(last)) + '条(含'+ str(np.sum(['record' in e for e in last])) +'条语音)\r\n'
            else:
                mes = mes + str(len(last)) + '条\r\n'
            mes = mes + '【' + str(each) + '】'
            last = mes1[each]
    if np.sum(['record' in e for e in last])!= 0:
        mes = mes + str(len(last)) + '条(含'+ str(np.sum(['record' in e for e in last])) +'条语音)\r\n'
    else:
        mes = mes + str(len(last)) + '条\r\n'
    await laidian_list.send(mes[:-2])
    
laidian = on_command('来点 ')
@laidian.handle()
async def _(bot: Bot, event: Event, state: T_State):
    mes = str(event.get_message()).strip().split()
    k = '来点' + mes[0]
    if k not in mes1.keys():
        await laidian.send('没有【'+k+'】这个条目哦')
        return
    try:
        num = int(mes[1])
    except:
        await laidian.send('请输入正确的数字!如:【来点 鬼叫 2】')
    if num >= len(mes1[k]):
        await laidian.send('【'+k+'】的有效范围为0到'+str(len(mes1[k])-1))
        return
    await laidian.send(Message(mes1[k][num]))

laidian_record = on_command('来点语音')
@laidian_record.handle()
async def _(bot: Bot, event: Event, state: T_State):
    mes = str(event.get_message()).strip()
    if mes not in mes1.keys():
        await laidian_record.send('没有【'+mes+'】这个条目哦')
        return
    record = []
    for each in mes1[mes]:
        if "CQ:record" in each:
            record.append(each)
    if len(record) == 0:
        await laidian_record.send('【'+mes+'】条目下没有语音哦')
    else:
        await laidian_record.send(Message(record[random.randint(0,len(record)-1)]))


###----------------debug
all1 = on_command('全部1', permission=SUPERUSER)
@all1.handle()
async def _(bot: Bot, event: Event, state: T_State):
    mes = str(event.get_message()).strip()
    for each in mes1.keys():
        if each == mes:
            for i in mes1[each]:
                await all1.send(Message(i))
            return

all2 = on_command('全部2', permission=SUPERUSER)
@all2.handle()
async def _(bot: Bot, event: Event, state: T_State):
    mes = str(event.get_message()).strip() 
    for each in mes2.keys():
        if each == mes:
            for i in mes2[each]:
                await all2.send(Message(i))
            return
