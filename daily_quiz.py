#!/usr/bin/env python3
import os
from datetime import datetime, timedelta

desktop_path = "/mnt/c/Users/ben82/Desktop/"

def get_yesterday_data():
    """取得昨天的學習內容當作測驗題目"""
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    quiz_file = f"/home/ben82/quiz_data_{yesterday_str}.txt"
    
    if not os.path.exists(quiz_file):
        return None, None, yesterday_str
    
    eng_sentence = ""
    eng_meaning = ""
    japanese_words = []
    
    with open(quiz_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("ENG_SENTENCE="):
                eng_sentence = line.replace("ENG_SENTENCE=", "")
            elif line.startswith("ENG_MEANING="):
                eng_meaning = line.replace("ENG_MEANING=", "")
            elif line.startswith("JPN_WORD="):
                parts = line.replace("JPN_WORD=", "").split("|")
                if len(parts) == 2:
                    japanese_words.append((parts[0], parts[1]))
    
    return eng_sentence, eng_meaning, japanese_words, yesterday_str

def generate_quiz():
    result = get_yesterday_data()
    
    if result[0] is None:
        today_str = datetime.now().strftime("%Y-%m-%d")
        content = f"""📝 每日小測驗 {today_str}
{'='*50}
沒有找到昨天的學習內容。
可能是第一天使用，明天開始會有測驗喔！
💡 記得每天都學習，這樣才能鞏固記憶！
"""
        return content
    
    eng_sentence, eng_meaning, japanese_words, yesterday_str = result
    
    content = f"""📝 每日小測驗 {datetime.now().strftime("%Y-%m-%d")}
（測驗範圍：{yesterday_str} 的學習內容）
{'='*50}

🇬🇧 英文測驗（第1題）
{'-'*50}
請回答以下問題：

1. 昨天的英文句子是什麼？
   （提示：意思是「{eng_meaning}」）

2. 這個句子的KK音標是什麼？
   （提示：4個字母的符號）

3. 用這個句子造一個你自己的句子

{'='*50}

🇯🇵 日文測驗（第2題）
{'-'*50}
請回答以下問題：

"""
    # 從10個單字中選5個測驗
    import random
    selected = random.sample(japanese_words, min(5, len(japanese_words)))
    for i, (japanese, meaning) in enumerate(selected, 1):
        content += f"{i}. 這個詞彙是什麼意思？\n   {japanese}\n\n"

    content += f"""
{'='*50}
💡 答題技巧：
- 先看日文，嘗試回想意思
- 不確定的先跳過，別浪費太多時間
- 全部答完後再對答案

📋 答案會在明天早上9點公佈喔！

{'='*50}
由 Hermes Agent 自動生成
"""

    # 儲存到桌面
    output_file = f"{desktop_path}每日測驗_{datetime.now().strftime('%Y-%m-%d')}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return content

content = generate_quiz()
print(content)
