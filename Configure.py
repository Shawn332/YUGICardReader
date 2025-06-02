# Configure.py

LANGUAGES = {
    "English": {
        "title": "Yu-Gi-Oh Masterduel Card Reader",
        "select_area": "Select Area",
        "deck_area": "Deck Area",
        "duel_area": "Duel Area",
        "settings": "Settings",
        "change_font": "Change Font",
        "change_frequency": "Change Processing Frequency",
        "change_hotkeys": "Change Hotkeys",
        "start": "Start",
        "stop": "Stop",
        "report": "Report",
        "status_not_running": "Status: Not Running | Area: Not Selected",
        "status_running": "Status: Running | Area: ",
        "no_area_selected": "No area selected.",
        "no_card_detected": "No card detected to report.",
        "hash_string_error": "Failed to generate hash string.",
        "error": "Error",
        "information": "Information",
        "card_details": "Card Details",
        "tier_info": "Tier Info",
        "change_language": "Change Language",
    },
    "Chinese": {
        "title": "游戏王大师决斗读取器",
        "select_area": "选择区域",
        "deck_area": "牌组区域",
        "duel_area": "决斗区域",
        "settings": "设置",
        "change_font": "更改字体",
        "change_frequency": "更改处理频率",
        "change_hotkeys": "更改快捷键",
        "start": "开始",
        "stop": "停止",
        "report": "报告",
        "status_not_running": "状态：未运行 | 区域：未选择",
        "status_running": "状态：运行中 | 区域：",
        "no_area_selected": "未选择区域。",
        "no_card_detected": "没有检测到要报告的卡片。",
        "hash_string_error": "生成哈希字符串失败。",
        "error": "错误",
        "information": "信息",
        "card_details": "卡片详情",
        "tier_info": "等级信息",
        "change_language": "更改语言",
    },
}

current_language = LANGUAGES["English"]

def set_language(language):
    global current_language
    if language in LANGUAGES:
        current_language = LANGUAGES[language]

def get_text(key):
    return current_language.get(key, key)

HOTKEYS = {
    "start": "F1",
    "stop": "F2",
    "report": "F3",
}

def set_hotkey(action, key):
    if action in HOTKEYS:
        HOTKEYS[action] = key

def get_hotkey(action):
    return HOTKEYS.get(action, "")
