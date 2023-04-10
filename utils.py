import openai 
import time
import re 
import numpy as np


def time_threshold():
    t = 60
    tmin=5
    tmax=120
    while True:
        value = yield t
        if value:
            t = max(t/2,tmin)
        else:
            t = min(t+10,tmax)
sleep_time=time_threshold()
next(sleep_time)
def query_gpt(prompt,cooldown_time=3):
    while True:
        try:
            # start_time=time.time()
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages=[{
                "role": "user", 
                "content": prompt}]
                )
            # print(f"GPT-3 API time: {time.time()-start_time}")
            answer=response.choices[0].message.content.strip()
            time.sleep(cooldown_time)
            sleep_time.send(True)
            break
        except:
            print(f"API error, retrying in {sleep_time} seconds...")
            time.sleep(sleep_time)
            sleep_time.send(False)
            if sleep_time == 120:
                print("API error, aborting...")
                answer=""
                break
    # print(f"Answer: {answer}")
    return answer

LANGUAGES_dict = {
    "English": "en","Chinese": "zh","German": "de","Spanish": "es","Russian": "ru","Korean": "ko","French": "fr","Japanese": "ja","Portuguese": "pt","Turkish": "tr","Polish": "pl","Catalan": "ca","Dutch": "nl","Arabic": "ar","Swedish": "sv","Italian": "it","Indonesian": "id","Hindi": "hi","Finnish": "fi","Vietnamese": "vi","Hebrew": "he","Ukrainian": "uk","Greek": "el","Malay": "ms","Czech": "cs","Romanian": "ro","Danish": "da","Hungarian": "hu","Tamil": "ta","Norwegian": "no","Thai": "th","Urdu": "ur","Croatian": "hr","Bulgarian": "bg","Lithuanian": "lt","Latin": "la","Maori": "mi","Malayalam": "ml","Welsh": "cy","Slovak": "sk","Telugu": "te","Persian": "fa","Latvian": "lv","Bengali": "bn","Serbian": "sr","Azerbaijani": "az","Slovenian": "sl","Kannada": "kn","Estonian": "et","Macedonian": "mk","Breton": "br","Basque": "eu","Icelandic": "is","Armenian": "hy","Nepali": "ne","Mongolian": "mn","Bosnian": "bs","Kazakh": "kk","Albanian": "sq","Swahili": "sw","Galician": "gl","Marathi": "mr","Punjabi": "pa","Sinhala": "si","Khmer": "km","Shona": "sn","Yoruba": "yo","Somali": "so","Afrikaans": "af","Occitan": "oc","Georgian": "ka","Belarusian": "be","Tajik": "tg","Sindhi": "sd","Gujarati": "gu","Amharic": "am","Yiddish": "yi","Lao": "lo","Uzbek": "uz","Faroese": "fo","Haitian Creole": "ht","Pashto": "ps","Turkmen": "tk","Nynorsk": "nn","Maltese": "mt","Sanskrit": "sa","Luxembourgish": "lb","Myanmar": "my","Tibetan": "bo","Tagalog": "tl","Malagasy": "mg","Assamese": "as","Tatar": "tt","Hawaiian": "haw","Lingala": "ln","Hausa": "ha","Bashkir": "ba","Javanese": "jw","Sundanese": "su",}

def remove_pdf_line_breaks(text: str, k=0) -> str:
    print("Removing line breaks...")
    text = re.sub(r'\n+', '\n', text)
    newline_positions = [i for i, char in enumerate(text) if char == '\n']
    distances = [newline_positions[i+1] - pos - 1 for i, pos in enumerate(newline_positions[:-1])]

    if not distances:
        return text

    # 计算平均值和标准差
    mean_distance = np.mean(distances)
    std_distance = np.std(distances)
    print(f"mean_distance: {mean_distance}, std_distance: {std_distance}")
    hist,bins=np.histogram(distances, bins=10)
    print(f"hist: {hist}, bins: {bins}")
    # 计算阈值，大于阈值的认为是硬回车
    # 找到hist中的最大值所对应的bin
    max_bin = bins[np.argmax(hist)]
    threshold_distance = max_bin
    print(f"threshold_distance: {threshold_distance}")
    # 初始化结果字符串
    result = []

    # 遍历字符串中的每个字符
    for i in range(len(text)):
        # 如果当前字符是换行符，检查它是否是硬回车
        if text[i] == '\n':
            # 如果是第一个换行符，则跳过它
            if i == newline_positions[0]:
                result.append(text[i])
                continue

            # 计算当前换行符与前一个换行符之间的距离
            distance = i - newline_positions[newline_positions.index(i) - 1] - 1
            # 如果距离大于平均值加上2倍标准差，认为是硬回车，将其替换为空格
            if distance > threshold_distance:
                result.append(' ')
            else:
                result.append(text[i])
        else:
            result.append(text[i])

    return ''.join(result)