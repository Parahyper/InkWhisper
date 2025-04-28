from openai import OpenAI

client = OpenAI(api_key="sk-5bfdb50a55124035bc5ae3a513b830ee", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "使用专业正式的语气"},
        {"role": "user", "content": "介绍一下你的收费标准，并回答我充值10块钱能用多久"},
    ],
    stream=False
)

print(response.choices[0].message.content)
