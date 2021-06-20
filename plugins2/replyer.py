from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
from jieba import posseg
import random
import time
import numpy as np

SHUT_UP = False
AVAILABLE = True
TIMETICK = None
plugin_name = 'replyer'

# 防止和其他机器人复读死循环
def replyBreaker():
    global TIMETICK
    if TIMETICK is None:
        TIMETICK = time.time()
        return False
    tmp = time.time()
    if tmp - TIMETICK >=3:
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
【roll】如"roll 6"\r\n\
【天气】如"天气 上海 浦东"、"天气 广东 番禺"\r\n\
【歌词】如"歌词 生日快乐"\r\n\
【翻译】如"翻译 hello"\r\n\
【运势】如"运势 水瓶座"\r\n\
【学习】"学习 群友发送内容 bot回复内容"\r\n\
【对联】如"对联 一去二三里"\r\n\
【抽象】如"抽象 爬"\r\n\
【百度】如"百度 今天晚上吃什么"\r\n\
【单词】发送"单词"查看相关说明\r\n\
【nlp】发送"nlp xxx"，bot会根据你的发送内容进行智能回复\r\n\
【其他】聊天回复和彩蛋\r\n\
# lu群专属\r\n\
【lulu语录】\r\n\
【来点怪歌】【来点鬼歌】\r\n\
【来点怪叫】【来点鬼叫】\r\n\
# 管理员权限\r\n\
【管理员菜单】查看具体权限指令\r\n\
']
mes1['晚安']=['晚安❤']
mes1['lulu语录']=mes1['るる语录']=['我知道没有单推，但是有点悲伤',
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
           '有一说一，你的胸部确实比我大']
mes2['白学']=mes2['和纱']=mes2['北原']=mes2['东马']=mes2['雪菜']=['白学家能不能爬啊']
mes2['去学习']=mes2['学习去']=mes2['自习']=mes2['考试']=mes2['作业']=mes2['上课']=['这就是国家栋梁吧']
mes1['走']=['当舔狗去了']
mes1['走，当舔狗去了']=['发错了']
mes1['laji爬']=['[CQ:image,file=eba8878b25ceee238d0573cf7dfdfc66.image]',
               '[CQ:image,file=59bc3f42430125462ec6b43e5d65304d.image]',
               '[CQ:image,file=127289e6641331fb0b47ff9dc83cba76.image]',
               '[CQ:image,file=12465c7db97145228946b25a59d7ebf0.image]',
               '[CQ:image,file=f13cfe973df76c8efd14b9870c0c62a5.image]']
mes1['啊哈']=['[CQ:image,file=b44767caa8d4aa597efc5a9e68648739.image]']
mes2['沙口']=['[CQ:image,file=022d7c9f652fe08ff327cb0896ac6fe7.image]',
           '[CQ:image,file=c733da12069ded503549e0cebe6a2fc7.image]',
           '[CQ:image,file=e499e4ba210706b0d7c5a9143053394b.image]']
mes1['差不多得了']=['[CQ:image,file=2a0fdd42c0bcd18a6a0464ea82f3ef88.image]',
           '[CQ:image,file=1818bed4efaf7bec76d0d993530f36ac.image]',
           '[CQ:image,file=ad09b441861102c1dbc10466c6078813.image]',
           '[CQ:image,file=eaa32b3877d064bf7768f303fbde92c7.image]',
           '[CQ:image,file=eaa32b3877d064bf7768f303fbde92c7.image]',
           '[CQ:image,file=b79dee322280db29020e07d9621388f8.image]',
           '[CQ:image,file=042551c00347054df1863f163ffbbf89.image]',
           '[CQ:image,file=c232be760838ded45a508b5be39a1657.image]']
mes1['基本信息']=['项目名称：507bot\r\n出生日期：2021.2.24\r\n\
版本号：v1.0\r\n项目地址：https://github.com/ender507/QQ-Chatting-507-bot\r\n活跃群聊：2']
mes1['你好']=['你好呀','hello word']
mes1['今天吃啥方便面']=['红烧牛肉','老坛酸菜','红油爆椒牛肉','鲜虾鱼板','香菇炖鸡',
           '雪笋肉丝','泡椒牛肉','咖喱海鲜','香浓叉烧','猪骨浓汤']
mes1['mua']=['(脸红)']
mes2['呀，这是火星语吧']=['我翻译得出来！我厉害吧']
mes2['507爬']=['我不爬，要爬你让laji爬']
mes2['507bot爬']=['我不爬，要爬你让laji爬']
mes2['雾宝']= ['雾宝suki♡','雾宝bot在不在？出来陪我玩']
mes2['雾妹']= ['雾宝suki♡','雾宝bot在不在？出来陪我玩']
mes2['二次元']=['[CQ:image,file=de71b50dda7c599a396580a61a172157.image]',
           '[CQ:image,file=38d09555fc3b1957f274e8eee3e08b42.image]',
           '[CQ:image,file=3e61b81bd7b95934d4fd2daf01b1ec73.image]',
           '[CQ:image,file=0526981a0710a622416b4e40355a64e9.image]',
           '[CQ:image,file=8b24d6b2e882f8cd876488a65b101475.image]']
mes2['二刺猿']=mes2['二刺螈']=mes2['二次猿']=mes2['二次元'][:]
mes2['发情']=['他不是一直都在发情吗？']
mes2['里道骸']=mes2['lidaohai']=['里道骸来点○图']
mes2['lly']=['总觉得空气中弥漫着沙口的气息...',
           '[CQ:image,file=21ea8701cd5397784b88bbc7678ab1cf.image]']
mes2['好耶']=['[CQ:image,file=f2275eb773f4521d8df72937526d980e.image]',
           '[CQ:image,file=5fd4239c09d03a9b20ab926dc5473adf.image]',
           '[CQ:image,file=21c8c55ec019c29814745a720f404827.image]',
           '[CQ:image,file=df646dbbe5d0e2db07d11017fb4e78be.image]']
mes2['色图']=mes2['涩图']=mes2['渋図']=mes2['ghs']=['[CQ:image,file=1f9f3c6a2d137a55b69e120d59cf56a8.image]',
           '[CQ:image,file=a175367a819da572887e6ae198b9e26e.image]',
           '[CQ:image,file=bc89f2ff230b116e4b2b36222436b889.image]']
mes3.append("不许ghs！（半恼）")
mes3.append("雾宝来啦")
mes2['学不完']=['已经是国家栋梁了']
mes1['来点油条']=mes1['来点老油条']=['[CQ:image,file=ecf9738224c8e25f319a9b85ac4613ca.image]',
           '[CQ:image,file=e50acb3582b4c8c57e5b096662725d00.image]',
           '[CQ:image,file=1900fc2b6eefbe9175f68e74a0498da9.image]',
           '[CQ:image,file=3d1a1b75ad119f7f47032077c31026a6.image]']
mes1['来点柚子']=mes1['来点yozuki']=['[CQ:image,file=aeee125d0cb170346b0584e4e57f6e06.image]',
           '[CQ:image,file=5ec7eea91e1fd1d13dc26e7586667ef1.image]',
           '[CQ:image,file=df57ecf1d20d4880aa85215ca0a7e9b8.image]',
           '[CQ:image,file=645e6df1564fec46daf536801434990d.image]']
mes1['来点红炎']=mes1['来点炎子哥']=['[CQ:image,file=c457ec6602c3d43bebe608c351cd42d8.image]']
mes1['来点507']=['[CQ:image,file=bac9be5aaa59bb7e2e29fde1597c7231.image]',
           '[CQ:image,file=645e6df1564fec46daf536801434990d.image]']
mes1['来点rikka']=['[CQ:image,file=b1b5cbb6bd317e89d1abbab9b3f4a330.image]']
mes1['来点雾宝']=mes1['来点雾妹']=['[CQ:image,file=9acce5f52b9545074940075070560547.image]']
mes1['来点鸭子']=mes1['来点鸭子哥']=['[CQ:image,file=8894332504c45648e585ed175b11ebee.image]']
mes1['来点laji']=mes1['来点垃圾']=['[CQ:image,file=efb02f943c0387c6103f4b0d1a9d5053.image]',
           '[CQ:image,file=6f6f6bf83f8d729e1ceb16ddbe9c9b07.image]',
           '[CQ:image,file=78590e0a6969a1cbd3a32d9e5dc729dd.image]',
           '[CQ:image,file=8acc1a6e78df6df45642a39e53d8b3b7.image]',
           '[CQ:image,file=7f9f0fd41115a2802bbc65488554bb8b.image]']
mes1['来点馨妹']=mes1['来点白神馨']=['[CQ:image,file=78590e0a6969a1cbd3a32d9e5dc729dd.image]',
           '[CQ:image,file=fc26c0cc800159c92858189385bb2e7f.image]']




mes=""
@on_natural_language(keywords=mes1.keys())
async def _(session: NLPSession):
    message = str(session.ctx['message'])
    global mes, mes1, mes3
    for each in mes3:
        if each in message:
            return None
    for each in mes1.keys():
        if each == message:
            mes = each
            break
    return IntentCommand(100.0, 'sendMes1')

@on_natural_language(keywords=mes2.keys())
async def _(session: NLPSession):
    message = str(session.ctx['message'])
    global mes, mes2, mes3
    for each in mes3:
        if each in message:
            return None
    for each in mes2.keys():
        if each in message:
            mes = each
            break
    return IntentCommand(100.0, 'sendMes2')

@on_command('sendMes1')
async def sendMes(session: CommandSession):
    global mes1, mes
    qqnum=str(session.ctx['user_id'])
    config = np.load('config.npy',allow_pickle=True).item()
    if qqnum in config['black_list'] or config[plugin_name] == False:
        return
    global SHUT_UP
    if SHUT_UP or replyBreaker():
        return
    await session.send(mes1[mes][random.randint(0,len(mes1[mes])-1)])


@on_command('sendMes2')
async def sendMes(session: CommandSession):
    global mes2, mes
    qqnum=str(session.ctx['user_id'])
    config = np.load('config.npy',allow_pickle=True).item()
    if qqnum in config['black_list'] or config[plugin_name] == False:
        return
    global SHUT_UP
    if SHUT_UP or replyBreaker():
        return
    await session.send(mes2[mes][random.randint(0,len(mes2[mes])-1)])


#---------------------------------------------------------------------------
# 以下是不需要权限的开关

# 关
@on_command('闭嘴')
async def shutup(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    config = np.load('config.npy',allow_pickle=True).item()
    if qqnum in config['black_list'] or config[plugin_name] == False:
        return
    global SHUT_UP
    SHUT_UP = True
    await session.send('唔——唔——')

# 查
@on_command('saysomething')
async def saysomething(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    config = np.load('config.npy',allow_pickle=True).item()
    if qqnum in config['black_list'] or config[plugin_name] == False:
        return
    global SHUT_UP
    if SHUT_UP:
        await session.send('可是他们都让我闭嘴...(委屈)')
    else:
        await session.send('那你来陪我聊天吧！')

# 开
@on_command('noshutup')
async def noshutup(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    config = np.load('config.npy',allow_pickle=True).item()
    if qqnum in config['black_list'] or config[plugin_name] == False:
        return
    global SHUT_UP
    SHUT_UP = False
    await session.send('507bot又回来啦！')


@on_natural_language(keywords={'回来吧'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'noshutup')

@on_natural_language(keywords={'说话啊'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'saysomething')
