import os
import requests
import random
import time
from fake_useragent import UserAgent

# 搜索关键词
query = "标准硬拉"
# 目标文件夹
save_dir = "C:\\Users\\xusir\\Desktop\\college\\github\\Ultralight-SimplePose\\Ultralight-SimplePose\\data\\fitness_images_硬拉"
# 确保保存目录存在
os.makedirs(save_dir, exist_ok=True)

# 百度图片搜索 API URL
url = f"https://image.baidu.com/search/acjson?tn=resultjson_com&logid=undefined&ipn=rj&ct=201326592&is=&fp=result&queryWord={query}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&word={query}&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&expermode=&pn=0&rn=30&gsm=1e&1558015051502="

# 使用 UserAgent 库生成随机 User-Agent
ua = UserAgent()

# 设置请求头
headers = {
    "User-Agent": ua.random,
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://image.baidu.com"
}

# 发送请求获取搜索结果页面
response = requests.get(url, headers=headers)
response.raise_for_status()

# 解析 JSON 数据
data = response.json()

# 检查图片数据
if 'data' not in data:
    print("没有找到图片数据。")

    exit()

# 下载图片
for i, item in enumerate(data['data']):
    try:
        if 'thumbURL' not in item:
            continue
        img_url = item['thumbURL']

        # 下载图片
        img_response = requests.get(img_url, headers=headers, stream=True)
        img_response.raise_for_status()

        # 保存图片
        img_path = os.path.join(save_dir, f"image_{i + 1}.jpg")
        with open(img_path, "wb") as img_file:
            for chunk in img_response.iter_content(1024):
                img_file.write(chunk)
        print(f"下载完成: {img_path}")

        # 随机延迟
        time.sleep(random.uniform(1, 3))

    except Exception as e:
        print(f"下载失败: {e}")

print("所有图片下载完成。")
