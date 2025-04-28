import  InitIW
import  UiIW
import  LLMs_api
if __name__ == '__main__':
    # 初始化操作函数
    InitIW.init_book()
    # InitIW.init_config()
    UiIW.UiIW()
    # 测试LLMs_api
    # print("正在执行")
    # input_messages = [
    #     "写一首诗",
    # ]
    # answer=LLMs_api.get_deepseek_responses(input_messages)
    # print(answer)
    # print("执行成功")