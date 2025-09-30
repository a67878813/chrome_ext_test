
# Python 不要将编译后的 .pyc 文件写入 __pycache__ 目录
import sys;sys.dont_write_bytecode = True



from flask import Flask, request, jsonify
from flask_cors import CORS # 导入 CORS

app = Flask(__name__)
CORS(app) # 启用所有路由的 CORS

from tcp_msg import TCP_msg
DEBUG_tcp =True
tcp_debugger = TCP_msg()

import os,re,pyperclip

group_dict={
    "D": r"F:\Program Files (x86)\Vshare\bD\D" ,
    "T": r"F:\Program Files (x86)\Vshare\bD\T" ,
    "d": r"F:\Program Files (x86)\Vshare\bD\d" ,
    "Y": r"F:\Program Files (x86)\Vshare\bD\Y" ,
    "Copy":r"",
}


def extract_content_after_decompress(text):
    """
    查找字符串中所有包含“解压”的实例，并提取其后以空格结尾的内容。


    参数:
        text (str): 待处理的原始字符串。

    返回:
        list: 包含所有匹配到的内容的列表。
              如果没有找到任何匹配项，则返回一个空列表。
    """
    # 这个正则表达式的解释：
    # r"解压\s*(\S+)"
    # “解压”：匹配字面上的“解压”这两个字
    # “\s*”：匹配零个或多个空格（或其他空白字符）
    # “(\S+)”：这是一个捕获组，匹配一个或多个非空白字符（即我们想要的内容）
    #           这个捕获组会一直匹配，直到遇到第一个空白字符为止。
    pattern = r"解压*(\S+)"
    # re.findall() 找到所有匹配模式的实例，并返回捕获组中的内容。
    # 这意味着它会直接返回我们想要提取的部分，而不是整个匹配到的字符串。
    matches = re.findall(pattern, text)
    return matches



def create_and_write_file_with_matches(_folder_path, text_content):
    """
    在指定路径下创建“新建文本文档.txt”，并逐行写入从文本中匹配到的内容。
    
    参数:
        _folder_path (str): 目标文件夹路径。
        text_content (str): 包含需要匹配内容的原始字符串。
    """
    # 1. 确保目标文件夹存在
    if not os.path.exists(_folder_path):
        print(f"错误：文件夹不存在：{_folder_path}")
        return

    # 2. 定义新文件的完整路径
    file_path = os.path.join(_folder_path, "新建文本文档.txt")

    # 3. 提取所有匹配到的内容
    matches = extract_content_after_decompress(text_content)
    
    if not matches:
        print("未在文本中找到任何匹配内容， 新建文本文档.txt 将不会写入。")
        return

    # 4. 逐行写入文件
    try:
        # 'w' 模式会创建新文件或覆盖已有的文件。
        # with 语句确保文件在操作完成后自动关闭。
        with open(file_path, 'a+', encoding='utf-8') as f:
            for item in matches:
                # 写入内容并加上换行符
                f.write(item + '\n')
        print(f"成功创建并写入文件：{file_path}")
        if DEBUG_tcp==True :tcp_debugger.send(message1="密码已写入", message2=fr"源:: {file_path}", message3=fr"至:: {matches}" )
        
    except Exception as e:
        print(f"写入文件时发生错误：{e}")


def only_copy_url(__urlinfo):
    pyperclip.copy(__urlinfo)
    return 0


def  process_url_to_clipboard(__urlinfo):
# 模式：匹配以 "http" 开头的字符串，直到遇到 "提取码" 或换行符为止
    # (\S*) 捕获所有非空白字符，确保能捕获完整的URL
    match = re.search(r'(https?://\S+?)\s+提取码', __urlinfo)
    if match:
        # 提取匹配到的 URL 和提取码
        url = match.group(1)
        # 提取码通常在 "提取码" 后面，我们假设它是一个独立的单词
        code_match = re.search(r'提取码[:：\s]*(\S+)', __urlinfo)
        if code_match:
            code = code_match.group(1)
            # 组合 URL 和提取码，准备写入剪贴板
            content_to_copy = f"{url}&pwd={code}"
            pyperclip.copy(content_to_copy)
            if DEBUG_tcp==True :tcp_debugger.send(message1="网盘地址复制至剪贴板", message2=fr"源:: {content_to_copy}", message3=fr"-" )

        
    return 0
import regex
def remove_emojis_and_special_chars(text):
    """
    删除字符串开头和内部的 emoji 和特殊符号。
    """
    # 匹配字符串开头的所有非中文字符、字母、数字
    pattern_start = r'^[^\u4e00-\u9fa5a-zA-Z0-9]+'
    
    # 匹配字符串内部的所有 emoji
    pattern_emojis = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U0001FB00-\U0001FB6F\U0001FBC0-\U0001FBEF\U0001FC00-\U0001FC6F\U0001FC70-\U0001FCFF\U0001FD00-\U0001FD4F\U0001FD50-\U0001FDFF\U0001FE00-\U0001FE4F\U0001FE50-\U0001FE9F\U0001FEA0-\U0001FEFF\U0001FF00-\U0001FFEF\U0001FFF0-\U0001FFFF\U00020000-\U0002A6DF\U0002A700-\U0002B73F\U0002B740-\U0002B81F\U0002B820-\U0002CEAF\U0002CEB0-\U0002EBEF\U0002F800-\U0002FA1F\U00030000-\U0003134F\U00031350-\U000323AF\U000E0020-\U000E007F\U000E0100-\U000E01EF\U000E01F0-\U000E0FFF]+'

    # 使用 regex.sub() 替换字符串开头的特殊符号
    cleaned_text = regex.sub(pattern_start, '', text)
    
    # 使用 regex.sub() 替换字符串内部的 emoji
    cleaned_text = regex.sub(pattern_emojis, '', cleaned_text)

    return cleaned_text.strip()
def search_and_creat_folder(_title,_group,_urlinfo,_domain):
    # 定义 Windows 文件路径中不允许的字符。
    # 这个正则表达式会匹配 <>:"/\|?* 这些特殊字符，以及末尾的空格。
    invalid_chars_pattern = r'[<>:"/\\|?*]|\s+$'
    # 使用 re.sub() 将所有不合法的字符替换为下划线 '_'
    cleaned_title = re.sub(invalid_chars_pattern, '_', _title)
    cleaned_title2=remove_emojis_and_special_chars(cleaned_title)
    folder_path= group_dict.get(_group)
    if not folder_path:
        print(f"错误：在 group_dict 中找不到群组 '{_group}'。")
        return
    dest_path = os.path.join(folder_path, cleaned_title2)
    if os.path.exists(dest_path):
    #add_unicode_string_win(stdscr,f"目标目录已存在，将覆盖或合并: {dest_path}\n")
        if DEBUG_tcp==True :tcp_debugger.send(message1="目标已存在", message2=fr"源:: {_group}", message3=fr"至:: {dest_path}" )
    else:
        try:
            # 创建文件夹
            os.makedirs(dest_path)
            print(f"文件夹创建成功：{dest_path}")
        except Exception as e:
            print(f"创建文件夹时发生错误：{e}")
        #extracted=extract_content_after_decompress(_urlinfo)
        #建立文件夹，写入密码
        create_and_write_file_with_matches(dest_path, _urlinfo)
        #复制剪贴板
        process_url_to_clipboard(_urlinfo)
    return 0



@app.route('/api/data', methods=['POST'])
def receive_data():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    data_title=data.get('title')
    data_downloadInfo=data.get('downloadInfo')
    data_group=data.get('group')
    data_domain=data.get('domain')
    print("---------------------------------")
    print("接收到来自 Chrome 扩展程序的数据：")
    print(f"标题 (title): {data_title}")
    print(f"下载信息 (downloadInfo): {data_downloadInfo}")
    print(f" (group): {data_group}")
    print(f"(domain): {data_domain}")

    if data_group!= "Copy":
    # 根据group 建立文件夹，写入密码至新建文本文档.txt 复制带提取码的超链接
        search_and_creat_folder(data_title,  data_group,  data_downloadInfo,data_domain)
    else:#copy 组
        #仅处理内容并拷贝至剪贴板
        if data_downloadInfo[:4]=='http':
            only_copy_url(data_downloadInfo)
        else:
            process_url_to_clipboard(data_downloadInfo)

    
    print("---------------------------------")

    return jsonify({"message": "Data received!", "data": ""}), 200




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8899, debug=True)