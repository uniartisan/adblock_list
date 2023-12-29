import sys
import os
import datetime
from raw_download import *

libdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'lib')
rawdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'raw')
outputdir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# 检查网络连接
for i in range(3):
    if isConnected():
        break
else:
    sys.exit('Network Error')

# 下载文件
success = False
while not success:
    success = download()


rawdata = [] # Basic 列表
rawdata_plus = [] # Plus 列表
rawdata_privacy = [] # Privacy 列表
rawdata_lite = [] # Lite 列表
whitelist = []
result = []
result_plus = []
result_privacy = []
result_lite = []
whitelist_rules = []


tag_to_list_mapping = {
    '[+]': rawdata_plus,
    '[P]': rawdata_privacy,
    '[M]': rawdata_lite,  # 注意这里同时也加入到 rawdata_plus
    '[W]': whitelist,
    '[R]': rawdata
}

with open(os.path.join(libdir, 'metadata.txt'), 'r', encoding='UTF-8') as f:
    for line in f:
        temp = line.strip('\n')
        if temp.startswith(('!', '#')) or len(temp) == 0:
            continue
        
        for tag, target_list in tag_to_list_mapping.items():
            if temp.startswith(tag):
                stripped_value = temp.strip(tag)
                target_list.append(stripped_value)
                
                # 特殊情况：'[M]' 同时也加入到 rawdata_plus
                if tag == '[M]':
                    rawdata_plus.append(stripped_value)
                break
        else:
            # 如果没有匹配的 tag，假定是 '[R]'
            rawdata.append(temp.strip('[R]'))




def read_file_and_append_to_list(file_path, result_list):
    with open(file_path, 'r', encoding='UTF-8') as f:
        for line in f:
            temp = line.strip('\n')
            if not temp or temp.startswith('!') or temp.startswith('['):
                continue
            result_list.append(temp)

def filter_result(result):
    filtered_result = []
    for item in result:
        if item.startswith('##') or item.startswith('.') \
                or item.startswith('(') or item.startswith('-') \
                or item.startswith('.com') or item.startswith('/') \
                or item.startswith('&') or item.startswith('$'):
            continue
        else:
            filtered_result.append(item)
    return filtered_result

def process_data(file_list, rawdir):
    result = []
    for file_name in file_list:
        read_file_and_append_to_list(os.path.join(rawdir, file_name), result)
    return result



def deal_with_whitelist(list1, list2):
    """去除 list1 里 list2 的元素"""
    for i in list2:
        if i.startswith('@@'):
            list1.append(i)
        elif i in list1:
            print(i)
            list1.remove(i)
            list1.append("@@" + i)
    return list1


# 排序去重
def sort_the_list(rules_list, whitelist_rules):
    rules_list = deal_with_whitelist(rules_list, whitelist_rules)

    return list(set(rules_list))




# 文本输出
def write_rules_to_file(filename, result_list, date_string, title):
    lenth = len(result_list)
    with open(os.path.join(outputdir, filename), "w", encoding='UTF-8') as f:
        f.write(f"[{title}]\n! Version: {date_string}\n! Title: {title}\n! Expires: 1 days (update frequency)\n")
        f.write(f"! URL = https://github.com/uniartisan/adblock_list\n! Length = {str(lenth)}\n")
        for rule in result_list:
            f.write(f"{rule}\n")







if __name__ == '__main__':
    # 时间戳信息
    time_now = datetime.datetime.now()
    date_string = time_now.strftime('%Y%m%d%H%S')

    result = process_data(rawdata, rawdir)
    result_plus = result + process_data(rawdata_plus, rawdir)
    result_privacy = process_data(rawdata_privacy, rawdir)
    result_lite = process_data(rawdata_lite, rawdir) + filter_result(result)

    whitelist_rules = process_data(whitelist, rawdir)
    result = sort_the_list(result, whitelist_rules)
    result_plus = sort_the_list(result_plus, whitelist_rules)
    result_privacy = sort_the_list(result_privacy, whitelist_rules)
    result_lite = sort_the_list(result_lite, whitelist_rules)


    # 使用函数来写入不同类型的规则
    write_rules_to_file("adblock.txt", result, date_string, "uniartisan's Adblock List")
    write_rules_to_file("adblock_plus.txt", result_plus, date_string, "uniartisan's Adblock List Plus")
    write_rules_to_file("adblock_privacy.txt", result_privacy, date_string, "uniartisan's Privacy List")
    write_rules_to_file("adblock_lite.txt", result_lite, date_string, "uniartisan's Adblock List Lite")
    # 清除缓存文件
    clean_raw_data()