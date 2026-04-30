#!/usr/bin/env python3
import urllib.request
import xml.etree.ElementTree as ET
import html
import os
from datetime import datetime, timedelta

desktop_path = "/mnt/c/Users/ben82/Desktop/"

# 英文詞彙（基礎到中級，每組10個）
english_groups = [
    # 第1組
    [
        ("Hello!", "你好", "/həˈlo/", "hə-LOH"),
        ("Good morning!", "早上好", "/ɡʊd ˈmɔrnɪŋ/", "good MOR-ning"),
        ("Thank you!", "謝謝你", "/θæŋk ju/", "THANK you"),
        ("You're welcome", "不客氣", "/jʊr ˈwɛl.kəm/", "you're WEL-come"),
        ("How are you?", "你好嗎", "/haʊ ɑr ju/", "HOW are YOU"),
        ("I'm fine", "我很好", "/aɪm faɪn/", "I'm FINE"),
        ("Nice to meet you", "很高興認識你", "/naɪs tu mit ju/", "NICE to MEET you"),
        ("What's your name?", "你叫什麼名字", "/wʌts jɔr nem/", "WHAT's your NAME"),
        ("Where are you from?", "你來自哪裡", "/wɛr ɑr ju frʌm/", "WHERE are you FROM"),
        ("See you later", "再見", "/si ju ˈleɪtɚ/", "SEE you LATER"),
    ],
    # 第2組
    [
        ("Water", "水", "/ˈwɔtɚ/", "WA-ter"),
        ("Coffee", "咖啡", "/ˈkɔfɪ/", "COFF-ee"),
        ("Food", "食物", "/fud/", "FOOD"),
        ("Book", "書", "/bʊk/", "BOOK"),
        ("House", "房子", "/haʊs/", "HOUSE"),
        ("Car", "車", "/kɑr/", "CAR"),
        ("Phone", "電話", "/fon/", "PHONE"),
        ("Time", "時間", "/taɪm/", "TIME"),
        ("Money", "錢", "/ˈmʌnɪ/", "MUH-nee"),
        ("Friend", "朋友", "/frɛnd/", "FRIEND"),
    ],
    # 第3組
    [
        ("Breakfast", "早餐", "/ˈbrɛkfəst/", "BREAK-fast"),
        ("Lunch", "午餐", "/lʌntʃ/", "LUNCH"),
        ("Dinner", "晚餐", "/ˈdɪnɚ/", "DIN-ner"),
        ("Restaurant", "餐廳", "/ˈrɛstərɑnt/", "RES-tau-rant"),
        ("Station", "車站", "/ˈsteʃən/", "STA-tion"),
        ("Airport", "機場", "/ˈɛrpɔrt/", "AIR-port"),
        ("Hospital", "醫院", "/ˈhɑspɪtəl/", "HOS-pi-tal"),
        ("School", "學校", "/skul/", "SCHOOL"),
        ("Office", "辦公室", "/ˈɔfɪs/", "OF-fice"),
        ("Company", "公司", "/ˈkʌmpənɪ/", "COM-pa-ny"),
    ],
    # 第4組
    [
        ("Monday", "星期一", "/ˈmʌndeɪ/", "MON-day"),
        ("Tuesday", "星期二", "/ˈtuːzdeɪ/", "TUES-day"),
        ("Wednesday", "星期三", "/ˈwɛnzdeɪ/", "WED-nes-day"),
        ("Thursday", "星期四", "/ˈθɝzdeɪ/", "THURS-day"),
        ("Friday", "星期五", "/ˈfraɪdeɪ/", "FRI-day"),
        ("Saturday", "星期六", "/ˈsætɚdeɪ/", "SAT-ur-day"),
        ("Sunday", "星期日", "/ˈsʌndeɪ/", "SUN-day"),
        ("Weekend", "週末", "/ˈwikɛnd/", "WEEK-end"),
        ("Morning", "早上", "/ˈmɔrnɪŋ/", "MOR-ning"),
        ("Evening", "晚上", "/ˈivnɪŋ/", "EVE-ning"),
    ],
    # 第5組
    [
        ("Delicious", "美味的", "/dɪˈlɪʃəs/", "de-LI-cious"),
        ("Expensive", "昂貴的", "/ɪkˈspɛnsɪv/", "ex-PEN-sive"),
        ("Cheap", "便宜的", "/tʃip/", "CHEAP"),
        ("Beautiful", "漂亮的", "/ˈbjutəfəl/", "BEAU-ti-ful"),
        ("Big", "大的", "/bɪɡ/", "BIG"),
        ("Small", "小的", "/smɔl/", "SMALL"),
        ("Hot", "熱的", "/hɑt/", "HOT"),
        ("Cold", "冷的", "/koʊld/", "COLD"),
        ("Fast", "快的", "/fæst/", "FAST"),
        ("Slow", "慢的", "/sloʊ/", "SLOW"),
    ],
]

# 日文N4→N3詞彙（每組10個）
japanese_groups = [
    # 第1組
    [
        ("料理（りょうり）", "吃飯/烹飪"),
        ("映画（えいが）", "電影"),
        ("散歩（さんぽ）", "散步"),
        ("計画（けいかく）", "計劃"),
        ("興味（きょうみ）", "興趣"),
        ("経験（けいけん）", "經驗"),
        ("主張（しゅちょう）", "主張"),
        ("説明（せつめい）", "說明"),
        ("調査（ちょうさ）", "調查"),
        ("結果（けっか）", "結果"),
    ],
    # 第2組
    [
        ("約束（やくそく）", "約定"),
        ("準備（じゅんび）", "準備"),
        ("連絡（れんらく）", "聯絡"),
        ("質問（しつもん）", "問題"),
        ("確認（かくにん）", "確認"),
        ("理由（りゆう）", "理由"),
        ("内容（ないよう）", "內容"),
        ("印象（いんしょう）", "印象"),
        ("表情（ひょうじょう）", "表情"),
        ("関係（かんけい）", "關係"),
    ],
    # 第3組
    [
        ("努力（どりょく）", "努力"),
        ("成功（せいこう）", "成功"),
        ("失敗（しっぱい）", "失敗"),
        ("目標（もくひょう）", "目標"),
        ("現在（げんざい）", "現在"),
        ("最近（さいきん）", "最近"),
        ("一般（いっぱん）", "一般"),
        ("必要（ひつよう）", "必要"),
        ("完全（かんぜん）", "完全"),
        ("危険（きけん）", "危險"),
    ],
    # 第4組
    [
        ("社会的（しゃかいてき）", "社會性的"),
        ("具体的な（ぐたいてき）", "具體的"),
        ("重要な（じゅうよう）", "重要的"),
        ("特別な（とくべつ）", "特別的"),
        ("基本的な（きほんてき）", "基本的"),
        ("様々な（さまざま）", "各種各樣的"),
        ("有効な（ゆうこう）", "有效的"),
        ("有名な（ゆうめい）", "有名的"),
        ("新鮮な（しんせん）", "新鮮的"),
        ("複雑な（ふくざつ）", "複雜的"),
    ],
    # 第5組
    [
        ("続ける（、つける）", "繼續"),
        ("変える（かえる）", "改變"),
        ("調べる（しらべる）", "調查"),
        ("考える（かんがえる）", "思考"),
        ("始める（はじめめる）", "開始"),
        ("付ける（つける）", "附加"),
        ("合わせる（あわせる）", "配合"),
        ("生まれる（うまれる）", "誕生"),
        ("過ごす（すごす）", "度過"),
        ("伝える（つたえる）", "傳達"),
    ],
]

def get_daily_content():
    today = datetime.now()
    day_of_year = today.timetuple().tm_yday
    
    # 英文：每5天換一組（每組10個）
    eng_group_index = (day_of_year - 1) // 5 % len(english_groups)
    eng_group = english_groups[eng_group_index]
    
    # 日文：每5天換一組（每組10個）
    jpn_group_index = (day_of_year - 1) // 5 % len(japanese_groups)
    jpn_group = japanese_groups[jpn_group_index]
    
    week = (day_of_year - 1) // 7 + 1
    
    return today.strftime("%Y-%m-%d"), eng_group, jpn_group, week

def generate_tts_text(eng_group, jpn_group):
    eng_sentence, eng_meaning, eng_kk, eng_stress = eng_group[0]
    tts_text = f"""英文學習時間！
    
今天的英文，十個詞彙：

"""
    for i, (sentence, meaning, kk, stress) in enumerate(eng_group, 1):
        tts_text += f"第{i}個：{sentence}，意思是{meaning}。\n"

    tts_text += f"""
現在是日文學習時間！
今天學習十個日文詞彙：
"""
    for i, (japanese, meaning) in enumerate(jpn_group, 1):
        tts_text += f"第{i}個：{japanese}，意思是{meaning}。\n"

    return tts_text

def save_quiz_data(eng_group, jpn_group, date_str):
    """儲存今日內容供明天測驗用"""
    quiz_file = f"/home/ben82/quiz_data_{date_str}.txt"
    with open(quiz_file, 'w', encoding='utf-8') as f:
        for sentence, meaning, kk, stress in eng_group:
            f.write(f"ENG:{sentence}|{meaning}|{kk}\n")
        for japanese, meaning in jpn_group:
            f.write(f"JPN:{japanese}|{meaning}\n")

# 主程式
today_str, eng_group, jpn_group, week = get_daily_content()
save_quiz_data(eng_group, jpn_group, today_str)

# 生成學習內容
content = f"""📚 每日語言學習 {today_str}
{'='*50}

🇬🇧 英文詞彙（第{week}週）
{'-'*50}
📝 今日十個英文詞彙：
"""
for i, (sentence, meaning, kk, stress) in enumerate(eng_group, 1):
    content += f"\n{i}. {sentence} → {meaning}\n   KK音標：{kk}\n   發音：{stress}\n"

content += f"""
{'='*50}

🇯🇵 日文詞彙（N4→N3）
{'-'*50}
📝 今日十個日文詞彙：
"""
for i, (japanese, meaning) in enumerate(jpn_group, 1):
    content += f"\n{i}. {japanese} → {meaning}\n"

content += f"""
{'='*50}
💡 記憶技巧：
- 第一天：看著中文說日文/英文
- 第二天：看著日文/英文說中文
- 第三天：嘗試自己造句

{'='*50}
🎯 本週目標（第{week}週）：
英文：掌握基礎詞彙，日常表達更順暢
日文：累積N3詞彙量

💬 今日練習：
英文：用今天的單字每個造一個句子
日文：嘗試用今天的單字每個造一個句子

{'='*50}
📝 明日小測驗預告：
明天晚上我會考你這10個英文+10個日文喔！
準備好了嗎？ 💪

{'='*50}
由 Hermes Agent 自動生成
"""

# 儲存到桌面
output_file = f"{desktop_path}每日學習_{today_str}.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(content)
print(f"\n✅ 已儲存到：{output_file}")
