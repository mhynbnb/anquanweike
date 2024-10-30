"""
File : get_all_course.py
Auther : MHY
Created : 2024/4/24 11:20
Last Updated :
Description :
Version :
"""

import requests
import time
import tqdm

categoryCode_list = [101004007, 101004008, 101004013, 101005001, 101005003, 101007001]
userId = ' '
userProjectId = ' '
cookie = (' ')
userName = ' '
xToken = ' '
tenantCode = 0000000


def sleep(seconds):
    for s in tqdm.tqdm(range(seconds)):
        time.sleep(1)


for categoryCode in categoryCode_list:
    header = {
        'Cookie': cookie, 'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 '
            'Safari/537.36 Edg/130.0.0.0', 'X-Token': xToken
    }
    data = {
        'tenantCode': tenantCode,  # constant,different for each user
        'userId': userId,  # constant,different for each user
        'userProjectId': userProjectId,  # constant,different for each user
        'chooseType': 3,  # constant,different for each user
        'categoryCode': categoryCode  # different for each category
    }
    time_stamp = str(int(time.time() * 1000) / 1000)
    url = f'https://weiban.mycourse.cn/pharos/usercourse/listCourse.do?timestamp={time_stamp}'
    rsp1 = requests.post(url, headers=header, data=data)  # 获取课程列表
    course_info_list = rsp1.json()['data']
    print(course_info_list)
    print(f'共有{len(course_info_list)}个课程')
    count = 0
    for course_info in course_info_list:
        count += 1
        print(f'进度: {count}/{len(course_info_list)}')
        # 提取userCourseId和resourceId
        userCourseId = course_info['userCourseId']
        # print(f'userCourseId={userCourseId}')
        resourceId = course_info['resourceId']
        resourceName = course_info['resourceName']
        # print('resourceName:', resourceName)
        # print('userCourseId:', userCourseId, 'resourceId:', resourceId)
        # 发送study请求，获取信息：无
        time_stamp2 = str(int(time.time() * 1000) / 1000)
        url2 = f'https://weiban.mycourse.cn/pharos/usercourse/study.do?timestamp={time_stamp2}'
        data2 = {
            'tenantCode': tenantCode,
            'userId': userId,
            'courseId': resourceId,
            'userProjectId': userProjectId
        }
        rsp2 = requests.post(url2, headers=header, data=data2)
        # print('study:', rsp2)
        # 发送getCourseUrl请求，获取信息：url4，method_token
        time_stamp3 = str(int(time.time() * 1000) / 1000)
        url3 = f'https://weiban.mycourse.cn/pharos/usercourse/getCourseUrl.do?timestamp={time_stamp3}'
        rsp3 = requests.post(url3, headers=header, data=data2)
        # print(rsp3.json())
        url4 = rsp3.json()['data']

        # 发送请求，获取答题用的相关资源
        data3 = {
            'userProjectId': userProjectId,
            'userId': userId,
            'courseId': resourceId,
            'projectType': 'special',
            'projectId': 'undefined',
            'protocol': 'true',
            'link': 20862,
            'weiban': 'weiban',
            'userName': userName
        }
        rsp4 = requests.post(url4, headers=header, data=data3)

        method_token = url4.split('&')[3].split('=')[1]
        # print('method_token:', method_token)
        sleep(15)
        # finnal
        url5 = (f'https://weiban.mycourse.cn/pharos/usercourse/getCaptcha.do?userCourseId={userCourseId}'
                f'&userProjectId={userProjectId}&userId={userId}&tenantCode={tenantCode}')
        data5 = {
        }
        header5 = {
            'Cookie': cookie, 'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 '
                'Safari/537.36 Edg/130.0.0.0'
        }

        rsp5 = requests.post(url5, data=data5, headers=header5)
        # print(f'rsp5={str(rsp5.json())}')
        questionId = rsp5.json()['captcha']["questionId"]

        # time.sleep(10)

        url6 = (f'https://weiban.mycourse.cn/pharos/usercourse/checkCaptcha.do?userCourseId={userCourseId}'
                f'&userProjectId={userProjectId}&userId={userId}&tenantCode={tenantCode}&questionId={questionId}')
        print(url6)
        data6 = {
            # 'coordinateXYs': [{"x": 64, "y": 416}, {"x": 141, "y": 416}, {"x": 218, "y": 410}]
            'coordinateXYs': '[{"x": 64, "y": 416}, {"x": 141, "y": 416}, {"x": 218, "y": 410}]'
        }
        header6 = {
            'Cookie': cookie, 'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 '
                'Safari/537.36 Edg/130.0.0.0'
        }

        rsp6 = requests.post(url6, data=data6, headers=header6)
        # print(f'rsp6={rsp6.json()['data']['showText']}')

        method_token = rsp6.json()['data']['methodToken']
        url7 = f'https://weiban.mycourse.cn/pharos/usercourse/v2/{method_token}.do?'
        time_stamp7 = int(time.time())
        data7 = {
            'callback': f'jQuery34107900224573703418_{time_stamp7}',
            'userCourseId': userCourseId,
            'tenantCode': tenantCode,
            '_': f'{time_stamp7}'
        }
        header7 = {
            'Cookie': cookie, 'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 '
                'Safari/537.36 Edg/124.0.0.0'
        }

        rsp7 = requests.post(url7, data=data7, headers=header7)
        print(rsp7.text)
        print(f'{resourceName} 大概率搞定了！')
        if count != len(course_info_list):
            print('下一个')
            sleep(1)
        else:
            print('全部搞定！')
            sleep(3)
