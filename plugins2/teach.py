from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
import requests
import json
import numpy as np

plugin_name='teach'

@on_command('学习')
async def learn(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    config = np.load('config.npy',allow_pickle=True).item()
    if qqnum in config['black_list'] or config[plugin_name] == False:
        return
    mes = str(session.state.get('message') or session.current_arg).split()
    if len(mes) != 2:
        await session.send('不符合格式要求！请在消息和回复之间用空格隔开')
        return
    reply = mes[1]
    mes = mes[0]
    await session.send('明白了！在有群友说“'+mes+'”时我应该回复“'+reply+'”')
    await session.send('上述内容会交由507审核，通过后507bot就能实装啦！')
    with open('plugins\\learn_log.txt','a') as f:
        f.write(mes+' '+reply+'\n')
        
