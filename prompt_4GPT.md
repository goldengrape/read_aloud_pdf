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