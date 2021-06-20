import base64

from nonebot import CommandSession, on_command
import numpy as np

__plugin_name__ = 'lmbtfy(帮你百度)'
__plugin_usage__ = r"""
Let Me Baidu That For You.
好消息！本机器人已与百度达成合作关系，今后大家有什么不懂的可以直接让我帮你百度一下！
网站由 tool.mkblog.cn/lmbtfy/ 提供
Command(s):
 - /lmbtfy [搜索关键词]
   生成「帮你百度」网址
""".strip()

from nonebot.command.argfilter.controllers import handle_cancellation
from nonebot.command.argfilter.extractors import extract_text

plugin_name = 'baidu'


@on_command('百度')
async def lmbtfy(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    config = np.load('config.npy',allow_pickle=True).item()
    if qqnum in config['black_list'] or config[plugin_name] == False:
        return
    keyword = session.get('keyword', prompt="请输入关键词", arg_filters=[handle_cancellation(session),extract_text])
    await session.send("你的问题很简单，让我告诉你:\n"
                       'http://tool.mkblog.cn/lmbtfy/?q=' + str(base64.b64encode(keyword.encode('utf-8')))[2:-1])

@lmbtfy.args_parser
async def _(session: CommandSession):
    arg = session.current_arg.strip()

    if session.is_first_run:
        if not arg:
            return

        session.state['keyword'] = arg

    if not arg:
        session.pause('请输入关键词')

    session.state[session.current_key] = arg
