# coding=utf-8
from flask import Flask, request, abort

from .WechatMP import WechatMP
import xmltodict
from flask import request, session, jsonify, g
from app.models import db, Volunteer, to_json
from . import wechat

Token = 'eryoyoyo'
appId = 'wx05c50b6c4968445f'
secret = '15c1b9330318cc0afdf6180bf05a7a2b'
wmp = WechatMP(Token=Token, appId=appId, secret=secret)


# @wechat.before_request
def checkSignature():
    signature = request.values.get('signature')
    timestamp = request.values.get('timestamp')
    nonce = request.values.get('nonce')
    echostr = request.values.get('echostr')  # 仅在验证服务器时使用次参数
    if not wmp.checkSignature(timestamp=timestamp, nonce=nonce, signature=signature):
        abort(404)
    if echostr:
        return echostr


@wechat.route('/send')
def send_msg():
    wmp.send_msg_test()
    return "wooooo"


def send_event(content):
    # wmp.send_msg("ooVV56IKYPX8ff4xzYCfYI3EO5Ng", content)
    wmp.send_msg(content=content)

@wechat.route('/', methods=['get', 'post'])
def main():
    msg = xmltodict.parse(request.data).get('xml')
    print("xmltodict.parse(request.data).get('xml'):")
    print(msg)
    msgType = msg.get('MsgType')
    res = wmp.replyText(msg, 'Hi~ 终于等到你啦，这里是阳光养老院，您关注之后会接受到该养老院的相关信息，如果不需要的话记得取关哟')
    if msgType == 'text':
        res = wmp.replyText(msg, "您输入的是" + msg.get('Content') + "，可是我看不懂呢，这里只是一个养老院而已了啦")
        wmp.send_msg()
        print("res:")
        print(res)
    if msgType == 'image':
        res = wmp.replyImage(msg, msg.get('MediaId'))
    """ And More Type of Message"""
    if msgType == 'event':
        if msg.get('Event') == 'subscribe':
            # 关注后回复
            open_id = msg.get('FromUserName')
            # add_open_id(open_id)
            res = wmp.replyText(msg, 'Hi~\n终于等到你啦，这里是阳光养老院，您关注之后会接受到该养老院的相关信息，如果不需要的话记得取关哟')
    print("xmltodict.unparse(res):")
    print(xmltodict.unparse(res))
    return xmltodict.unparse(res)


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8001)
