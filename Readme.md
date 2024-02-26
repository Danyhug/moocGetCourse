# API 文档：获取课程信息
## 路由：POST /getCourseInfo
### 安装
pip insatll -r .\requirements.txt
python server.py
### 请求体
user: 用户信息，包含用户名和密码，以 JSON 格式传输。
### 示例请求体
```json
{  
  "username": "example_user",  
  "password": "example_password"  
}
```
### 响应体
- mooc: MOOC 平台上的课程列表。
- zjy: zjy 上的课程列表。
- msg: 消息提示，通常为"获取成功"，如果发生错误则包含错误信息。
- ### 示例响应体
```json
{
  "mooc": [
    {
      "name": "模具数字化设计制造综合实训",
      "class": "",
      "time": "2024-02-27",
      "id": "1d2e3e5fe8c34b7286976d3d8d133c06",
      "teacher": "王正才"
    },
    {
      "name": "样品前处理技术",
      "class": "",
      "time": "2024-02-20",
      "id": "57c420562586410fb1c9c82caf65c5b3",
      "teacher": "夏德强"
    }
  ],
  "zjy": [
    {
      "name": "微机讲解",
      "class": "微机1班",
      "time": "2022-12-30 17:18:52",
      "id": "ada4505aee6d4af5bde073e703f269ba",
      "teacher": "唐海洋"
    }
  ],
  "msg": "获取成功"
}
```