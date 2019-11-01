# -*- coding: UTF-8 -*-
from retrieval_chatbot import control
from ElizaChat import ElizaChat
from poemChat import poemChat
import re
import tensorflow as tf
import falcon
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply, ImageReply

class Connect(object):
    def __init__(self):
        self.retrieval = control.Agent()
        self.pchat = poemChat()
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
            try:
                text = msg.content
                c = len(text)
                if c == 1 and '啊' not in text and '哼' not in text and '嗨' not in text:
                    poem_flag = 24
                    poem = self.pchat.gen_poem(text, poem_flag)
                    replyTxt = self.pchat.pretty_print_poem(poem_=poem)
                    tf.reset_default_graph()

                else:
                    eliza = ElizaChat()
                    replyTxt = eliza.analyze(text)
                    if replyTxt == "@$@":
                        replyTxt, score = self.retrieval.api(text)
                        replyTxt = replyTxt
                reply = TextReply(content=replyTxt, message=msg)
                xml = reply.render()
                resp.body = (xml)
                resp.status = falcon.HTTP_200
            except Exception as e:
                print(e)



        elif msg.type == 'image':
            reply = ImageReply(media_id=msg.media_id, message=msg)
            xml = reply.render()
            resp.body = (xml)
            resp.status = falcon.HTTP_200

app = falcon.API()
connect = Connect()
app.add_route('/connect', connect)

