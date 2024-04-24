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


for categoryCode in categoryCode_list:
    header={
    'Cookie':'Hm_lvt_05399ccffcee10764eab39735c54698f=1713926205; Hm_lpvt_05399ccffcee10764eab39735c54698f=1713926205; SERVERID=3e9e86f31a75ec1ee6c732efcaf93765|1713927010|1713926205'
    ,'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
    ,'X-Token':'66ee1be4-661e-414d-a90b-7376d8dcc577'
    }
    data={
        'tenantCode': 43000010,#constant,different for each user
        'userId': 'f0e0eaf0-86e6-4a8d-aa07-d2aa34f5cca6',#constant,different for each user
        'userProjectId': 'd566d88d-db54-424f-8571-5fb8efd788e0',#constant,different for each user
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
            'userId': 'f0e0eaf0-86e6-4a8d-aa07-d2aa34f5cca6',
            'courseId': resourceId,
            'userProjectId': 'd566d88d-db54-424f-8571-5fb8efd788e0'
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
            'userProjectId': 'd566d88d-db54-424f-8571-5fb8efd788e0',
            'userId': 'f0e0eaf0-86e6-4a8d-aa07-d2aa34f5cca6',
            'courseId': resourceId,
            'projectType': 'special',
            'projectId': 'undefined',
            'protocol': 'true',
            'link': 20862,
            'weiban': 'weiban',
            'userName': '73d7946d5fbd4ddc9b608292bad68c44'
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
            'Cookie': 'Hm_lvt_05399ccffcee10764eab39735c54698f=1713926205; Hm_lpvt_05399ccffcee10764eab39735c54698f=1713926205; SERVERID=3e9e86f31a75ec1ee6c732efcaf93765|1713927010|1713926205'
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