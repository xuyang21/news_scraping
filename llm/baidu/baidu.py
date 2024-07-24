import os
import requests
import json
from datetime import datetime, timedelta
import utils.utils as proj_utils

get_access_token_url = "https://aip.baidubce.com/oauth/2.0/token"
ERNIE_Speed_8K_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_speed"
access_key = ""

TEST_CASE = 'Israel’s embattled prime minister, Benjamin Netanyahu, began addressing on Wednesday in an eventthat ' \
            'drew throngs of protesters and spotlighted the sharp divide between Republicans and Democratsin their ' \
            'approach to the devastating . A divisive political figure before the conflict began,Netanyahu faces ' \
            'deepening dissent at home, where of Israelis want him to leave office. In the GazaStrip, his right-wing ' \
            'government is approaching 10 months of war, with a death toll of more than39,000 Palestinians, ' \
            'according to local health officials, and facing widespread criticism over thehumanitarian disaster the ' \
            'conflict has unleashed. Netanyahu’s address will be streamed live here.'

class AuthResult:
    def __init__(self, access_token, expires_in, session_key, refresh_token, scope, session_secret, refresh_time=0,
                 error='', error_description=''):
        self.access_token = access_token
        self.expires_in = expires_in
        self.error = error
        self.error_description = error_description
        self.session_key = session_key
        self.refresh_token = refresh_token
        self.scope = scope
        self.session_secret = session_secret
        self.refresh_time = int(datetime.utcnow().timestamp())

    def __str__(self):
        return f"AuthResult(access_token={self.access_token}, out_date={datetime.fromtimestamp(self.refresh_time + self.expires_in)}"


def get_access_token(force):
    expired = False
    exist = True
    if not force:
        try:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/meta.txt') as file:
                meta = file.read()
                auth_result = AuthResult(**json.loads(meta))
                print("[baidu] local auth_result:" + str(auth_result))
                if auth_result.access_token != "None" and auth_result.access_token != "" and auth_result.expires_in != "None" and auth_result.expires_in != "":
                    time_difference = int(datetime.utcnow().timestamp()) - auth_result.refresh_time
                    if time_difference < auth_result.expires_in:
                        return auth_result.access_token
                    else:
                        expired = True
                else:
                    exist = False
                print("[baidu] access_token expired=", expired, "exist=", exist, "try fetch by http")
        except FileNotFoundError:
            print("[baidu] local no cache, try fetch by http")
    # 发送HTTP请求
    data = {'grant_type': 'client_credentials', 'client_id': 'uvyaUSCR3reR3A4ILxgAIt4P',
            'client_secret': 'BsToxS4BwLFLl7QkZSq5nAp09MfVJVUP'}
    response = requests.post(get_access_token_url, data=data)
    # 检查响应状态码
    if response.status_code == 200:
        # 打印响应内容
        print(response.text)
        auth_result = AuthResult(**json.loads(response.text))
        print(auth_result)
        proj_utils.write_to_file(os.path.dirname(os.path.abspath(__file__)) + "/meta.txt", json.dumps(auth_result.__dict__))
        return auth_result.access_token
    else:
        print("[baidu] get_access_token failed")
    return ""


def get_llm_out(data):
    access_token = get_access_token(False)
    if access_token == "":
        print("[baidu] get access_token failed")
    params = {
        "access_token": access_token,
    }
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(ERNIE_Speed_8K_URL, json=data, headers=headers, params=params)
    if response.status_code == 200:
        # 打印响应内容
        print("[baidu] llm raw response" + response.text)
        parse_out = json.loads(response.text)
        result = parse_out['result']
        return result
    return ""


def write_to_file(file_path, content):
    folder_path = os.path.dirname(os.path.abspath(__file__)) + '/generate/' + proj_utils.get_current_date().strftime("%Y-%m-%d")
    if not os.path.exists(folder_path):
        # 如果文件夹不存在，则创建
        os.makedirs(folder_path)
    with open(folder_path + file_path, 'w') as file:
        file.write(content)


content_list = [
    "extract the main information of the news and re-output an English article.\n",
    '将下面这段英文翻译成中文,尽量完整传达原文意思\n',
    '理解下面文章的内容，并重新输出成一篇文章\n',
    '提取下面文章中的重要内容，必须删除其中带有主观意味的内容，去掉含有主观色彩的字段，例如：我们，我认为\n'
    '将下面的文章以新闻的格式输出,结果必须在400字以内，不能含有主观色彩的字段，例如：我们，我认为。不能表达看法\n'
    '将下面的文章以新闻的格式输出，输出结果必须在200字以内，不能含有主观色彩的字段，例如：我们，我认为。不能表达看法\n'
    '对下面这篇新闻进行后期校对，只需要输出新闻正文，不要额外提示词'
]

system_list = [
    'You are a professional news editor who is good at extracting key points from redundant articles as news materials',
    '你是专业的语言学家,擅长将英文翻译成中文',
    '你是专业中文语言学家,擅长提取文章信息，输出结果语句通顺，符合中文阅读习惯',
    '你是中文阅读专家,擅长理解文章语气和语义'
    '你是专业中文新闻编辑,擅长将一篇文章转换成新闻'
    '你是专业中文新闻编辑,擅长将一篇文章转换成新闻'
    '你是专业中文新闻后期编辑,负责新闻校对,确保新闻内容语言通顺、规范，没有拼写错误'
]


def get_llm_summary(llm_in):
    llm_out_list = []
    for index, content in enumerate(content_list):
        llm_in = get_llm_out({'messages': [{"role": "user", "content": content + llm_in}],
                              'system': system_list[index]}).replace("\n", "").replace("\\n", "")
        if llm_in == '':
            return
        llm_out_list.append(llm_in)

    write_to_file('/answer.txt', '\n'.join(llm_out_list))
    return llm_in


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_llm_summary(TEST_CASE)