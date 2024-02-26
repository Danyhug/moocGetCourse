import json

import uvicorn
from fastapi import FastAPI, Depends, Body

from mooc import Mooc

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/getCourseInfo")
async def get_course_info(user=Body(...)):
    data = user
    print(data)
    mooc = Mooc()

    # 课程列表
    course_list = {
        'mooc': [],
        'zjy': [],
        'msg': '获取成功'
    }
    try:
        if mooc.login(data['username'], data['password']):
            course_list['mooc'] = mooc.get_mooc_course()
            if mooc.check_zjy_auth():
                course_list['zjy'] = mooc.get_zjy_all_course()
        return course_list
    except RuntimeError as e:
        course_list['msg'] = str(e)
        return course_list


uvicorn.run(app, host="0.0.0.0", port=20000)
