# 使用flask构建的RESTful接口

## 特性列表

- 使用文件系统储存SESSION
- 使用SQLite作为关系型数据库
- 分模块组织源代码

## 待办

- route
    - blueprint
    - app.url_map.iter_rules()
- session
    - redis
- 日志
    - 自带
- 自定义异常与HTTP状态码映射
    - flask 提供的修饰器
- ORM and migrations
    - SQLAlchemy
    - mongoengine
- Validating
    - @todo
- 文件上传
- Authentication
    - JWT
    - Cryptography
    - HTTP 头传递token
- Authorization
    - RBAC
- 内容协商
    - 按输入格式解析并响应 flask-restful
- 分页
    - HTTP 头分页
- RESTFUL
    - 输入字段重写 HTTP verbs
        - WSGI Middleware
    - Rate Limiting
    - Versioning
- l18n
- cli

## 部署步骤