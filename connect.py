#!/usr/bin/env python
#-*- coding: utf-8 -*-
import falcon
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply, ImageReply
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.agent import Agent

class Connect(object):

    def __init__(self):
        interpreter = RasaNLUInterpreter("models/current/nlu")
        self.agent = Agent.load('models/dialogue', interpreter=interpreter)
        print("初始化完成")

    def on_get(self, req, resp):
        query_string = req.query_string
        query_list = query_string.split('&')
        b = {}
        for i in query_list:
            b[i.split('=')[0]] = i.split('=')[1]

        try:
            check_signature(token='114338', signature=b['signature'], timestamp=b['timestamp'], nonce=b['nonce'])
            resp.body = (b['echostr'])
        except InvalidSignatureException:
            pass
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        xml = req.stream.read()
        msg = parse_message(xml)
        if msg.type == 'text':
            replyTxt=self.agent.handle_message(msg.content)[0].get('text')
            reply = TextReply(content=replyTxt, message=msg)
            xml = reply.render()
            resp.body = (xml)
            resp.status = falcon.HTTP_200
        elif msg.type == 'image':
            reply = ImageReply(media_id=msg.media_id, message=msg)
            xml = reply.render()
            resp.body = (xml)
            resp.status = falcon.HTTP_200


app = falcon.API()
connect = Connect()
app.add_route('/connect', connect)