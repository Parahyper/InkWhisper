import os
from openai import OpenAI

# API统一调用函数
def get_openai_responses(input_messages,llms):
    if llms == "DeepSeek":
        return get_deepseek_responses(input_messages)
    elif llms == "Doubao":
        return get_doubao_responses(input_messages)
    pass


# 调用deepseek模型
def get_deepseek_responses(input_messages):
    print("调用deepseek模型")
    answer = []
    print(input_messages)
    # 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
    # 初始化Ark客户端，从环境变量中读取您的API Key
    client = OpenAI(base_url="https://ark.cn-beijing.volces.com/api/v3",api_key="")
    # print(message)
    print(input_messages)
    response = client.chat.completions.create(
        # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
        model="deepseek-r1-250120",
        # model="doubao-1-5-thinking-pro-250415",
        messages=[
            {"role": "user", "content": "使用专业正式的语气，并且语言干练简洁"},
            {"role": "user", "content": input_messages}
        ]
    )
    # print(answer)
    return response.choices[0].message.content

# 调用doubao模型
def get_doubao_responses(input_messages):
    print("调用doubao模型")
    answer = []
    print(input_messages)
    # 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
    # 初始化Ark客户端，从环境变量中读取您的API Key
    client = OpenAI(base_url="https://ark.cn-beijing.volces.com/api/v3",api_key="")
    # print(message)
    print(input_messages)
    response = client.chat.completions.create(
        # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
        model="doubao-1-5-thinking-pro-250415",
        messages=[
            {"role": "user", "content": "使用专业正式的语气，并且语言干练简洁"},
            {"role": "user", "content": input_messages}
        ]
    )
    # print(answer)
    return response.choices[0].message.content