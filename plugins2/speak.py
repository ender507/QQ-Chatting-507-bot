from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
import requests
import json
import numpy as np

plugin_name='speak'

@on_command('说话')
async def learn(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    config = np.load('config.npy',allow_pickle=True).item()
    if qqnum in config['black_list'] or config[plugin_name] == False:
        return
    mes = str(session.state.get('message') or session.current_arg)
    await session.send('[CQ:tts,text='+mes+']')
