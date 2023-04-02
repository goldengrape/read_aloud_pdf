import openai 
import time


sleep_time=60 
def query_gpt(prompt,cooldown_time=3):
    global sleep_time
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
            # print(f"after sleep 3s, I finished")
            sleep_time = int(sleep_time/2)
            sleep_time = max(sleep_time, 10)
            break
        except:
            print(f"API error, retrying in {sleep_time} seconds...")
            time.sleep(sleep_time)
            sleep_time += 10
            if sleep_time > 120:
                print("API error, aborting...")
                answer=""
                break
    # print(f"Answer: {answer}")
    return answer