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
【歌词】如"歌词 生日快乐"\r\n\
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
版本号：v1.0\r\n项目地址：\r\n\
github地址：https://github.com/ender507/QQ-Chatting-507-bot\r\n\
gitee地址：https://gitee.com/ender507/QQ-Chatting-507-bot\r\n\
活跃群聊：2']
mes1['你好']=['你好呀','hello word']
mes1['今天吃啥方便面']=['红烧牛肉','老坛酸菜','红油爆椒牛肉','鲜虾鱼板','香菇炖鸡',
           '雪笋肉丝','泡椒牛肉','咖喱海鲜','香浓叉烧','猪骨浓汤']
mes1['mua']=['(脸红)']
mes2['呀，这是火星语吧']=['我翻译得出来！我厉害吧']
mes2['507爬']=['我不爬，要爬你让laji爬']
mes2['507bot爬']=['我不爬，要爬你让laji爬']
mes2['二次元']=['[CQ:image,file=de71b50dda7c599a396580a61a172157.image]',
           '[CQ:image,file=38d09555fc3b1957f274e8eee3e08b42.image]',
           '[CQ:image,file=3e61b81bd7b95934d4fd2daf01b1ec73.image]',
           '[CQ:image,file=0526981a0710a622416b4e40355a64e9.image]',
           '[CQ:image,file=8b24d6b2e882f8cd876488a65b101475.image]',
             '']
mes2['二刺猿']=mes2['二刺螈']=mes2['二次猿']=mes2['二次元'][:]
mes2['发情']=['他不是一直都在发情吗？']
mes2['里道骸']=mes2['lidaohai']=['里道骸来点○图']
mes1['来点lly']=['[CQ:image,file=21ea8701cd5397784b88bbc7678ab1cf.image]',
             '[CQ:image,file=60f46c7e7e7cf55514a2b446707b1190.image]']
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
           '[CQ:image,file=3d1a1b75ad119f7f47032077c31026a6.image]',
            '[CQ:image,file=be2ffc3a403bf985714dc3a6bc3195b0.image]',
            '[CQ:image,file=bad2f6e3c0b79d3c6e5e92ac256c334e.image]',
            '[CQ:image,file=d71e1c83604b5f4221839525789d13e1.image]']
mes1['来点柚子']=mes1['来点yozuki']=['[CQ:image,file=aeee125d0cb170346b0584e4e57f6e06.image]',
           '[CQ:image,file=5ec7eea91e1fd1d13dc26e7586667ef1.image]',
           '[CQ:image,file=df57ecf1d20d4880aa85215ca0a7e9b8.image]',
           '[CQ:image,file=645e6df1564fec46daf536801434990d.image]',
            '[CQ:image,file=61ced67febb41dbe55da099ba70a2d58.image]',
            '[CQ:image,file=b08904b23d21ae70eda675007f79b76f.image]',
            '[CQ:image,file=0b5618891e137ead98bd071db5350aef.image]',
            '[CQ:image,file=979c39e6e1235201a09beadded6b0978.image]',
            '[CQ:image,file=6e17aa908a42db523c4b2edc08c72522.image]']
mes1['来点红炎']=mes1['来点炎子哥']=['[CQ:image,file=a0f818ba85eb523c5e537b490224112d.image]',
                            '[CQ:image,file=de7376611c199da2e8a38c006465e1bb.image]',
                            '[CQ:image,file=4999fc8e743681d89c6143c47a65bade.image]']
mes1['来点crylins']=mes1['来点cryl1ns']=mes1['来点cry']=['[CQ:image,file=6e006bcdcad3e1d41a913882c11c43ac.image]',
 '[CQ:image,file=78a27dab046095f69be8cd52107b6839.image]',
 '[CQ:image,file=17c74ada500505168d02d30a411fac9c.image]',
'[CQ:image,file=b17cac47480f4f80e2b4bf20103a4e30.image]']
mes1['来点507']=['[CQ:image,file=bac9be5aaa59bb7e2e29fde1597c7231.image]',
           '[CQ:image,file=645e6df1564fec46daf536801434990d.image]',
               '[CQ:image,file=7f330cd493ca8801d949076f0bd0fc91.image]',
               '[CQ:image,file=41b7e135e6421299490e0ed574698aaf.image]',
               '[CQ:image,file=068f8638ed1513a49ffbf0ab35fae935.image]']
mes1['来点rikka']=['[CQ:image,file=b1b5cbb6bd317e89d1abbab9b3f4a330.image]',
                 '[CQ:image,file=8469e90cf15b2ef5057df46e50d7b47b.image]',
                 '[CQ:image,file=4f00bc1e50b5cfceb63ec2c3fafb892e.image]',
                 '[CQ:image,file=c85c7ab904857a4f10490c40fd47daf2.image]',
                 '[CQ:image,file=34a3a85f562345fd13e1ae35cdf6df4c.image]']
mes1['来点雾宝']=mes1['来点雾妹']=['[CQ:image,file=fdf285102fd20d06d47cd5f1298c36e9.image]',
                           '[CQ:image,file=50ffabd0f461b1fb156b3344f1e1afcf.image]']
mes1['来点鸭子']=mes1['来点鸭子哥']=['[CQ:image,file=8894332504c45648e585ed175b11ebee.image]',
                            '[CQ:image,file=26e146bdc56279fc6de20cb518d0fd67.image]']
mes1['来点laji']=mes1['来点垃圾']=['[CQ:image,file=efb02f943c0387c6103f4b0d1a9d5053.image]',
           '[CQ:image,file=6f6f6bf83f8d729e1ceb16ddbe9c9b07.image]',
           '[CQ:image,file=78590e0a6969a1cbd3a32d9e5dc729dd.image]',
           '[CQ:image,file=8acc1a6e78df6df45642a39e53d8b3b7.image]',
           '[CQ:image,file=7f9f0fd41115a2802bbc65488554bb8b.image]',
            '[CQ:image,file=40f32c3a10d1a467cdb7a9a5a80d3c74.image]']
mes1['来点馨妹']=mes1['来点白神馨']=['[CQ:image,file=78590e0a6969a1cbd3a32d9e5dc729dd.image]',
           '[CQ:image,file=ddf16954f4f3c680776a59fe86e5e5fc.image]',
                            '[CQ:image,file=29617c66e8b8e051bff5b8b68a6872e0.image]',
                            '[CQ:image,file=3f822706576691ec2b6bf49c03146619.image]']
mes1['来点母鸡']=mes1['来点母狗']=mes1['来点母鸡太太']=mes1['来点母狗太太']=[
'[CQ:image,file=72f33262b1e1383286f7f829adf18418.image]',
'[CQ:image,file=ba03b01b4d50a7f5d1dc77020ca2d407.image]',
'[CQ:image,file=17c74ada500505168d02d30a411fac9c.image]']
mes1['来点盒子']=mes1['来点hezzi']=mes1['来点HezZi']=['[CQ:image,file=c86452dabcc7d736576839ac8eb7a045.image]',
                                '[CQ:image,file=bd687e790933b04b759b2b1fbc327480.image]']
mes2['嘉然']=mes2['然然']=['[CQ:image,file=0663139220cb104eb7b36182ffd0a74a.image]',
                       '[CQ:image,file=75e5ae9906a7f82cb2fc3ff8794634f4.image]',
                       '[CQ:image,file=7a41cc36cd61ba4bc2cd1c60d308a2b6.image]',
                       '[CQ:image,file=5007ab1ebf0e866cf308acae86e812a6.image]',
                       '[CQ:image,file=b050bfa2eae63bf3d4e76cb566a8e454.image]',
                       '[CQ:image,file=c87684a7950b52d6e94aed397dea502c.image]']
mes1['来点CL']=mes1['来点cl']=['[CQ:image,file=c5758c577a3837ff8b8ea06739b09528.image]']
mes1['来点yasuki']=['[CQ:image,file=e88bc0d070b361f5502a122b4c33eb02.image]',
                  '[CQ:image,file=119b2d5bdef9d98722bd06051d94ca0b.image]']
mes1['来点akira']=['[CQ:image,file=38e41e0afb0f5bc19e78dbf5c6bcbde4.image]']
mes1['来点wx']=['[CQ:image,file=126de23e7368f8776a9348d9eaf315c5.image]']
mes1['来点莲宝']=['[CQ:image,file=e8fb35be162b0a6f25f312dbaf5d9d60.image]',
              '[CQ:image,file=a721ba862faa1b1836c3ea8e98ad87ec.image]']
mes1['来点mana']=['[CQ:image,file=39d55a18adb3a8296376edbae045e744.image]']
mes1['来点疫苗']=['[CQ:image,file=0db70e727eb9b5f05982f7a320f0d5f0.image]']
mes1['来点as']=['[CQ:image,file=543ebeec0aff30f2d3d0a9f40fe8a917.image]']
mes1['来点吴京']=['[CQ:image,file=7df5bbf912ca9c3b4443c27dd4f16a46.image]',
              '[CQ:image,file=12427d236cc6c90e012224624232fa3d.image]']
mes1['来点阿喵喵']=['[CQ:image,file=58ac5da441ae78445763895a165b39f0.image]',
               '[CQ:image,file=8a865a8246ce8ad3e3af5c5fbe197b13.image]']
mes2['三点']=['[CQ:image,file=4ff600edab13efb8070e3a2f87b873b9.image]',
            '[CQ:image,file=ee6a2e5727065aeff35e4c96d5153d48.image]']
mes1['来点黄金船']=['[CQ:image,file=dd633e108918c721939b7a5280b2f1cc.image]']
mes2['审核']=['[CQ:image,file=bd5080b2b0087d7146ff7617a0fbde46.image]']
mes1['来点小舞']=['[CQ:image,file=8814e7ab87911820613b7cb2a044ef4c.image]',
              ' [CQ:image,file=85fe02d402f75fcdada6ed1c3b080ccd.image]']
mes1['来点谢拉']=['[CQ:image,file=6f956c8641c85b9f7eca7aa35da32c31.image]',
              '[CQ:image,file=f6067abbf685c008f8a8ffefeafc16b2.image]']
mes1['来点hentai']=['[CQ:image,file=a90b2a0c3fdd580d89a2f9e71ff6a375.image]',
                  '[CQ:image,file=0781d404926a30046bc1cc0fc6dc6a1c.image]']
mes1['来点加菲猫']=['[CQ:image,file=c76423016d3129deffcfdea417a8cb0f.image]']


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
            return IntentCommand(100.0, 'sendMes1')
    return None

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
            return IntentCommand(100.0, 'sendMes2')
    return None

@on_command('sendMes1')
async def sendMes1(session: CommandSession):
    global mes1, mes
    qqnum=str(session.ctx['user_id'])
    config = np.load('config.npy',allow_pickle=True).item()
    if qqnum in config['black_list'] or config[plugin_name] == False:
        return
    global SHUT_UP
    if SHUT_UP or replyBreaker(5):
        return
    await session.send(mes1[mes][random.randint(0,len(mes1[mes])-1)])


@on_command('sendMes2')
async def sendMes2(session: CommandSession):
    global mes2, mes
    qqnum=str(session.ctx['user_id'])
    config = np.load('config.npy',allow_pickle=True).item()
    if qqnum in config['black_list'] or config[plugin_name] == False:
        return
    global SHUT_UP
    if SHUT_UP or replyBreaker(10):
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
