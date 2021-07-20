from plugins.words import *
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
import random
import time
import numpy as np
from datetime import datetime


'''
memo_note = {(qqnum,week):memo}
'''
memo_note = dict({})
try:
    memo_note = np.load('plugins\\memo.npy',allow_pickle=True).item()
except:
    memo_note = dict({})
    np.save('plugins\\memo.npy',memo_note)
plugin_name ='memo'
    

num2week=[
[],
['1','周一','星期一','礼拜一'],
['2','周二','星期二','礼拜二'],
['3','周三','星期三','礼拜三'],
['4','周四','星期四','礼拜四'],
['5','周五','星期五','礼拜五'],
['6','周六','星期六','礼拜六'],
['7','周日','星期日','星期天','礼拜天','礼拜日']
    ]

@on_command('备忘')
async def memo(session: CommandSession):
    global wordRecord, escapeList
    qqnum = str(session.ctx['user_id'])
    config = np.load('config.npy',allow_pickle=True).item()
    if qqnum in config['black_list'] or config[plugin_name] == False:
        return
    content = str(session.state.get('message') or session.current_arg)  
    # 查询
    today = datetime.now().isoweekday()
    if content=="":
        mes = qqnum + "的" + num2week[today][1] + '备忘为：'
        tmp = mes[:]
        for each in memo_note.keys():
            if qqnum == each[0] and each[1] == today:
                for m in memo_note[each]:
                    mes += m
                    mes += '\r\n'
        if mes == tmp:
            mes += '空'
        await session.send(mes)
        return
    try:
        content = content.split(' ',2)
        # 查询全部
        if content[0] == 'ls':
            mes = qqnum + "的" + '备忘为：'
            tmp = mes[:]
            for each in memo_note.keys():
                if qqnum == each[0]:
                    for m in memo_note[each]:
                        mes = mes + '【' + num2week[each[1]][1] + '】'
                        mes += m
                        mes += '\r\n'
            if mes == tmp:
                mes += '空'
            await session.send(mes)
            return
        # 新增
        elif content[0] == '+':
            day = 0
            for i in range(len(num2week)):
                if content[1] in num2week[i]:
                    day = i
            if day==0:
                raise Exception
            if (qqnum, day) not in memo_note.keys():
                memo_note[(qqnum, day)] = []
            memo_note[(qqnum, day)].append(content[2])
            np.save('plugins\\memo.npy',memo_note)
            await session.send('添加成功')
        # 删除
        elif content[0] == '-':
            flag = True
            for each in memo_note.keys():
                print(each)
                if qqnum == each[0] and each[1] == int(content[1]):
                    for i in range(len(memo_note[each])):
                        if memo_note[each][i] == content[2]:
                            print(memo_note[each][i] , content[2])
                            del memo_note[each][i]
                            await session.send('删除成功')
                            flag = False
                            break
            if flag:
                await session.send('删除失败：要删除的消息不存在')
        elif content[0] == '菜单':
            mes = "【备忘】查看当天备忘消息\r\n\
【备忘 ls】查看当前qq的全部备忘消息\r\n\
【备忘 + 4 你好】在周四的备忘消息中加入'你好'\r\n\
【备忘 - 4 你好】在周四的备忘消息中删去'你好'\
"
            await session.send(mes)
        # 格式错误
        else:
            raise Exception('格式错误')
    except:
        mes = "消息格式错误！尝试：\
【备忘】查看当天备忘消息\r\n\
【备忘 ls】查看当前qq的全部备忘消息\r\n\
【备忘 + 4 你好】在周四的备忘消息中加入'你好'\r\n\
【备忘 - 4 你好】在周四的备忘消息中删去'你好'\
"
        await session.send(mes)
    else:
        pass

 
