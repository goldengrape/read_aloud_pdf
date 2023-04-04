# %%
import fitz
import pysubs2
from bs4 import BeautifulSoup


# %%
def convert_PDF_page_to_html(file_path, start_page, end_page):
    pdf_document = fitz.open(file_path)
    htmls = [pdf_document.load_page(i).get_text("html") for i in range(start_page, end_page + 1)]
    return htmls
def read_sub_file(file_path):
    sub=pysubs2.load(file_path, encoding="utf-8")
    return sub
def combine_phrase(sub_data, n):
    N=len(sub_data)
    phrase_list=[]
    for i in range(N):
        start_phrase_index=max(i-n,0)
        end_phrase_index=min(i+n+1,N)
        phrase=' '.join([sub_data[j].text for j in range(start_phrase_index,end_phrase_index)])
        phrase_list.append(phrase)
    return phrase_list

# %%
def estimate_text_width(html_str):
    # 使用BeautifulSoup解析HTML字符串
    soup = BeautifulSoup(html_str, 'html.parser')

    # 初始化总宽度
    total_width = 0.0

    # 遍历所有的<span>标签
    for span_tag in soup.find_all('span'):
        # 获取<span>标签中的文本内容
        span_text = span_tag.get_text()
        # 获取字符数量
        char_count = len(span_text)
        # 获取style属性
        style = span_tag.get('style', '')
        # 从style属性中提取字体大小
        font_size = None
        for item in style.split(';'):
            if 'font-size' in item:
                font_size = float(item.split(':')[1].strip().rstrip('pt'))
                break
        # 如果字体大小存在，累加宽度
        if font_size is not None:
            total_width += char_count * font_size

    return total_width

def find_longest_common_substring(html_str, phrase_str):
    # 使用BeautifulSoup解析HTML字符串
    soup = BeautifulSoup(html_str, 'html.parser')

    # 初始化变量
    max_length = 0  # 最大公共子串的长度
    longest_common_substring = ""
    top = None
    left = None

    # 遍历所有的<p>标签
    for p_tag in soup.find_all('p'):
        # 获取<p>标签中的文本内容
        p_text = p_tag.get_text()

        # 动态规划计算最大公共子串
        dp = [[0] * (len(phrase_str) + 1) for _ in range(len(p_text) + 1)]
        for i in range(1, len(p_text) + 1):
            for j in range(1, len(phrase_str) + 1):
                if p_text[i - 1] == phrase_str[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                    if dp[i][j] > max_length:
                        max_length = dp[i][j]
                        end_index = i - 1
                        # 获取最大公共子串在p_text中的起始位置
                        start_index = end_index - max_length + 1
                        # 获取最大公共子串
                        longest_common_substring = p_text[start_index:end_index + 1]
                        # 获取style属性
                        style = p_tag.get('style', '')
                        # 从style属性中提取top和left坐标
                        for item in style.split(';'):
                            if 'top' in item:
                                top = float(item.split(':')[1].strip().rstrip('pt'))
                            if 'left' in item:
                                left = float(item.split(':')[1].strip().rstrip('pt'))
                            if 'line-height' in item:
                                line_height = float(item.split(':')[1].strip().rstrip('pt'))
                        # 取得该行的长度
                        # estimate_text_width(该行的html字符串)
                        line_length = estimate_text_width(p_tag.prettify())

    # 如果没有找到公共子串，返回空字符串和None
    if max_length == 0:
        return "", None, None

    return longest_common_substring, top, left, line_length, line_height

# %%
def find_phrases_in_html(html, subs, n):
    phrases_list=combine_phrase(subs,n)
    N=len(phrases_list)
    time_location_list=[]
    for i in range(N):
        phrase=phrases_list[i]
        start_time=subs[i].start
        end_time=subs[i].end
        longest_common_substring, top, left,line_length,line_height = find_longest_common_substring(html, phrase)
        # if longest_common_substring:
        time_location_list.append({
                "common_substr_length": len(longest_common_substring),
                "start_time": start_time,
                "end_time": end_time,
                "top": top,
                "left": left,
                "line_length": line_length,
                "line_height": line_height
            })
    return time_location_list
def find_phrases_in_pages(htmls, subs, n):
    time_location_dict={}
    result=[]
    for page_num, html in enumerate(htmls):
        time_location=find_phrases_in_html(html, subs, n)
        time_location_dict[page_num]=(time_location)
    for i in range(len(subs)):
        # 比较每个页面中time_location['common_substr_length']的数值
        # 取最大的那个页面
        max_page_num=max(time_location_dict, key=lambda x: time_location_dict[x][i]['common_substr_length'])
        # 取出该页面的time_location
        time_location=time_location_dict[max_page_num][i]
        # 添加page_num
        time_location['page_num']=max_page_num
        result.append(time_location)
    return result
def merge_time_location(time_location_list):
    # 如果top, left, line_length, line_height, page_num都相同，那么认为是同一行
    # 合并相同行的时间
    result=[]
    for i in range(len(time_location_list)):
        if i==0:
            result.append(time_location_list[i])
        else:
            if time_location_list[i]['top']==time_location_list[i-1]['top'] and \
                time_location_list[i]['left']==time_location_list[i-1]['left'] and \
                time_location_list[i]['line_length']==time_location_list[i-1]['line_length'] and \
                time_location_list[i]['line_height']==time_location_list[i-1]['line_height'] and \
                time_location_list[i]['page_num']==time_location_list[i-1]['page_num']:
                result[-1]['end_time']=time_location_list[i]['end_time']
            else:
                result.append(time_location_list[i])
    return result
def get_time_location(pdf_file_path,
                      sub_file_path,
                      start_page,
                      end_page,
                      n=2):
    htmls=convert_PDF_page_to_html(pdf_file_path, start_page, end_page)
    sub_data = read_sub_file(sub_file_path)
    result=merge_time_location(
    find_phrases_in_pages(htmls, sub_data,n ))
    return result



# %%
if __name__ == '__main__':
    pdf_file_path = 'test_pdf/test2.pdf'
    vtt_file_path = 'test_pdf/test.vtt'
    start_page = 1
    end_page = 2
    result=get_time_location(pdf_file_path, vtt_file_path, start_page, end_page)


