# 抖音热榜关键词提取工具（完整修复版）
import requests
import time
from urllib.parse import quote

# 需要动态获取的加密参数（此处需要根据实际接口更新）
def generate_anti_spider_params():
    return {
        'device_platform': 'webapp',
        'ts': str(int(time.time())),
        'aid': '6383',
        'channel': 'channel_pc_web',
        'detail_list': '1',
        'source': '6',
        'pc_client_type': '1',
        'version_code': '190500',
        'cookie_enabled': 'true',
        'screen_width': '1920',
        'screen_height': '1080',
        'browser_language': 'zh-CN',
        'browser_platform': 'Win32',
        'browser_name': 'Chrome',
        'browser_version': '119.0.0.0',
        'browser_online': 'true',
        'engine_name': 'Blink',
        'os_name': 'Windows',
        'os_version': '10',
        'engine_version': '119.0.0.0',
        'cpu_core_num': '16',
        'device_memory': '8',
        'platform': 'PC',
        'ts': str(int(time.time())),
    }

# 确保Cookie只包含ASCII字符
safe_cookie = "__ac_nonce=0642b127300c9d3b1c1f9; __ac_signature=_02B4Z6wo00f01LjDKSAAAIDBw6.ti2JqnpZvZIXAAEx696;"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Referer': 'https://www.douyin.com/discover',
    'Cookie': safe_cookie  # 需要实际获取
}

url = 'https://www.douyin.com/aweme/v1/web/hot/search/list/'

try:
    # 发送带有完整参数的请求
    response = requests.get(
        url,
        headers=headers,
        params=generate_anti_spider_params(),
        timeout=10
    )

    # 调试输出
    print(f"状态码: {response.status_code}")
    print(f"响应长度: {len(response.text)} 字节")

    # 响应有效性检查
    response.raise_for_status()

    # 尝试解析JSON
    try:
        json_data = response.json()
        if json_data.get('status_code') != 0:
            print(f"接口返回错误: {json_data.get('status_msg')}")
            exit()

        data = json_data.get('data', {}).get('word_list', [])

        print("\n实时热榜TOP5：")
        for i, item in enumerate(data[:5], 1):
            print(f"{i}. {item.get('word')}（热度：{item.get('hot_value')}）")

    except requests.exceptions.JSONDecodeError:
        print("JSON解析失败，响应内容可能是HTML：")
        print(response.text[:500])  # 打印前500字符用于调试
        print("\n可能遇到以下问题：")
        print("1. 需要更新反爬虫参数（特别是ts和加密参数）")
        print("2. Cookie已失效，需要重新获取")
        print("3. 请求频率过高被暂时封禁")

except requests.exceptions.RequestException as e:
    print(f"请求失败: {str(e)}")
    print("建议检查：")
    print("1. 网络连接是否正常")
    print("2. 目标URL是否变更")
    print("3. 是否需要使用代理服务器")