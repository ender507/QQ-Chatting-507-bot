from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
import random
import numpy as np

plugin_name = 'record'

record_list = dict()
record_list['666']=['[CQ:record,file=666.amr]']
record_list['六六六']=['[CQ:record,file=666.amr]']
record_list['az']=['[CQ:record,file=az.amr]']
record_list['啊这']=['[CQ:record,file=az.amr]']
record_list['谢谢']=['[CQ:record,file=xiexie.amr]']
record_list['谢']=['[CQ:record,file=xiexie.amr]']
record_list['菜']=['[CQ:record,file=cai.amr]']
record_list['来点鬼叫']=['[CQ:record,file=guaijiao1.amr]',
                     '[CQ:record,file=guaijiao2.amr]',
                     '[CQ:record,file=guaijiao3.amr]',
                     '[CQ:record,file=guaijiao4.amr]',
                     '[CQ:record,file=guaijiao5.amr]',
                     '[CQ:record,file=guaijiao6.amr]',
                     '[CQ:record,file=guaijiao7.amr]',
                     '[CQ:record,file=guaijiao8.amr]',
                     '[CQ:record,file=guaijiao9.amr]',
                     '[CQ:record,file=guaijiao10.amr]']
record_list['来点怪叫']=record_list['来点鬼叫'][:]
record_list['来点鬼歌']=['[CQ:record,file=g1.amr]',
                     '[CQ:record,file=g2.amr]',
                     '[CQ:record,file=g3.amr]',
                     '[CQ:record,file=g4.amr]',
                     '[CQ:record,file=g5.amr]',
                     '[CQ:record,file=g6.amr]',
                     '[CQ:record,file=g7.amr]',
                     '[CQ:record,file=g8.amr]',
                     '[CQ:record,file=g9.amr]',
                     '[CQ:record,file=g10.amr]']
record_list['来点怪歌']=record_list['来点鬼歌'][:]
record_list['怎么办']=['[CQ:record,file=zenmeban1.amr]',
                    '[CQ:record,file=zenmeban2.amr]']
record_list['绝了']=['[CQ:record,file=juele.amr]']
record_list['别走']=['[CQ:record,file=biezou.amr]']
record_list['nice']=['[CQ:record,file=nice.amr]']
record_list['奈斯']=['[CQ:record,file=nice.amr]']
record_list['求饶']=['[CQ:record,file=qiurao.amr]']
record_list['这波']=['[CQ:record,file=zhebo.amr]']

mes = ""

@on_command('record')
async def rcd(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    config = np.load('config.npy',allow_pickle=True).item()
    if qqnum in config['black_list'] or config[plugin_name] == False:
        return
    global mes, record_list
    await session.send(record_list[mes][random.randint(0,len(record_list[mes])-1)])

@on_natural_language(keywords=record_list.keys())
async def _(session: NLPSession):
    message = str(session.ctx['message'])
    global mes, record_list
    for each in record_list.keys():
        if each in message:
            mes = each
            break
    return IntentCommand(100.0, 'record')




