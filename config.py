from nonebot.default_config import *

SUPERUSERS = {1419626179}
COMMAND_START = {''}
NICKNAME = {''}


# 当对话API无返回结果时的输出
EXPR_DONT_UNDERSTAND = (
    '您搁那说啥呢...',
    '啥玩意？',
    '其实我不太明白你的意思……'
)

# 对话API平台选择 ('tencent' / 'itpk' / '')
# 若为 '' 则不启用对话功能
NLP_API = 'itpk'


# [可选]腾讯AI开发平台(https://ai.qq.com/)对话API
TENCENT_APP_ID = ''
TENCENT_APP_KEY = ''

# [可选]茉莉机器人(http://www.itpk.cn/)对话API [不填也可调用]
ITPK_API_KEY = '86b7f3a08e1923c02726146d222bb2b0'
ITPK_APT_SECRET = '23kjlsify7ys'
