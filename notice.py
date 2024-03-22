# -*- coding: utf-8 -*-
import os
import requests
import json
import datetime
import pytz


[company_id, app_secret, agent_id] = os.environ.get("QY_WX_TOKEN").split("|")


def get_beijing_time(format_="%Y-%m-%d %H:%M:%S"):
    # 设置时区为北京时间
    tz = pytz.timezone("Asia/Shanghai")
    # 获取当前日期和时间，并转换为北京时间
    current_datetime = datetime.datetime.now(tz)
    # 格式化输出当前日期时间
    formatted_datetime = current_datetime.strftime(format_)
    return formatted_datetime


def send_text(token, msg):
    send_url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}"
    data = json.dumps(
        {
            "safe": 0,
            "touser": "@all",
            "msgtype": "textcard",
            "agentid": agent_id,
            "textcard": {
                "title": "链接检查情况",
                "description": f'<div class="gray">{get_beijing_time()}</div> <div class="normal">前端导航外链汇总，共收集总数：{msg["total"]}</div><div class="highlight">🌟：{msg["running"]}、❌：{msg["error"]}</div>',
                "url": "https://github.com/rr210/navs",
                "btntxt": "详情查看",
            },
        }
    )
    response = requests.post(send_url, data)
    print(response.text)


def send_qywx_message(message):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={company_id}&corpsecret={app_secret}"
    response = requests.get(url)
    token_json = json.loads(response.text)
    send_text(token=token_json["access_token"], msg=message)
