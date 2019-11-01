from poemChat import poemChat
import re
import tensorflow as tf

pchat = poemChat()

while True:
    text = input("请输入你的对话: ")
    poem_flag = 24
    poemList = re.findall("于(.+)的", text)
    key = poemList[0][0]
    poem = pchat.gen_poem(key, poem_flag)
    replyTxt = pchat.pretty_print_poem(poem_=poem)
    tf.reset_default_graph()
    print(replyTxt)