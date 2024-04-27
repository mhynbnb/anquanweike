'''
File : get_all_course.py
Auther : MHY
Created : 2024/4/24 11:20
Last Updated : 
Description : 
Version : 
'''
import requests
import time
categoryCode_list=[101001001,101001002,101003002,101004002,101004003,
                   101004006,101004007,101004008,101006001,101007001]
userId='b252b05d-974d-40ce-b6a4-1a791b132a9b'
userProjectId='8bcb1671-216e-4cb8-ac6c-7a0cac4d9abe'
cookie='Hm_lvt_05399ccffcee10764eab39735c54698f=1713926205,1713945684,1714226821; Hm_lpvt_05399ccffcee10764eab39735c54698f=1714226821; SERVERID=3e9e86f31a75ec1ee6c732efcaf93765|1714226902|1714226820'
userName='8404df0f654f4f6f9c239658fe66c73f'
xToken='215b01a3-92f7-4ddc-9883-3191a15c4a68'


for categoryCode in categoryCode_list:
    header={
    'Cookie':cookie
    ,'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
    ,'X-Token':xToken
    }
    data={
        'tenantCode': 43000010,#constant,different for each user
        'userId': userId,#constant,different for each user
        'userProjectId': userProjectId,#constant,different for each user
        'chooseType': 3,#constant,different for each user
        'categoryCode': categoryCode#different for each category
    }
    time_stamp=str(int(time.time()*1000)/1000)
    url=f'https://weiban.mycourse.cn/pharos/usercourse/listCourse.do?timestamp={time_stamp}'
    rsp1=requests.post(url,headers=header,data=data)#获取课程列表
    course_info_list=rsp1.json()['data']
    print(course_info_list)
    print(f'共有{len(course_info_list)}个课程')
    count=0
    for course_info in course_info_list:
        count+=1
        if count!=1:
            continue
        print(f'进度: {count}/{len(course_info_list)}')
        #提取userCourseId和resourceId
        userCourseId=course_info['userCourseId']
        resourceId=course_info['resourceId']
        resourceName=course_info['resourceName']
        print('resourceName:',resourceName)
        print('userCourseId:',userCourseId, 'resourceId:',resourceId)
        # 发送study请求，获取信息：无
        time_stamp2 = str(int(time.time() * 1000) / 1000)
        url2=f'https://weiban.mycourse.cn/pharos/usercourse/study.do?timestamp={time_stamp2}'
        data2={
            'tenantCode': 43000010,
            'userId': userId,
            'courseId': resourceId,
            'userProjectId': userProjectId
        }
        rsp2=requests.post(url2,headers=header,data=data2)
        print('study:',rsp2)
        #发送getCourseUrl请求，获取信息：url4，method_token
        time_stamp3 = str(int(time.time() * 1000) / 1000)
        url3=f'https://weiban.mycourse.cn/pharos/usercourse/getCourseUrl.do?timestamp={time_stamp3}'
        rsp3=requests.post(url3,headers=header,data=data2)
        print(rsp3.json())
        url4=rsp3.json()['data']

        #发送xxx请求，获取信息：无，作用：未知
        data3={
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
        rsp4=requests.post(url4,headers=header,data=data3)

        method_token=url4.split('&')[3].split('=')[1]
        print('method_token:',method_token)

        #finnal
        url5 = f'https://weiban.mycourse.cn/pharos/usercourse/v1/{method_token}.do?'
        time_stamp5 = int(time.time())
        data5 = {
            'callback': f'jQuery34107900224573703418_{time_stamp5}',
            'userCourseId': userCourseId,
            'tenantCode': 43000010,
            '_': f'{time_stamp5}'
        }
        header5 = {
            'Cookie': cookie
            , 'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
        }

        rsp5 = requests.post(url5, data=data5, headers=header5)
        print(rsp5)
        print(f'{resourceName} 大概率搞定了！')
        if count!=len(course_info_list):
            print('15秒后进行下一个')
            time.sleep(15)
        else:
            print('全部搞定！')
            time.sleep(15)