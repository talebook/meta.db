db.talebook.org

# Features:
* User: 无门槛注册，根据同步的书目数量升级，read vote edit admin
* Meta: bsdiff增量同步metadata.db到服务端，额外计算md5->bookid
* Key设计，以isbn+title为key，对多个version，每个version有格式 大小 md5（一本书多种版本），但是一个title有好几个版本？
* Merge Service: 挑选有价值的记录合并到主db，以star数决定可信度；
* Web界面可搜索，查看，star，精选，踩，修改，删除
* API接口提供sync，get_image, upload_meta, upload_img
* 数据量
    * 书：4k=40MB，1kw=10M=100GB
    * 图：一张35KB(480x640)，1kw=10M=3.5TB


## 用户注册和管理
1. 降低使用门槛：支持 social auth 或者 邮件注册
2. 根据同步到服务器中的metadata.db计算贡献度
3. 设置三挡角色：reader普通用户、editor编辑员、admin管理员、sre运维
4. 生成有效的apikey（强制用户分享上传，才能下载）


## metadata.db 增量同步
1. 使用 sqlite .backup 'new.db' 拷贝一份数据库
2. 使用 bsdiff 计算增量差异（首次直接传输完整文件）
3. 每个user各自一个独立目录，同步cover.jpg


## 界面
1. 首页：列举最近更新的书籍
2. 搜索：任意搜索（对标豆瓣？）
3. 详情：要求登录
4. 点star



# Talebook:
* 作为plugin集成
* 增加system设置
* 定时上传metadata.db
* 定时下载info.db到本地DB，离线批量查询？ 数据量可能太大了



# 库表设计

```
User = {
    id: 1,
    name: 'user',
    nick: 'good name',
    level: 'user/vip',
    auth: 'read/write/admin',
    apikey: ['key1', 'key2'],
    path: '/user/1/',
}

Book = {
    title: '朝花夕拾',
    isbn: 'xxxxxxx',
    meta: <Meta>,
    stars: 1,
    choices: 1,
    users: ['user1', 'user2'],
    files: [{format: 'epub', length: 1234, md5: 'xxxx'}],
}

Meta = {
    title: "确是我说的——鲁迅语选(一书\"掌握\"鲁迅名言!广搜博采鲁迅精华，辑录名言警句300余条!) (上海辞书出品)",
    authors: [ "佚名" ],
    comments: "暂无简介",
    isbn: "0000000000001",
    language: null,
    pubdate: "2024-04-04",
    publisher: "Unknown",
    rating: null,
    series: null,
    tags: [],
    timestamp: "2024-04-04",
}
```

