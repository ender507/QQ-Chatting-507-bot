from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
from jieba import posseg
import random
import time
 
FIRST_BOOT = True
SHUT_UP = False
AVAILABLE = True

BLACK_LIST = []

TIMETICK = None
# 防止和其他机器人复读死循环
def replyBreaker():
    global TIMETICK
    if TIMETICK is None:
        TIMETICK = time.time()
        return True
    tmp = time.time()
    if tmp - TIMETICK >=3:
        TIMETICK = tmp
        return False
    return True

@on_command('test', permission=SUPERUSER)
async def test(session: CommandSession):
    global AVAILABLE
    AVAILABLE = True
    await session.send('')

@on_command('cmd启用', permission=SUPERUSER)
async def cmdSetUp(session: CommandSession):
    global AVAILABLE
    AVAILABLE = True
    await session.send('cmd已启用！来和507bot聊天吧')

@on_command('cmd禁用', permission=SUPERUSER)
async def cmdShutDown(session: CommandSession):
    global AVAILABLE
    AVAILABLE = False
    await session.send('cmd禁用了...讨厌和507bot聊天吗？')

@on_command('cmd黑名单', permission=SUPERUSER)
async def cmdBlackListPush(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if uid in BLACK_LIST:
        await session.send('这个人已经在cmd黑名单里了')
    elif '1419626179' in uid:
        await session.send('我才不会把507加到黑名单里呢！')
    else:
        BLACK_LIST.append(uid)
        await session.send(uid+'的cmd功能已禁用')

@on_command('cmd出狱', permission=SUPERUSER)
async def cmdBlackListPop(session: CommandSession):
    uid = str(session.state.get('message') or session.current_arg)
    if uid == '鸭子哥':
        uid = '1292719501'
    global BLACK_LIST
    if '1419626179' in uid:
        await session.send('507怎么可能在黑名单里呢！')
    if uid not in BLACK_LIST:
        await session.send('这个人不在cmd黑名单里哦')
    else:
        for i in range(len(BLACK_LIST)):
            if uid in BLACK_LIST[i] or BLACK_LIST[i] in uid:
                del BLACK_LIST[i]
                break
        await session.send(uid+'的cmd功能已启用')

@on_command('憨憨bot')
async def hhbot(session: CommandSession):
    if replyBreaker():
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('[CQ:image,file=b600be26d6aa1cb557135bbed16ed1bf.image]')

@on_command('lulu语录')
async def _(session: CommandSession):
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    mes = ['我知道没有单推，但是有点悲伤',
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
    await session.send(mes[random.randint(0,len(mes)-1)])


@on_command('白学')
async def _(session: CommandSession):
    if replyBreaker():
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('白学家能不能爬啊')

@on_command('去学习')
async def _(session: CommandSession):
    if replyBreaker():
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('这就是国家栋梁吧')

@on_command('走')
async def shakou(session: CommandSession):
    if replyBreaker():
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('当舔狗去了')

@on_command('走，当舔狗去了')
async def shakou(session: CommandSession):
    if replyBreaker():
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('发错了')

@on_command('lajipa', aliases=('laji爬', 'lajibot爬'))
async def lajipa(session: CommandSession):
    if replyBreaker():
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    #await session.send('[CQ:image,file=eba8878b25ceee238d0573cf7dfdfc66.image]')
    #await session.send('[CQ:image,file=59bc3f42430125462ec6b43e5d65304d.image]')
    await session.send('[CQ:image,file=127289e6641331fb0b47ff9dc83cba76.image]')

@on_command('啊哈')
async def aha(session: CommandSession):
    if replyBreaker():
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('[CQ:image,file=b44767caa8d4aa597efc5a9e68648739.image]')

@on_command('shakou')
async def shakou(session: CommandSession):
    if replyBreaker():
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('[CQ:image,file=c733da12069ded503549e0cebe6a2fc7.image]')

@on_command('差不多得了')
async def chabuduodele(session: CommandSession):
    if replyBreaker():
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('[CQ:image,file=1818bed4efaf7bec76d0d993530f36ac.image]')

    
@on_command('基本信息')
async def info(session: CommandSession):
    if replyBreaker():
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send('项目名称：507bot\r\n出生日期：2021.2.24\r\n\
版本号：v0.7\r\n项目地址：https://github.com/ender507/QQ-Chatting-507-bot\r\n活跃群聊：2')

@on_command('说', permission=SUPERUSER)
async def say(session: CommandSession):
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    await session.send(session.state.get('message') or session.current_arg)

@on_command('shutup')
async def shutup(session: CommandSession):
    global AVAILABLE
    if not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global SHUT_UP
    SHUT_UP = True
    await session.send('唔——唔——')


@on_command('你好')
async def hello(session: CommandSession):
    if replyBreaker():
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    if random.randint(0,10) == 10:
        await session.send('Hello World!')
    else:
        await session.send('你好呀')

@on_command('mua')
async def mua(session: CommandSession):
    if replyBreaker():
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    await session.send('(脸红)')

    
@on_command('touchhead')
async def touchhead(session: CommandSession):
    if replyBreaker():
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    reply = ["嘻嘻，好痒啊w","好舒服w"]
    await session.send(reply[random.randint(0,1)])

@on_command('saysomething')
async def shutup(session: CommandSession):
    global AVAILABLE
    if not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global SHUT_UP
    if SHUT_UP:
        await session.send('可是他们都让我闭嘴...(委屈)')
    else:
        await session.send('那你来陪我聊天吧！')

@on_command('noshutup')
async def noshutup(session: CommandSession):
    global AVAILABLE
    if not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global SHUT_UP
    SHUT_UP = False
    await session.send('507bot又回来啦！')

@on_command('507bot')
async def bot(session: CommandSession):
    if replyBreaker():
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global FIRST_BOOT
    if FIRST_BOOT:
        await session.send('507bot来啦')
        FIRST_BOOT = False
        return
    mes = '我是507bot！我的常用指令：\r\n\
【roll】接数字，roll点\r\n\
【天气】接省份和城市，查询实时天气状况\r\n\
【歌词】接曲名，查询歌词（因易刷屏暂未开放）\r\n\
【翻译】中译英或其他语种译中\r\n\
【运势】接星座，依据星座查看当日运势\r\n\
【学习】接群友发送内容和bot回复内容，让bot学习新知识\r\n\
【对联】接上联，bot回复下联\r\n\
【明日方舟抽卡】抽卡模拟器\r\n\
【bot管理相关（需要权限）】开启/移除功能模块、终止、黑名单\r\n\
【其他】聊天回复和彩蛋\r\n\
需要向507反馈问题请使用【学习】功能，让bot记录反馈内容'
    await session.send(mes)

@on_command('climb')
async def climb(session: CommandSession):
    if replyBreaker():
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    await session.send('我不爬，要爬你让laji爬')

@on_command('hiiro')
async def hiiro(session: CommandSession):
    if replyBreaker():
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    await session.send('hiiro debu')

@on_command('wubao')
async def wubao(session: CommandSession):
    if replyBreaker():
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    reply = ['雾宝suki♡','雾宝bot在不在？出来陪我玩']
    await session.send(reply[random.randint(0,1)])
    
@on_command('ero')
async def ero(session: CommandSession):
    if replyBreaker():
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    await session.send('[CQ:image,file=1f9f3c6a2d137a55b69e120d59cf56a8.image]')

@on_command('block')
async def block(session: CommandSession):
   pass
    
@on_command('chaofeng')
async def chaofeng(session: CommandSession):
    if replyBreaker():
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    await session.send('我翻译得出来！我厉害吧')

@on_command('_lulu')
async def lulu(session: CommandSession):
    if replyBreaker():
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    await session.send('るる是谁？有507bot可爱吗')


@on_command('laji爬小助手')
async def _(session: CommandSession):
    if replyBreaker():
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    await session.send('【laji爬小助手】大家好，我是本群laji爬小助手\r\n希望看到这条消息的群友和我一起让laji爬')

@on_command('rut')
async def rut(session: CommandSession):
    if replyBreaker():
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    await session.send('他不是一直都在发情吗？')

@on_command('lidaohai')
async def shakou(session: CommandSession):
    if replyBreaker():
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    await session.send('里道骸来点○图')

@on_command('lly')
async def lly(session: CommandSession):
    if replyBreaker():
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    await session.send('总觉得空气中弥漫着沙口的气息...')

@on_command('好耶')
async def good(session: CommandSession):
    if replyBreaker():
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    await session.send('[CQ:image,file=f2275eb773f4521d8df72937526d980e.image]')

@on_command('love')
async def love(session: CommandSession):
    if replyBreaker():
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    global SHUT_UP
    global AVAILABLE
    if SHUT_UP or not AVAILABLE:
        return
    await session.send('我也爱你哦❥（仅代表机器人个人，不代表bot主人观点）')

@on_command('roll')
async def roll(session: CommandSession):
    global AVAILABLE
    if not AVAILABLE:
        return
    qqnum=str(session.ctx['user_id'])
    global BLACK_LIST
    if qqnum in BLACK_LIST:
        return
    content = str(session.state.get('message') or session.current_arg)
    if content.isdigit():
        num = int(content)
        await session.send('roll点结果：'+str(random.randint(1,num)))
    

@on_natural_language(keywords={'507爬', '507bot爬','507能不能爬','507bot能不能爬'})
async def _(session: NLPSession):
    # 前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(100.0, 'climb')

@on_natural_language(keywords={'507bot'})
async def _(session: NLPSession):
    return IntentCommand(100.0, '507bot')

@on_natural_language(keywords={'507我爱你', '507bot我爱你','507 我爱你','507bot 我爱你',
                               '507我喜欢你', '507bot我喜欢你','507 我喜欢你','507bot 我喜欢你'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'love')

@on_natural_language(keywords={'色图','涩图','渋図','ghs'})
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()
    if "不许ghs！（半恼）" in str(stripped_msg):
        return IntentCommand(100.0, 'block')
    return IntentCommand(100.0, 'ero')


#@on_natural_language(keywords={'lulu','るる'})
#async def _(session: NLPSession):
#    if random.randint(0,2) != 0:
#        return IntentCommand(100.0, 'block')
#    return IntentCommand(100.0, '_lulu')


@on_natural_language(keywords={'呀，这是火星语吧'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'chaofeng')

@on_natural_language(keywords={'雾宝','雾妹'})
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()
    if "雾宝来啦" in str(stripped_msg):
        return IntentCommand(100.0, 'block')
    if random.randint(0,2) != 0:
        return IntentCommand(100.0, 'block')
    return IntentCommand(100.0, 'wubao')

@on_natural_language(keywords={'hiiro'})
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()
    if "来点hiiro" in str(stripped_msg):
        return IntentCommand(100.0, 'block')
    return IntentCommand(100.0, 'hiiro')

@on_natural_language(keywords={'闭嘴'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'shutup')

@on_natural_language(keywords={'回来吧'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'noshutup')

@on_natural_language(keywords={'说话啊'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'saysomething')

@on_natural_language(keywords={'沙口'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'shakou')

@on_natural_language(keywords={'差不多得了'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'chabuduodele')

@on_natural_language(keywords={'摸摸头'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'touchhead')

@on_natural_language(keywords={'mua'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'mua')

@on_natural_language(keywords={'又发情'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'rut')

@on_natural_language(keywords={'里道骸','ldh'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'lidaohai')

@on_natural_language(keywords={'lly'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'lly')

@on_natural_language(keywords={'现在是'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'laji爬小助手')

@on_natural_language(keywords={'lulu语录','るる语录'})
async def _(session: NLPSession):
    return IntentCommand(100.0, 'lulu语录')

@on_natural_language(keywords={'去学习'})
async def _(session: NLPSession):
    return IntentCommand(100.0, '去学习')

@on_natural_language(keywords={'和纱','北原','东马','雪菜','白学'})
async def _(session: NLPSession):
    return IntentCommand(100.0, '白学')
