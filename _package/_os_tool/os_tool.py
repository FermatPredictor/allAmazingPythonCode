import os
import re

def batch_show_name(path):
    # 函數功能: 顯示指定路徑下，該層的檔案及資料夾名稱
    for fname in os.listdir(path):
        print(os.path.join(path, fname))
        

def recursive_show_name(path):
    # 函數功能: 遞迴顯示指定路徑下的所有檔案及資料夾名稱
    for fd in os.listdir(path):
        full_path = os.path.join(path,fd)
        if os.path.isdir(full_path):
            print('資料夾:',fd)
            recursive_show_name(full_path)
        else:
            print('檔案:',fd)
            
def search_in_path(path, find_regex):
    """
    函數功能: 遞迴搜索路徑下的所有檔案名稱是否吻合正則表達式
    回傳吻合的所有檔名
    """
    res = []
    for fd in os.listdir(path):
        full_path = os.path.join(path,fd)
        if not os.path.isfile(full_path):
            res += search_in_path(full_path, find_regex)
            continue
        if re.search(find_regex, fd):
            res.append(fd)
    return res

if __name__=='__main__':
    path = r'C:\Users\User\Desktop\leetcodeSolutionPython\LeetcodeSolutionForPython'
    recursive_show_name(path)
    print(search_in_path(path, '^(_)*242_'))