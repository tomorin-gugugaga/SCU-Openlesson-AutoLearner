# SCU-Openlesson-AutoLearner
自动学习四川大学公开课（特指新生实验室安全课）

## 环境需求
Python3 安装Requests包 （可能需配置venv）


## 需要配置的内容：
<img width="517" height="195" alt="image" src="https://github.com/user-attachments/assets/aaa94de5-aabd-44eb-a0f2-ffc881238bf2" />


12000000000为1200秒
默认配置为新生实验室安全课，未尝试其他环境下的兼容性。


## 如何获取cookies：

- 第一步<br/>登录`大川学堂`
- 第二步<br/>访问https://ecourse.scu.edu.cn/unifiedplatform/v1/user/current
- 第三步<br/>按下`f12`(若不行尝试`fn+f12`或`右键-检查`)，并找到`网络`<img width="1429" height="734" alt="image" src="https://github.com/user-attachments/assets/bfd8f4af-e528-4b2e-a1d1-cc4e06f56ba1" />

- 第四步<br/>刷新页面，找到`current`并进入<img width="1415" height="723" alt="image" src="https://github.com/user-attachments/assets/897a495c-2f28-4eda-a9bd-a7e290eb1286" />
- 第五步<br/>复制`标头`-`Cookie`中全部内容<img width="1426" height="728" alt="image" src="https://github.com/user-attachments/assets/47c691e0-e07e-46cd-a056-8282ec1afd50" />
- 第六步<br/>粘贴到代码cookie变量的引号中<img width="837" height="255" alt="image" src="https://github.com/user-attachments/assets/3db9eada-257b-4ec5-8548-4cc257e7f1fa" />

## 备注
目前支持课程关键信息存储在`childinfo-childinfo-info`处的课程，如《实验室安全管理与操作规范》
```json

[
    {
        "info": {
            ...
        },
        "childInfo": [
            {
                "info": {
                    ...
                },
                "childInfo": [
                    {
                        "info": {
                            "identification": "31c700b4c4454119a5245bd51335f3bb",
                            "guid_": "c66022c7dc404503a30114f31778ba28",
                            "chapter_describe": "acb09c65c026414b8626ffe10a69cefc",
                            "parent_id": "f4085a38edc448a39f9cb5a7293bc1e1",
                            "chapter_name": "实验室安全管理与环境保护概述（一）",
                            "course_semester_id": 1,
                            "resource_attributes": "courseware",
                            "resourse_type": "video",
                            "publish_status": 1,
                            "order": "1.1.1",
                            "status": 2,
                            "labels": null,
                            "knowledgePoints": null
                        },
                        "childInfo": []
                    }
                ]
            },
            {
                "info": {
                    ...
                },
                "childInfo": [
                    {
                        "info": {
                            "identification": "b6ab41c42c4042f4acb295d2d4eeb46e",
                            "guid_": "967ed40d6a9947369dc2526ed432fade",
                            "chapter_describe": "94a57f3f9b854ffeba5a169455f638a4",
                            "parent_id": "03842b2e1ff34ad18079f1555773329c",
                            "chapter_name": "实验室安全管理与环境保护概述（二）",
                            "course_semester_id": 1,
                            "resource_attributes": "courseware",
                            "resourse_type": "video",
                            "publish_status": 1,
                            "order": "1.2.1",
                            "status": 1,
                            "labels": null,
                            "knowledgePoints": null
                        },
                        "childInfo": []
                    }
                ]
            },
    ...
    ...

```


对于课程关键信息存储在`childinfo-info`处的课程，如《高等数学高阶课程》,相关逻辑有所差别，最新版本已尝试适配，如「新生线上第一课」现已测试通过
```json

[
    {
        "info": {
            ...
        },
        "childInfo": [
            {
                "info": {
                    "chapter_name": "1.1 极限概念与性质",
                    "identification": "251027f9761d42ee8acef4a22c26ed37",
                    "guid_": "65c4b534e4d34aefba3b490cbba2716b",
                    "chapter_describe": "b7d9a9a5a4bf444ea9ea972c252ad901",
                    "parent_id": "f8e2365459e74c27afebd6f44c0cd055",
                    "course_semester_id": 2,
                    "resource_attributes": "courseware",
                    "resourse_type": "video",
                    "publish_status": 1,
                    "order": "1.1",
                    "status": 1,
                    "labels": null,
                    "knowledgePoints": null
                },
                "childInfo": []
            },
            {
                "info": {
                    "chapter_name": "1.2 极限存在性的判别",
                    "identification": "fed10f6b44544bc889d9b37fe8c93ab2",
                    "guid_": "9b03b4c25f3546a29aa348a41505d666",
                    "chapter_describe": "a0959c1d5c5840eabe4efe329d1cefcd",
                    "parent_id": "f8e2365459e74c27afebd6f44c0cd055",
                    "course_semester_id": 2,
                    "resource_attributes": "courseware",
                    "resourse_type": "video",
                    "publish_status": 1,
                    "order": "1.2",
                    "status": 0,
                    "labels": null,
                    "knowledgePoints": null
                },
                "childInfo": []
            },
    ...
    ...

```


