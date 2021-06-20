'''管理员功能'''
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
import os
import shutil
import numpy as np
    

@on_command('管理员菜单', permission=SUPERUSER)
async def explosion(session: CommandSession):
    mes = "\
圆括号内表示要输入的内容\r\n\
【管理员菜单】呼出本菜单\r\n\
【自爆】关闭bot\r\n\
【说】复读和发送CQ码\r\n\
【黑名单 查】同'查','查看','查询','list'\r\n\
【黑名单 增 (qq号)】同'增','新增','添加','加入','新加','+'\r\n\
【黑名单 删 (qq号)】同'删','删除','去除','移除','-'\r\n\
【模块 查】同'查','查看','查询','list','dir','ls'\r\n\
【模块 状态 (模块名)】查看模块开关状态\r\n\
【模块 开 (模块名)】同'开启','开','on'\r\n\
【模块 关 (模块名)】同'关闭','关','off'\
"
    await session.send(mes)


# 直接退出从而关闭程序
@on_command('自爆', permission=SUPERUSER)
async def explosion(session: CommandSession):
    await session.send('啊我死了')
    await session.send('[CQ:record,file=zibao.amr]')
    exit(0)



# 复读，如"说 你好"会回复"你好"
# 可以接CQ码，如"说 [CQ:image,file=xxx]"
@on_command('说', permission=SUPERUSER)
async def say(session: CommandSession):
    mes = str(session.state.get('message') or session.current_arg)
    ans = ""
    # 将QQ消息的方括号转义给转回来，从而解析CQ码
    if mes[:5] == '&#91;':
        ans += '['
        ans += mes[5:-5]
        ans += ']'
    else:
        ans = mes
    await session.send(ans)



# 黑名单
@on_command('黑名单', permission=SUPERUSER)
async def say(session: CommandSession):
    mes = str(session.state.get('message') or session.current_arg).split()
    # 增
    if mes[0] in ['增','新增','添加','加入','新加','+']:
        config = np.load('config.npy',allow_pickle=True).item()
        if str(mes[1]) in config['black_list']:
            await session.send(mes[1]+'已经在黑名单中了')
            return
        config['black_list'].add(str(mes[1]))
        np.save('config.npy', config)
    # 删
    elif mes[0] in ['删','删除','去除','移除','-']:
        config = np.load('config.npy',allow_pickle=True).item()
        if str(mes[1]) not in config['black_list']:
            await session.send(mes[1]+'已经在黑名单中了')
            return
        config['black_list'].remove(str(mes[1]))
        np.save('config.npy', config)
    # 查
    elif mes[0] in ['查','查看','查询','list']:
        if len(config['black_list']) == 0:
            await session.send('当前黑名单为空')
            return
        reply_mes = '当前黑名单：'
        for each_qq in config['black_list']:
            reply_mes = reply_mes + '【' + str(each_qq) + '】'
            await session.send('reply_mes')
    else:
        await session.send('未知参数：【'+mes[0]+'】\r\n试试【新增】、【删除】或【查看】？')



# 模块管理
@on_command('模块', permission=SUPERUSER)
async def explosion(session: CommandSession):
    mes = str(session.state.get('message') or session.current_arg).split()
    config = np.load('config.npy',allow_pickle=True).item()
    # 查询全部模块
    if mes[0] in ['查','查看','查询','list','dir','ls']:
        reply_mes = '当前载入的模块包含:'
        for each_plugin in config['plugins']:
            reply_mes = reply_mes + '【' + str(each_plugin) + '】'
        await session.send(reply_mes)
    else:
        if mes[1] not in config.keys():
            await session.send(mes[1]+'模块不存在，输入"模块 查看"查看所有模块')
            return
        elif mes[1] == 'super':
            await session.send('管理员权限不可修改！')
            return
        # 查询单个模块状态
        if mes[0] in ['状态']:
            await session.send(mes[1]+'模块开启：'+str(config[mes[1]]))
            return
        # 修改模块状态
        elif mes[0] in ['开启','开','on']:
            flag = True
        elif mes[0] in ['关闭','关','off']:
            flag = False
        else:
            await session.send('未知操作：'+mes[0])
            return
        config[mes[1]] = flag
        np.save('config.npy', config)
        await session.send(mes[1]+'模块开启：'+str(config[mes[1]]))
            
        
