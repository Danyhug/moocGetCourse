"""
Created By 智慧职教助手
http://mooc.zzf4.top
"""

import hashlib
import json
from bs4 import BeautifulSoup

import requests


class Mooc:
    def __init__(self):
        global headers
        self.token = None
        self.loginId = None
        self.URL_GET_COURSE_POST: str = 'https://icve-mooc.icve.com.cn/patch/zhzj/studentMooc_selectMoocCourse.action'
        self.URL_GET_USERINFO_GET = 'https://icve-mooc.icve.com.cn/learning/u/student/student/mooc_index.action'
        self.passwd = None
        self.uname = None
        self.zyk_need_token = None
        self.URL_LOGIN_POST = 'https://sso.icve.com.cn/prod-api/data/userLoginV2'
        self.session = requests.session()
        self.session.headers.update(
            {'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; OPPO R11 Plus Build/NMF26X; wv) AppleWebKit/537.36'
                           ' (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36 whatyApp whatyApiApp',
             'Referer': 'https://icve-mooc.icve.com.cn/',
             'Content-Type': 'application/x-www-form-urlencoded',
             'Connection': 'close'})

    def md5(self, s):
        md5_hash = hashlib.md5()
        md5_hash.update(s.encode('utf-8'))
        hashed_bytes = md5_hash.digest()
        hashed_string = ''.join(format(byte, '02x') for byte in hashed_bytes)[8:24]
        return hashed_string

    def login(self, username: str, passwd: str) -> bool:
        data = {
            'userName': username,
            'type': 1,
            'password': passwd
        }
        res = self.session.post(self.URL_LOGIN_POST, json.dumps(data), headers={
            'Content-Type': 'application/json',
            'Referer': 'https://sso.icve.com.cn/sso/auth?mode=simple&source=2&redirect=https%3A%2F%2Fmooc.icve.com.cn'
        }).json()
        # 登录成功
        # print(res)
        if res['code'] == 500:
            raise RuntimeError(res['msg'])
        elif res['code'] == 200:
            # 保存账号信息
            print('登录成功')
            self.zyk_need_token = res['data']['token']
            self.uname = username
            self.passwd = passwd

            try:
                self.getUserinfo()
            except AttributeError:
                raise RuntimeError('登录失败，未知错误，请重新登录')

            # # 存储登录状态
            # glo.userInfoRes = f'智慧职教模块 > 用户名 {username} 登陆在 {datetime.datetime.now()}'

            return True
        return False

    # 获取用户信息
    def getUserinfo(self):
        # 获取到了html代码，分析要的参数
        html = self.session.get(self.URL_GET_USERINFO_GET).text
        soup = BeautifulSoup(html, 'html.parser')
        # 解析html代码获取token
        n = 0
        for t in soup.find('script').text.splitlines():
            if t:
                if t.find('loginIdToken') != -1:
                    self.token = t.split("'")[1]
                    n += 1
                elif t.find('_LOGINID_ ') != -1:
                    self.loginId = t.split("'")[1]
                    n += 1

                if n == 2:
                    print('获取用户信息成功')
                    # 证明找到了需要的参数
                    return True

        return False

    def get_mooc_course(self):
        print('正在获取所有智慧职教课程')
        data = {
            'token': self.token,
            'siteCode': 'zhzj',
            'curPage': 1,
            'pageSize': 99,
            'selectType': 1,
            'searchName': ''
        }
        # 这有loginId res['loginId]
        res = self.session.post(self.URL_GET_COURSE_POST, data=data).json()
        print('已获取所有智慧职教课程')
        # 返回数据
        d = []
        for r in res['data']:
            d.append({
                'name': r[0],
                'class': '',
                'time': r[3],
                'id': r[6],
                'teacher': r[15]
            })

        return d

    def get_zjy_all_course(self):
        data = {
            'data': 'info',
            'page.searchItem.queryId': 'getCourseById',
            'page.searchItem.keyname': '',
            'page.curPage': 1,
            'page.pageSize': 200
        }
        self.session.get('https://user.icve.com.cn/learning/u/userDefinedSql/getBySqlCode.json')
        res = self.session.post('https://user.icve.com.cn/learning/u/userDefinedSql/getBySqlCode.json', data).json()
        if res['errorCode'] != '0':
            print('获取失败', res)
            return []
        # 返回数据
        d = []
        # 所有课程
        if res['page']['items']:
            courses = res['page']['items'][0]['info']
            for c in courses:
                d.append({
                    'name': c['ext1'],
                    'class': c['ext2'],
                    'time': c['ext3'],
                    'id': c['ext9'],
                    'teacher': c['ext4']
                })
            return d

        # print(res['page']['searchItem'])
        return []

    # 检查是否有职教云权限
    def check_zjy_auth(self) -> bool:
        url = 'https://user.icve.com.cn/patch/zhzj/projectStatistics_getReviewStatus.action'
        res = self.session.post(url).json()
        print(res)
        if res['code'] == '00000':
            self.session.get(
                'https://user.icve.com.cn/learning/entity/student/commonStudent_ajax.action?serviceName=learnRecordCallBack&modle=callBack')
            return True
        return False


if __name__ == '__main__':
    uname = ''
    password = ''
    mooc = Mooc()
    # 课程列表
    course_list = {
        'mooc': [],
        'zjy': []
    }
    if mooc.login(uname, password):
        course_list['mooc'] = mooc.get_mooc_course()
        if mooc.check_zjy_auth():
            course_list['zjy'] = mooc.get_zjy_all_course()

    print(course_list)
