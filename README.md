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


