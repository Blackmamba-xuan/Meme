from retrieval_chatbot import control
from ElizaChat import ElizaChat

retrieval = control.Agent()
while True:
    question=input("请输入你的对话: ")
    replyTxt, score = retrieval.api(question)
    print(replyTxt)