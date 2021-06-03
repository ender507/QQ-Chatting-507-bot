from plugins.words import *
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.permission import *
import random

# wordRecord['qqnum'] = [word, ans, mode]
wordRecord = dict({})
# escapeList['qqnum'] = [word1, word2...]
escapeList = dict({})

with open('plugins\\esWord.txt','r') as f:
    for eachLine in f:
        s = eachLine.split()
        if s[0] not in escapeList.keys():
            escapeList[s[0]] = []
        escapeList[s[0]].append(s[1][:-1])


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
    

@on_command('单词')
async def words(session: CommandSession):
    mes = "【单词1】进入背单词模式一，给出英文猜中文。给出英文后输入中文意思或'答案'继续下一个单词\r\n\
【单词2】进入背单词模式二，给出中文猜英文。输入正确单词或'答案'后继续下一个单词\r\n\
【单词3】进入背单词模式三，同二，但英文单词会随机给出一半(向上取整)的字母\r\n\
【单词】查看功能说明\r\n\
【删除 hello】让某个单词不再出现（此功能针对每个账号有独立记录且不需要审核）\r\n\
【退出】退出背单词模式，不退出bot会一直烦你\
"
    await session.send(mes)

@on_command('退出')
async def words(session: CommandSession):
    global wordRecord, escapeList
    qqnum=str(session.ctx['user_id'])
    if qqnum in wordRecord:
        del wordRecord[qqnum]
        await session.send(qqnum+'已退出背单词模式')
    else:
        await session.send(qqnum+'不在背单词模式中')

@on_command('单词1')
async def words1(session: CommandSession):
    global wordRecord, escapeList
    qqnum=str(session.ctx['user_id'])
    await session.send('进入背单词【模式一】：给出英文猜中文')
    word = None
    if qqnum not in escapeList.keys():
        escapeList[qqnum] = []
    while word in escapeList[qqnum] or word is None:
        pos = random.randint(0,len(wordList)-1)
        word = wordList[pos]
    wordRecord[qqnum] = [word, ansList[pos], 1]
    await session.send(word)

@on_command('单词2')
async def words2(session: CommandSession):
    global wordRecord, escapeList
    qqnum=str(session.ctx['user_id'])
    await session.send('进入背单词【模式二】：给出中文猜英文')
    word = None
    if qqnum not in escapeList.keys():
        escapeList[qqnum] = []
    while word in escapeList[qqnum] or word is None:
        pos = random.randint(0,len(wordList)-1)
        word = wordList[pos]
    wordRecord[qqnum] = [word, ansList[pos], 2]
    await session.send(ansList[pos])

@on_command('单词3')
async def words3(session: CommandSession):
    global wordRecord, escapeList
    qqnum=str(session.ctx['user_id'])
    await session.send('进入背单词【模式三】：给出中文猜英文，给出英文片段')
    word = None
    if qqnum not in escapeList.keys():
        escapeList[qqnum] = []
    while word in escapeList[qqnum] or word is None:
        pos = random.randint(0,len(wordList)-1)
        word = wordList[pos]
    wordRecord[qqnum] = [word, ansList[pos], 3]
    await session.send(ansList[pos]+'\r\n提示：'+halfChange(word))


@on_command('答案')
async def ans(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    if qqnum not in wordRecord.keys():
        await session.send('你不在背单词模式中哦')
        return
    word = wordRecord[qqnum][0]
    ans = wordRecord[qqnum][1]
    await session.send('【'+word+'】'+ans)
    word = None
    while word in escapeList[qqnum] or word == None:
        pos = random.randint(0,len(wordList)-1)
        word = wordList[pos]
    if wordRecord[qqnum][2] == 1:
        wordRecord[qqnum] = [word, ansList[pos], 1]
        await session.send('下一个单词：【'+word+'】')
    elif wordRecord[qqnum][2] == 2:
        wordRecord[qqnum] = [word, ansList[pos], 2]
        await session.send('下一个单词：【'+ansList[pos]+'】')
    elif wordRecord[qqnum][2] == 3:
        wordRecord[qqnum] = [word, ansList[pos], 3]
        await session.send('下一个单词：【'+ansList[pos]+'】，提示：【'+halfChange(word)+'】')

@on_command('删除单词')
async def delete(session: CommandSession):
    qqnum=str(session.ctx['user_id'])
    mes = str(session.state.get('message') or session.current_arg).split()
    word = mes[0]
    with open('plugins\\esWord.txt','a') as f:
        f.write(qqnum+' '+word+'\n')
    global escapeList
    if qqnum not in escapeList.keys():
        escapeList[qqnum] = []
    escapeList[qqnum].append(word)
    await session.send(word+'已被添加至'+qqnum+'的删除列表中')

@on_command('replyAns')
async def replyans(session: CommandSession):
    message = session.state.get('message')
    qqnum=str(session.ctx['user_id'])
    flag = False
    word = wordRecord[qqnum][0]
    ans = wordRecord[qqnum][1]
    if wordRecord[qqnum][2] == 1 and message in ans:
        flag = True
    elif message == word:
        flag = True
    if flag:
        await session.send('回答正确：【'+word+'】'+ans)
        word = None
        while word in escapeList[qqnum] or word == None:
            pos = random.randint(0,len(wordList)-1)
            word = wordList[pos]
        if wordRecord[qqnum][2] == 1:
            wordRecord[qqnum] = [word, ansList[pos], 1]
            await session.send('下一个单词：【'+word+'】')
        elif wordRecord[qqnum][2] == 2:
            wordRecord[qqnum] = [word, ansList[pos], 2]
            await session.send('下一个单词：【'+ansList[pos]+'】')
        elif wordRecord[qqnum][2] == 3:
            wordRecord[qqnum] = [word, ansList[pos], 3]
            await session.send('下一个单词：【'+ansList[pos]+'】，提示：【'+halfChange(word)+'】')
    else:
        await session.send('回答错误')
    

@on_natural_language
async def _(session: NLPSession):
    stripped_msg = str(session.msg_text.strip())
    qqnum=str(session.ctx['user_id'])
    if qqnum not in wordRecord.keys():
        return None
    return IntentCommand(100.0, 'replyAns', args={'message': session.msg_text}) 
