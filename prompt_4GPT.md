# [PDF_to_text.py](PDF_to_text.py)

## 目的

将PDF指定的页面转换成纯文本文件

## 方法

1. 读取PDF指定页面，可以是连续页面
2. 依次读取指定页面的文本内容
3. 使用GPT将每页的文本内容整理，仅仅保留正文的部分，去除页眉页脚
4. 将多页整理后的文本保存成一个txt文件 

<!-- ## 函数描述要求

我准备使用python撰写上述过程的程序，请使用函数式编程的风格构思上述过程，给出所需要的函数，最终以main()函数调用，现在不必写出具体的函数实现过程，请仅仅列出每个函数的描述、输入、输出。
我准备使用PyMuPDF，由于你的数据内容截至到2021年9月，因此新引入的函数/方法你可能不清楚，所以请注明所使用的PyMuPDF版本号。 -->

## 函数具体描述

函数设计如下：

read_pdf_pages(pdf_file: str, start_page: int, end_page: int) -> List[str]
描述：读取指定范围内的PDF页面并将每页的文本内容转换为纯文本。
输入：
pdf_file：PDF文件路径。
start_page：起始页码（从0开始计数）。
end_page：结束页码（包含在内）。
输出：包含指定页面纯文本内容的列表。

clean_text(text: str) -> str
描述：使用GPT删除文本中的页眉和页脚、图像标注等。
输入：包含页眉和页脚的文本字符串。
输出：仅包含正文部分的文本字符串。

save_to_txt(text: str, output_file: str) -> None
描述：将给定文本保存到指定的txt文件中。
输入：
text：要保存的文本字符串。
output_file：输出txt文件的路径。
输出：无。

main(pdf_file: str, start_page: int, end_page: int, output_file: str) -> None
描述：主函数，负责调用其他函数以完成PDF页面转换为纯文本文件的任务。
输入：
pdf_file：PDF文件路径。
start_page：起始页码（从0开始计数）。
end_page：结束页码（包含在内）。
output_file：输出txt文件的路径。
输出：无。

PyMuPDF版本：1.18.19。

请按上述要求，写出python程序


# PDF_speach_to_video

## 目的
在朗读PDF时，显示在朗读位置显示出高亮区域

## 方法
1. 读取PDF指定页面，可以是连续页面
2. 依次读取指定页面的内容，转换成html
3. 读取字幕文件(vtt)，该字幕文件中，每一条字幕是一个单词
4.1. 对于字幕中的每一个单词，找到其前后各n个词，组成短语，在PDF内容中找到最可能的短语，然后从html中找到该短语所在的位置
4.2. 将PDF页面渲染成图片，在短语所在位置叠加上半透明浅色矩形，以标记出朗读位置。
4.3. 带有朗读标记的PDF图片的持续时间为该短语的持续时间。据此将图片连接成视频

<!-- ## 函数描述要求

我准备使用python撰写上述过程的程序，请使用函数式编程的风格构思上述过程，给出所需要的函数，最终以main()函数调用，现在不必写出具体的函数实现过程，请仅仅列出每个函数的描述、输入、输出。
我准备使用PyMuPDF，由于你的数据内容截至到2021年9月，因此新引入的函数/方法你可能不清楚，所以请注明所使用的PyMuPDF版本号。 -->

## 函数具体描述

请使用PyMuPDF，不要使用opencv

1. read_pdf_pages(file_path, start_page, end_page)
描述：读取指定PDF文件的连续页面。
输入：
file_path：PDF文件路径（字符串）
start_page：起始页面（整数）
end_page：结束页面（整数）
输出：包含PDF页面的列表

2. convert_pages_to_html(pdf_pages)
描述：将PDF页面转换为HTML。
输入：包含PDF页面的列表
输出：包含HTML页面的列表

3. read_vtt_file(file_path)
描述：读取字幕文件（vtt格式）。
输入：字幕文件路径（字符串）
输出：字幕数据（列表）

4. find_phrases_in_html(html_pages, vtt_data, n)
描述：从HTML中找到与字幕数据相对应的短语。
输入：
html_pages：包含HTML页面的列表
- vtt_data：字幕数据（列表）
- n：单词前后各取的词数（整数）
- 输出：包含短语及其在HTML中的位置信息的列表

5. render_pdf_pages_with_highlight(pdf_pages, phrases_positions)
描述：将高亮区域添加到PDF页面，并将其渲染为图片。
输入：
pdf_pages：包含PDF页面的列表
phrases_positions：包含短语及其在HTML中的位置信息的列表
输出：包含带有高亮区域的PDF页面图片的列表

6. create_video_from_images(images, vtt_data, output_path)
描述：根据带有高亮区域的PDF页面图片和字幕数据创建视频。
输入：
images：包含带有高亮区域的PDF页面图片的列表
vtt_data：字幕数据（列表）
output_path：输出视频文件的路径（字符串）
输出：无

7.main()
描述：主函数，调用上述所有函数。
输入：无
输出：无