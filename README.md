# QQ聊天机器人：507bot
基于nonebot和go-cqhttp的QQ聊天机器人，含有部分自己写的插件和别人开源的插件。
## 现有插件
|插件名称|插件功能|插件来源|特殊说明|
|:-:|:-:|:-:|:-:|
|arknight_gacha|模拟明日方舟十连抽卡（卡池更新至画中人）|自己写的|只支持所有角色均无up的情况|
|bilibili|推送b站主播的动态（含视频和直播）|https://github.com/wxz97121/QQBot_bilibili|见原作者|
|cmd|roll点、特定消息自动回复，含开关|自己写的|为了符合群友的xp设置的内容，图一乐。图片回复需要在本地保存了相应图片|
|couplet|对对联|https://github.com/233a344a455/DeltaBot|见原作者|
|lyric|爬取并发送网易云音乐的歌词|自己写的|使用了网易云接口（包括歌曲搜索接口、歌词获取接口）|
|star|查看不同星座的当日运势|自己写的|用了QQ已经过时的星座运势接口（2015年），虽然日期的年份不对但是也只是图一乐而已，不管了|
|super|管理员功能（含私货）|自己写的|除了强制关闭外基本没用，黑名单和模块管理功能分散在各个模块里|
|teach|让群友教bot在群友特定发言下进行特定回复|自己写的|写入本地文本文件而不是直接加入功能模块，防止bot被群友玩恶堕。有意思的回复自己手动加就行|
|translate|翻译，中译英或其他语种翻译成中文|自己写的|用了有道翻译的接口并爬取结果|
|weather|依据省份和城市查看实时天气|自己写的|使用中央气象台的接口（含省份代码接口、城市代码接口、天气查询接口）|
## TODO LIST
TODO：
- [ ] ~~能用QQ消息执行的重启功能~~(新版本插件启用禁用不需要重启就能生效，因此重启功能实装取消)
- [x] 能够统一管理、能用QQ消息执行的黑名单(v0.4更新实装)
- [x] 能用QQ消息执行的插件启用/禁用功能(v0.4更新实装)
- [x] 小游戏(v0.3版本更新实装，指对联)
- [x] 抽卡模拟器(v0.5版本更新实装，目前只支持明日方舟)
- [ ] 翻译功能可以指定语种

## 更新日志
### v0.3
v0.3版本下首次开源
### v0.4
- 新增模块管理功能：模块名+启用/禁用可以进行模块开关而不需要重启整个bot
- 新增黑名单功能：模块名+黑名单/出狱+QQ号可以对用户进行特定模块使用的禁用和解除
- 删除了原有模块管理的文件操作功能（原本的模块管理功能由py模块文件的删除和复制实现，需要重启bot才能应用更新）
- 新增了翻译的屏蔽词
- 天气指令优化：除了原来的天气+省份+城市之外，还支持天气+直辖市和天气+直辖市+具体地名的传参方式
### v0.5
- 新增arknight_gacha模块，模拟明日方舟十连抽卡（卡池更新至画中人）
- 唤醒507bot由命令形式`@on_command`改成自然语言形式`@on_natural_language`（现在只要提及507bot就能唤醒）
- 回复关键词"雾宝"和"雾妹"时加入过滤选项，防止和雾宝bot进行无限聊天
- 发送歌词设置了最大上限(被群友发的圆周率之歌搞了一手
- 天气模块微调：查询台湾省天气时有特殊提示（台湾天气用现在实装的api查询不出来，更新前会导致查询无回复）
- 修正天气回复文本错误：原本api返回值的`rain`被我误认为下雨概率，经核实后改为降雨等级
- 新增部分无关紧要的自动回复
## 其他说明
更新完全随缘，目标只为图一乐

![1.png](1.png)
