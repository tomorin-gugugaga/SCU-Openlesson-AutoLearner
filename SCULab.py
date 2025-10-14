import requests
import asyncio
import requests_async as arequests
import json

#配置开始

courseId='1b0acc38feb34fd299dcd283adeaf4d8' #课程id 目前经过测试的课程id: 新生线上第一课:66a33dc0330a4d079309c1996032ad30  实验室安全课:1ca7e86f42a244ec9bc1690f7920cd20
courseSemester=1 #学年
courseType=1 #课程类型，默认为1
cookie="Paste Your Cookie Here!"
#⚠️复制自己的cookie并粘贴,应当形如fanyamoocs=xxx; Hm_lvt_bxxx; HMACCOUNT=xxx; S1_rman_sid=xxx; Hm_lpvt_xxx=xxx; fs_session_id=xxx
interval=6000 # 默认每次请求向学习时长中添加6000ms，可根据需求增加至出现 {'status': 400, 'message': '学习时长异常不记入统计'} 为止
sleepBetweenRequests=0 #默认每个请求之间休眠0s，防止被封控，若出现 {'status': 200, 'message': 'OK', 'data': '调用太过频繁:1000'} 请适量调高
maxConcurrent=3 #最大并发数，同时处理的视频数量，建议设置为1-5，避免请求过快
maxTime=12000000000 #在无法获取视频时长的情况下每个视频最大学习时长

#配置结束


headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'cookie': cookie
}

def getUserInfo():
    #https://ecourse.scu.edu.cn/unifiedplatform/v1/user/current
    
    try:
        url="https://ecourse.scu.edu.cn/unifiedplatform/v1/user/current"
        resp=requests.request("GET",url=url,headers=headers)
        #print(resp.json())
        return int(resp.json()['extendMessage']['userCode'])
    except Exception as e:
        print("登录状态可能已过期，请尝试重新登录并再次获取cookies")
        print(e)
        return -1

async def joinClass(courseId,courseType,courseSemester):
    payload={"courseId":courseId,"courseType":courseType,"courseSemester":courseSemester}
    try:
        response0 = await arequests.request("POST", "https://ecourse.scu.edu.cn/learn/v1/learningsituation/join", headers=headers, json=payload)
        response_json=response0.json()
        if response_json["message"]=="OK":
            print("加入课程成功")
            print(response_json)
            return True
        
        else:
            print("加入课程失败，错误信息，请尝试手动加入课程，程序将退出：")
            print(response_json)
            return False
    except:
        print("无法加入课程，请求出错，程序将退出")
        raise SystemError

async def fetchLessonList(courseId:str,semester:int):
    
    #https://ecourse.scu.edu.cn/learn/v1/homepage/chapter/info?courseId=1ca7e86f42a244ec9bc1690f7920cd20&type=&semester=1
    url='https://ecourse.scu.edu.cn/learn/v1/homepage/chapter/info'
    params={
        "courseId":courseId,
        "type":'',
        "semester":semester
    }
    try:
        resp=await arequests.get(url=url,params=params,headers=headers)
    except:
        print("无法获取课程列表-请求出错，程序将退出")
        raise SystemError

    #print(resp.json())
    lessonList=resp.json()['data']
    print(resp.json())
    return lessonList

def fetchVidInfo(chapter_describe_List:list):
    
    #https://ecourse.scu.edu.cn/learn/v1/course/file/info

    url='https://ecourse.scu.edu.cn/learn/v1/course/file/info'
    jdata=chapter_describe_List
    try:
        resp=requests.request("POST",url=url,headers=headers,json=jdata)
    except:
        print("无法获取视频时长-请求出错，程序将退出")
        raise SystemError
    VidInfoList=resp.json()['data']
    #print(resp.json())
    videoDurationList=[]
    #print(VidInfoList)
    for i in VidInfoList:
        try:
            videoDurationList.append(int(i["videoDuration"]))
        except KeyboardInterrupt:
            print("用户中断，程序退出")
            raise SystemExit
        except:
            videoDurationList.append(-1)
    print(videoDurationList)
    return videoDurationList
    
    

    

async def addTime(courseId:str,guid_:str,courseType:int,courseSemester:int,videoDuration:int,semaphore:asyncio.Semaphore):
    # 增加学习时长（审核标准：允许视频时长±10000毫秒浮动）
    
    jdata={"courseId":courseId,"timeInterval":interval,"courseType":courseType,"resourceId":guid_,"courseSemester":courseSemester}
    
    print("Now Stydying:",guid_)
    try:
        async with semaphore:  # 使用信号量限制并发
            await asyncio.sleep(sleepBetweenRequests) 
            resp = await arequests.request("POST", "https://ecourse.scu.edu.cn/learn/v1/statistics/course/learntime", headers=headers, json=jdata)
            print(resp.json())
            
            if "获取分布式锁失败" in resp.json()['data']:
                print("速率过快。请适当调低最大并发数")
                return -1
            learntime=int(resp.json()["data"]["learnTime"])
            #输出学习进度
            print(f"Course {courseId} studied: {learntime*10000} of {videoDuration} | {learntime*10000/(videoDuration if videoDuration!=-1 else maxTime)*100:.2f} % ")
            return learntime
    except KeyboardInterrupt:
        print("用户中断，程序退出")
        raise SystemExit
    except:
        print("请求失败:请求出错")
        return -1



    
        

async def changeLessonStatus(guid_,courseType:int,courseSemester:int,userCode:int):
    # {"courseId":"1ca7e86f42a244ec9bc1690f7920cd20","courseType":1,"subsectionId":"4c48729e182442eba847a3a20ec96ae0","status":2,"resourceType":"video","courseSemester":1,"userCode":"2025141240176","studyTotalTime":1200000000}
    # https://ecourse.scu.edu.cn/learn/v1/learningsituation/resource/study/status

    url="https://ecourse.scu.edu.cn/learn/v1/learningsituation/resource/study/status"
    jdata={"courseId":"1ca7e86f42a244ec9bc1690f7920cd20","courseType":courseType,"subsectionId":guid_,"status":2,"resourceType":"video","courseSemester":courseSemester,"userCode":userCode,"studyTotalTime":1200000000}
    try: 
        resp = await arequests.request("POST",url,headers=headers,json=jdata)
        #{'status': 400, 'message': 'subsectionId: 399cd1b75cd8482c9ac79c7f481802b5 未匹配到对应的资源'}
        print("Changing Lesson Status:",guid_,resp.json())
        if resp.json()['status']!=200:
            print("可能该课程无需进行状态更改，如课程界面状态未成功变更，请手动进入课程页面观看1分钟视频以刷新状态")
        return resp.json()
    except:
        print("更改课程状态失败:请求出错")
        return -1

async def doLearningProcess(guid_,courseId,courseType,courseSemester,videoDuration,userCode,semaphore:asyncio.Semaphore):
    learntime=0
    while learntime*10000 < (maxTime if videoDuration==-1 else videoDuration):
        learntime=await addTime(courseId,guid_,courseType,courseSemester,videoDuration,semaphore) #有序
    await changeLessonStatus(guid_,courseType,courseSemester,userCode)


async def main():
#=== Main Program ===#

#=== Fetch User Info ===#
    userCode=getUserInfo()
    if userCode==-1:
        raise SystemExit
    
#=== Join Class & Fetch Lesson List ===#
    fetchResponse= await asyncio.gather(
        joinClass(courseId,1,courseSemester),
        fetchLessonList(courseId,courseSemester)
    )
    lessonList=fetchResponse[1]
    #print(lessonList)
    if fetchResponse[0]==False:
        raise SystemExit

    VidInfo=[]
    guid_List=[]
    chapter_describe_List=[]
    VidNum=0
    Dir_Type=2 #1 or 2

#=== Parse Lesson List ===#
    try: 
        print("Trying For TYPE2 Directories (default)")
        for i in lessonList:
            cd=i["childInfo"]
            for j in cd:
                cd2=j["childInfo"]
                for k in cd2:
                    #print(k["info"])
                    VidInfo.append(k["info"])
                    chapter_describe_List.append(k["info"]["chapter_describe"])
                    guid_List.append(k["info"]["guid_"])
                    VidNum+=1
        if VidNum==0:
            VidInfo=[]
            guid_List=[]
            chapter_describe_List=[]
            VidNum=0
            raise RuntimeError
    except RuntimeError:
        Dir_Type=1
        print("Going For TYPE1 Directories")
        for i in lessonList:
            cd=i["childInfo"]
            for j in cd:
                cd2=j["info"]
                VidInfo.append(cd2)
                chapter_describe_List.append(cd2["chapter_describe"])
                guid_List.append(cd2["guid_"])
                VidNum+=1
    except KeyboardInterrupt:
        print("用户中断，程序退出")
        raise SystemExit
    except:
        print("Unable to parse lesson list, the program will exit")
        raise SystemExit

#=== Fetch Video Duration ===#
    videoDurationList=fetchVidInfo(chapter_describe_List)

#=== Main Learning Loop ===#  
    # 创建信号量限制并发数
    semaphore = asyncio.Semaphore(maxConcurrent)
    
    LearningTasks=[]     
    ptr=0 
    for guid_ in guid_List:
        LearningTasks.append(asyncio.create_task(doLearningProcess(guid_,courseId,courseType,courseSemester,videoDurationList[ptr],userCode,semaphore)))
        ptr+=1
    
    await asyncio.gather(*LearningTasks)



if __name__ == '__main__':
    asyncio.run(main())
