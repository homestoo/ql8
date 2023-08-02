# 慕思会员_v1.1 小程序
# 2023/7/8  修改代码逻辑，修复已知bug
# 抓包urlhttps://atom.musiyoujia.com/member/wechatlogin/selectuserinfo
# 取appId，openId值填入mstoken，参数用@分割 ，多账号回车分割
# export mstoekn=appId@openId
# cron 0 0 7 * * ?

# ======自定义变量======
# 填入自己的User-Agent！
UserAgent = ""




import random
import time
from dotenv import load_dotenv
import os
import requests

time_yc = random.randint(10, 300)
# 加载.env文件
load_dotenv()
# 获取DWcookie环境变量值
accounts = os.getenv('mstoken')
# 检查DWcookie是否存在
if accounts is None:
    print('你不填mstoken，咋运行？')
else:
    # 获取环境变量的值，并按==分割成多个账号的参数组合
    accounts = os.environ.get('mstoken').split('\n')

    # 遍历所有账号
    for idx, account in enumerate(accounts, start=1):
        # 按分号参分割当前账号的不同数
        values = account.split('@')
        appId, openId = values[0], values[1]  # 获取各个值
        account_count = len(accounts)
        print(f"====获取账号{idx}信息====")
        time.sleep(2)
        url = "https://atom.musiyoujia.com/member/wechatlogin/selectuserinfo"

        headers = {
            'api_token': '1677561193953820673',
    'api_client_code': '65',
    'api_version': '1.0.0',
    'api_timestamp': '1688796859294',
    'api_sign': '0B4EBFAD242010A08A1132D7B03F33B9',
    'content-type': 'application/json',
    'Accept-Encoding': 'gzip,compress,br,deflate',
    'User-Agent': UserAgent
        }
        data = {"appId": appId,
                #"appType": "WECHAT_MINI_PROGRAM",
                "openId": openId
                }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            # 请求成功
            result = response.json()
            if "data" in result and "resMemberInfo" in result["data"] and "mobile" in result["data"]["resMemberInfo"]:
                value_mobile = result["data"]["resMemberInfo"]["mobile"]  # 获取账号
                # 进行下一步操作
                print(f"账号[{value_mobile}]")
            else:
                print("未找到 mobile,退出")
                exit(1)
            time.sleep(2)
            if "data" in result and "resMemberInfo" in result["data"] and "memberId" in result["data"]["resMemberInfo"]:
                member_id = result["data"]["resMemberInfo"]["memberId"]  # 获取token

            else:
                print("未找到 memberId，退出")
                exit(1)
            value_point = result["data"]["memberInfo"]["pointInfo"]["point"]  # 获取积分
            print(f"剩余积分:{value_point}")
        else:
            # 请求失败
            print('post请求失败:', response.status_code)
            exit(1)

        print("====开始签到====")
        time.sleep(2)
        url = 'https://atom.musiyoujia.com/member/memberbehavior/add'

        data = {
            "appId": appId,
            "appType": "WECHAT_MINI_PROGRAM",
            "osType": "ios",
            "model": "iPhone XR<iPhone11,8>",
            "browser": "微信小程序",
            "platform": "1",
            "sourceType": "5",
            "sourceChannel": "会员小程序",
            "siteId": "",
            "visitorId": "",
            "deviceId": "",
            "spotId": "",
            "campaignId": "",
            "deviceType": "",
            "eventLabel": "",
            "eventValue": "",
            "eventAttr2": "2023.7.8",
            "eventAttr3": "",
            "eventAttr4": "",
            "eventAttr5": "",
            "eventAttr6": "",
            "googleCampaignName": "",
            "googleCampaignSource": "",
            "googleCampaignMedium": "",
            "googleCampaignContent": "",
            "memberType": "DeRUCCI",
            "customId": member_id,
            "locationUrl": "/pages/user/signIn",
            "url": "/pages/user/signIn",
            "pageTitle": "每日签到",
            "logType": "event",
            "behaviorIds": [1, 3],
            "eventCategory": "用户签到",
            "eventAction": "签到",
            "eventAttr1": 1,
            "openId": openId
        }

        response = requests.post(url, json=data, headers=headers)
        result=response.json()

        if response.status_code == 200:
            if result['msg']=='success':
                result_point = result["data"]["point"]  # 签到奖励
                if result_point == 0:
                    print("签到状态：[重复签到]")
                else:
                    print(f"签到成功---{result_point}积分")
            else:
                print(f"签到失败，原因未知{result}")
        else:
            # 请求失败
            print('请求失败:', response.status_code)

