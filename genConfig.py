'''
初次使用bot时，运行该程序生成config.npy从而保证模块正常运行
'''
import numpy as np

config = dict()
# 黑名单
config['black_list'] = set()
# 全部模块
config['plugins'] = [
'super',
'lyric',
'NLP',
'baidu'
'couplet',
'emoji',
'record',
'speak',
'star',
'teach',
'translate',
'weather',
'word',
'replyer',
'roll'
]
# 模块状态
config['super'] = True
config['lyric'] = True
config['NLP'] = True
config['baidu'] = True
config['couplet'] = True
config['emoji'] = True
config['record'] = True
config['speak'] = True
config['star'] = True
config['teach'] = True
config['translate'] = True
config['weather'] = True
config['word'] = True
config['replyer'] = True
config['roll'] = True

np.save('config.npy', config)
