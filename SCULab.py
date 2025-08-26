import requests


#配置开始

courseId='1ca7e86f42a244ec9bc1690f7920cd20' #课程id
courseSemaster=1 #学年
cookie="Your Cookie" #⚠️复制自己的cookie并粘贴,应当形如fanyamoocs=xxx; Hm_lvt_bxxx; HMACCOUNT=xxx; S1_rman_sid=xxx; Hm_lpvt_xxx=xxx; fs_session_id=xxx
interval=5000 # 默认5000，可根据需求增加至报错为止
maxTime=12000000000 #在无法获取视频时长的情况下每个视频最大学习时长

#配置结束


headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'cookie': cookie
}

def getUserInfo():
    #https://ecourse.scu.edu.cn/unifiedplatform/v1/user/current
    url="https://ecourse.scu.edu.cn/unifiedplatform/v1/user/current"
    resp=requests.request("GET",url=url,headers=headers)
    return int(resp.json()['extendMessage']['userCode'])



def fetchLessonList(courseId:str,semester:int):
    #https://ecourse.scu.edu.cn/learn/v1/homepage/chapter/info?courseId=1ca7e86f42a244ec9bc1690f7920cd20&type=&semester=1
    url='https://ecourse.scu.edu.cn/learn/v1/homepage/chapter/info'
    params={
        "courseId":courseId,
        "type":'',
        "semester":semester
    }
    resp=requests.get(url=url,params=params,headers=headers)
    #print(resp.json())
    lessonList=resp.json()['data']
    return lessonList

    

    

def fetchVidInfo(chapter_describe_List:list):
    #https://ecourse.scu.edu.cn/learn/v1/course/file/info

    url='https://ecourse.scu.edu.cn/learn/v1/course/file/info'
    jdata=chapter_describe_List
    resp=requests.request("POST",url=url,headers=headers,json=jdata)
    VidInfoList=resp.json()['data']
    #print(resp.json())
    videoDurationList=[]
    #print(VidInfoList)
    for i in VidInfoList:
        try:
            videoDurationList.append(int(i["videoDuration"]))
        except:
            videoDurationList.append(-1)
    print(videoDurationList)
    return videoDurationList
    

def addTime(courseId:str,guid_:str,courseType:int,courseSemester:int):
    # 增加学习时长（允许视频时长±10000毫秒浮动）
    
    jdata={"courseId":courseId,"timeInterval":interval,"courseType":courseType,"resourceId":guid_,"courseSemester":courseSemester}
    
    resp = requests.request("POST", "https://ecourse.scu.edu.cn/learn/v1/statistics/course/learntime", headers=headers, json=jdata)
    print("Now Stydying:",guid_,resp.json())
    return int(resp.json()["data"]["learnTime"])


def changeLessonStatus(guid_,courseType:int,courseSemester:int,userCode:int):
    # {"courseId":"1ca7e86f42a244ec9bc1690f7920cd20","courseType":1,"subsectionId":"4c48729e182442eba847a3a20ec96ae0","status":2,"resourceType":"video","courseSemester":1,"userCode":"2025141240176","studyTotalTime":1200000000}
    # https://ecourse.scu.edu.cn/learn/v1/learningsituation/resource/study/status

    url="https://ecourse.scu.edu.cn/learn/v1/learningsituation/resource/study/status"
    jdata={"courseId":"1ca7e86f42a244ec9bc1690f7920cd20","courseType":courseType,"subsectionId":guid_,"status":2,"resourceType":"video","courseSemester":courseSemaster,"userCode":userCode,"studyTotalTime":1200000000}
    resp = requests.request("POST",url,headers=headers,json=jdata)
    print("Changing Lesson Status:",guid_,resp.json())
    return resp.json()

if __name__ == '__main__':

    userCode=getUserInfo()
    lessonList=fetchLessonList(courseId,1)

    VidInfo=[]
    guid_List=[]
    chapter_describe_List=[]
    VidNum=0

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

    #print(chapter_describe_List) 
    #print(guid_List)

    videoDurationList=fetchVidInfo(chapter_describe_List)
    print(videoDurationList)





    counter=999
    flag=[]
    flagsize=0
    #maxTime=max(videoDurationList)
    for i in range(VidNum):
        flag.append("True")

    while counter!=0 :
        counter=0
        ptr=0
        for guid_ in guid_List:
            if flag[ptr]:
                learntime=addTime(courseId,guid_,1,courseSemaster)
                print("Studied:",learntime*10000,"/",videoDurationList[ptr])
                counter+=1
                if videoDurationList[ptr]==-1:
                    if learntime*10000 > maxTime:
                        flag[ptr]=False
                        changeLessonStatus(guid_,1,courseSemaster,userCode)

                else:
                    if learntime*10000 > videoDurationList[ptr] :
                            flag[ptr]=False
                            changeLessonStatus(guid_,1,courseSemaster,userCode)
                
                
            ptr+=1

    





        

            


                
