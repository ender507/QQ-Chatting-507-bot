from .words import *
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, Event

import random
import time
import numpy as np

# wordRecord['qqnum'] = [word, ans, mode, source, timestamp]
wordRecord = dict({})
# escapeList['qqnum'] = [word1, word2...]
escapeList = np.load('plugins\\word\\esWord.npy',allow_pickle=True).item()

def delTimeOutRecord():
    global wordRecord
    t = time.time()
    for each_key in wordRecord.keys():
        if t - wordRecord[each_key][4] >= 120:  # 超时时间2min
            del wordRecord[each_key]
            


def halfChange(word):
    length = len(word)
    x = [1 for i in range(length)]
    for i in range(length//2):
        x[i] = 0
    random.shuffle(x)
    new_word = ""
    for i in range(length):
        if x[i] == 0:
            new_word += ' _ '
        else:
            new_word += word[i]
    return new_word
    

word_menu = on_command('单词')
@word_menu.handle()
async def _(bot: Bot, event: Event, state: T_State):
    mes = "【单词1】进入背单词模式一，给出英文猜中文。给出英文后输入中文意思或'答案'继续下一个单词\r\n\
【单词2】进入背单词模式二，给出中文猜英文。输入正确单词或'答案'后继续下一个单词\r\n\
【单词3】进入背单词模式三，同二，但英文单词会随机给出一半(向上取整)的字母\r\n\
【单词】查看功能说明\r\n\
【删除 hello】让某个单词不再出现（此功能针对每个账号有独立记录且不需要审核）\r\n\
【退出】退出背单词模式，不退出bot会一直烦你\
"
    await word_menu.send(mes)

word_exit = on_command('退出')
@word_exit.handle()
async def _(bot: Bot, event: Event, state: T_State):
    global wordRecord, escapeList
    qqnum=str(event.get_user_id())
    if str(event.get_message_type()) == 'private':
        mes_src = 'private'
    else:
        mes_src = str(event.get_group_id())
    if mes_src!= wordRecord[qqnum][3]:
        return
    if qqnum in wordRecord:
        del wordRecord[qqnum]
        await word_exit.send(qqnum+'已退出背单词模式')
    else:
        await word_exit.send(qqnum+'不在背单词模式中')

word1 = on_command('单词1')
@word1.handle()
async def _(bot: Bot, event: Event, state: T_State):
    global wordRecord, escapeList
    qqnum=str(event.get_user_id())
    if str(event.get_message_type()) == 'private':
        mes_src = 'private'
    else:
        mes_src = str(event.get_group_id())
    await word1.send('进入背单词【模式一】：给出英文猜中文')
    word = None
    if qqnum not in escapeList.keys():
        escapeList[qqnum] = []
    while word in escapeList[qqnum] or word is None:
        pos = random.randint(0,len(wordList)-1)
        word = wordList[pos]
    wordRecord[qqnum] = [word, ansList[pos], 1, mes_src, time.time()]
    await word1.send(word)

word2 = on_command('单词2')
@word2.handle()
async def _(bot: Bot, event: Event, state: T_State):
    global wordRecord, escapeList
    qqnum=str(event.get_user_id())
    if str(event.get_message_type()) == 'private':
        mes_src = 'private'
    else:
        mes_src = str(event.get_group_id())
    await word2.send('进入背单词【模式二】：给出中文猜英文')
    word = None
    if qqnum not in escapeList.keys():
        escapeList[qqnum] = []
    while word in escapeList[qqnum] or word is None:
        pos = random.randint(0,len(wordList)-1)
        word = wordList[pos]
    wordRecord[qqnum] = [word, ansList[pos], 2, mes_src, time.time()]
    await word2.send(ansList[pos])

word3 = on_command('单词3')
@word3.handle()
async def _(bot: Bot, event: Event, state: T_State):
    global wordRecord, escapeList
    qqnum=str(event.get_user_id())
    if str(event.get_message_type()) == 'private':
        mes_src = 'private'
    else:
        mes_src = str(event.get_group_id())
    await word3.send('进入背单词【模式三】：给出中文猜英文，给出英文片段')
    word = None
    if qqnum not in escapeList.keys():
        escapeList[qqnum] = []
    while word in escapeList[qqnum] or word is None:
        pos = random.randint(0,len(wordList)-1)
        word = wordList[pos]
    wordRecord[qqnum] = [word, ansList[pos], 3, mes_src, time.time()]
    await word3.send(ansList[pos]+'\r\n提示：'+halfChange(word))


word_ans = on_command('答案',aliases=set(('不会')))
@word_ans.handle()
async def _(bot: Bot, event: Event, state: T_State):
    qqnum=str(event.get_user_id())
    if qqnum not in wordRecord.keys():
        await word_ans.send('你不在背单词模式中哦')
        return
    if str(event.get_message_type()) == 'private':
        mes_src = 'private'
    else:
        mes_src = str(event.get_group_id())
    if mes_src!= wordRecord[qqnum][3]:
        return
    word = wordRecord[qqnum][0]
    ans = wordRecord[qqnum][1]
    await word_ans.send('【'+word+'】'+ans)
    word = None
    while word in escapeList[qqnum] or word == None:
        pos = random.randint(0,len(wordList)-1)
        word = wordList[pos]
    if wordRecord[qqnum][2] == 1:
        wordRecord[qqnum] = [word, ansList[pos], 1, mes_src, time.time()]
        await word_ans.send('下一个单词：【'+word+'】')
    elif wordRecord[qqnum][2] == 2:
        wordRecord[qqnum] = [word, ansList[pos], 2, mes_src, time.time()]
        await word_ans.send('下一个单词：【'+ansList[pos]+'】')
    elif wordRecord[qqnum][2] == 3:
        wordRecord[qqnum] = [word, ansList[pos], 3, mes_src, time.time()]
        await word_ans.send('下一个单词：【'+ansList[pos]+'】，提示：【'+halfChange(word)+'】')

word_del = on_command('删除单词',aliases=set(('删除')))
word_del.handle()
async def _(bot: Bot, event: Event, state: T_State):
    qqnum=str(event.get_user_id())
    mes = str(event.get_message()).strip()
    word = mes[0]
    global escapeList
    if qqnum not in escapeList.keys():
        escapeList[qqnum] = []
    escapeList[qqnum].append(word)
    np.save('plugins\\word\\esWord.npy',escapeList)
    await word_del.send(word+'已被添加至'+qqnum+'的删除列表中')



async def replyAns(bot: Bot, event: Event, mes, qqnum, mes_src):
    if mes_src!= wordRecord[qqnum][3]:
        return
    flag = False
    word = wordRecord[qqnum][0]
    ans = wordRecord[qqnum][1]
    def checkAlphabet(s):
        alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        f = False
        if '.' in s:
            f = True
        for i in s:
            if i in alphabet:
                f = True
                break
        return f
    if wordRecord[qqnum][2] == 1 and (message in ans):
        if not checkAlphabet(message):
            flag = True
        else:
            flag = False
            await reply_ans.send("答案中不能出现字母或点('.')")
    elif wordRecord[qqnum][2] != 1 and message == word:
        flag = True
    if flag:
        await reply_ans.send('回答正确：【'+word+'】'+ans)
        word = None
        while word in escapeList[qqnum] or word == None:
            pos = random.randint(0,len(wordList)-1)
            word = wordList[pos]
        if wordRecord[qqnum][2] == 1:
            wordRecord[qqnum] = [word, ansList[pos], 1, mes_src, time.time()]
            await reply_ans.send('下一个单词：【'+word+'】')
        elif wordRecord[qqnum][2] == 2:
            wordRecord[qqnum] = [word, ansList[pos], 2, mes_src, time.time()]
            await reply_ans.send('下一个单词：【'+ansList[pos]+'】')
        elif wordRecord[qqnum][2] == 3:
            wordRecord[qqnum] = [word, ansList[pos], 3, mes_src, time.time()]
            await reply_ans.send('下一个单词：【'+ansList[pos]+'】，提示：【'+halfChange(word)+'】')
    else:
        await reply_ans.send('回答错误')
    

word_mode = on_command('')
word_mode.handle()
async def _(bot: Bot, event: Event, state: T_State):
    stripped_msg = str(event.get_message()).strip()
    qqnum=str(event.get_user_id())
    if str(event.get_message_type()) == 'private':
        mes_src = 'private'
    else:
        mes_src = str(event.get_group_id())
    delTimeOutRecord()
    if qqnum not in wordRecord.keys() or wordRecord[qqnum][3]!=mes_src:
        return
    await replyAns(bot, event, stripped_msg, qqnum, mes_src)
