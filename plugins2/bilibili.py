import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
from datetime import datetime,date,timedelta
import random
import requests
import json,collections,xml
from lxml import etree
import time

VR_uid_list=[6471011,387636363,171206421]
VR_group_list=[[1057501621],[1057501621],[1057501621]]
VR_name_list=['雾宝','lulu','白神馨']

plugin_name = 'bilibili'

#  每隔一分钟进行一次状态检测
@nonebot.scheduler.scheduled_job('interval',minutes=1)
async def _():
    bot = nonebot.get_bot()
    for i in range(min(len(VR_uid_list),len(VR_group_list))):
        res=''
        # 获取动态信息
        dynamic_content = GetDynamicStatus(VR_uid_list[i], i)
        for content in dynamic_content:
            try:
                for groupnum in VR_group_list[i]:
                    res = await bot.send_group_msg(group_id=groupnum, message=content)
            except CQHttpError as e:
                pass

        # 获取直播信息
        room_id = get_live_room_id(VR_uid_list[i])
        live_status = GetLiveStatus(room_id)
        if live_status != '':
            for groupnum in VR_group_list[i]:
                await bot.send_group_msg(group_id=groupnum,
                                         message=VR_name_list[i] +' 开播啦！直播间标题：' + live_status)

# 获取直播间id
def get_live_room_id(mid):
    res = requests.get('https://api.bilibili.com/x/space/acc/info?mid='+str(mid)+'&jsonp=jsonp')
    res.encoding = 'utf-8'
    res = res.text
    data = json.loads(res)
    data = data['data']
    roomid = 0
    try:
        roomid = data['live_room']['roomid']
    except:
        print(mid,'error in get live room id')
        pass
    return roomid

# 获取b站动态状态
def GetDynamicStatus(uid, VRindex):
    #print('Debug uid  '+str(uid))
    res = requests.get('https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid='+str(uid)+'offset_dynamic_id=0')
    res.encoding='utf-8'
    res = res.text
    #res = res.encode('utf-8')
    cards_data = json.loads(res)
    try:
        cards_data = cards_data['data']['cards']
    except:
        print('exit:',uid)
        exit()
    print(uid,'Success get')
    try:
        with open(str(uid)+'Dynamic','r') as f:
            last_dynamic_str = f.read()
            f.close()
    except Exception as err:
        last_dynamic_str=''
        pass
    if last_dynamic_str == '':
        last_dynamic_str = cards_data[1]['desc']['dynamic_id_str']
    print(last_dynamic_str)
    index = 0
    content_list=[]
    cards_data[0]['card'] = json.loads(cards_data[0]['card'],encoding='gb2312')
    nowtime = time.time().__int__()
    # card是字符串，需要重新解析
    while last_dynamic_str != cards_data[index]['desc']['dynamic_id_str']:
        #print(cards_data[index]['desc'])
        try:
            if nowtime-cards_data[index]['desc']['timestamp'] > 125:
                break
            if (cards_data[index]['desc']['type'] == 64):
                content_list.append(VR_name_list[VRindex] +'发了新专栏「'+ cards_data[index]['card']['title'] + '」并说： ' +cards_data[index]['card']['dynamic'])
            else:
                if (cards_data[index]['desc']['type'] == 8):
                    content_list.append(VR_name_list[VRindex] + '发了新视频「'+ cards_data[index]['card']['title'] + '」并说： ' +cards_data[index]['card']['dynamic'])
                else:         
                    if ('description' in cards_data[index]['card']['item']):
                        #这个是带图新动态
                        content_list.append(VR_name_list[VRindex] + '发了新动态： ' +cards_data[index]['card']['item']['description'])
                        #print('Fuck')
                        #CQ使用参考：[CQ:image,file=http://i1.piimg.com/567571/fdd6e7b6d93f1ef0.jpg]
                        for pic_info in cards_data[index]['card']['item']['pictures']:
                            content_list.append('[CQ:image,file='+pic_info['img_src']+']')
                    else:
                        #这个表示转发，原动态的信息在 cards-item-origin里面。里面又是一个超级长的字符串……
                        #origin = json.loads(cards_data[index]['card']['item']['origin'],encoding='gb2312') 我也不知道这能不能解析，没试过
                        #origin_name = 'Fuck'
                        if 'origin_user' in cards_data[index]['card']:
                            origin_name = cards_data[index]['card']['origin_user']['info']['uname']
                            content_list.append(VR_name_list[VRindex]+ '转发了「'+ origin_name + '」的动态并说： ' +cards_data[index]['card']['item']['content'])
                        else:
                            #这个是不带图的自己发的动态
                            content_list.append(VR_name_list[VRindex]+ '发了新动态： ' +cards_data[index]['card']['item']['content'])
            content_list.append('本条动态地址为'+'https://t.bilibili.com/'+ cards_data[index]['desc']['dynamic_id_str'])
        except Exception as err:
                print('PROCESS ERROR')
                pass
        index += 1
        if len(cards_data) == index:
            break
        cards_data[index]['card'] = json.loads(cards_data[index]['card'])
    f = open(str(uid)+'Dynamic','w')
    f.write(cards_data[0]['desc']['dynamic_id_str'])
    f.close()
    return content_list


# 获取b站直播状态
def GetLiveStatus(uid):
    res = requests.get('https://api.live.bilibili.com/room/v1/Room/get_info?device=phone&;platform=ios&scale=3&build=10000&room_id=' + str(uid))
    #res = requests.get('https://api.live.bilibili.com/AppRoom/msg?room_id='+str(uid))
    #res = requests.get ('https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid=21463238')
    res.encoding = 'utf-8'
    res = res.text
    try:
        with open(str(uid)+'Live','r') as f:
            last_live_str = f.read()
            f.close()
    except Exception as err:
            last_live_str = '0'
            pass
    try:
        live_data = json.loads(res)
        live_data = live_data['data']
        now_live_status = str(live_data['live_status'])
        live_title = live_data['title']
    except:
        now_live_status = '0'
        pass
    f = open(str(uid)+'Live','w')
    f.write(now_live_status)
    f.close()
    if last_live_str != '1':
        if now_live_status == '1':
            return live_title
    return ''
