from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
import random


plugin_name = 'roll'

@on_command('roll')
async def roll(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    config = np.load('config.npy',allow_pickle=True).item()
    if qqnum in config['black_list'] or config[plugin_name] == False:
        return
    content = str(session.state.get('message') or session.current_arg)
    if content.isdigit():
        num = int(content)
        await session.send('roll点结果：'+str(random.randint(1,num)))
