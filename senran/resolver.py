"""
森蚺解詞儀 (Senran Resolver)
動態解析中文字詞並精準對接底層 Python 物件之屬性與方法。
"""

import difflib
from typing import Any, List, Optional
from senran.dictionary import ALL_LEXICON, PREFIX_RULES, REVERSE_LEXICON


def resolve_attribute_name(target: Any, name: str) -> Optional[str]:
    """
    根據目標物件 target 與傳入的名稱 name，推導出真正的 Python 屬性名稱。
    
    推導優先級：
    1. 原名直取（若本身就是底層既有屬性，或完全匹配英文名）
    2. 全域詞典精準匹配（ALL_LEXICON: 單詞與常用複合詞）
    3. 前綴規則匹配（如「為_」->「is_」、「化_」->「to_」等）
    4. 復合分解匹配（如「取_狀態」->「get_status」）
    5. 目標物件現有屬性之語義推斷（檢查 dir(target) 中的方法是否對應翻譯）
    """
    # 1. 若該名稱為全域詞典精準收錄之文言詞彙，優先查核目標物件是否具備對應英文屬性
    if name in ALL_LEXICON:
        candidate = ALL_LEXICON[name]
        if hasattr(target, candidate):
            return candidate

    # 2. 原名直取（若本身就是底層原生屬性，例如調用原庫英文名或自定義屬性）
    if hasattr(target, name):
        return name

    # 3. 前綴規則匹配 (如 為_數字 -> is_digit / is_numeric)
    for zh_prefix, en_prefix in PREFIX_RULES:
        if name.startswith(zh_prefix):
            remainder = name[len(zh_prefix):]
            translated_remainder = ALL_LEXICON.get(remainder, remainder)
            candidate = f"{en_prefix}{translated_remainder}"
            if hasattr(target, candidate):
                return candidate

    # 4. 下劃線複合拆解 (如 取_文 -> get_text)
    if "_" in name:
        parts = name.split("_")
        translated_parts = [ALL_LEXICON.get(p, p) for p in parts]
        candidate = "_".join(translated_parts)
        if hasattr(target, candidate):
            return candidate

    # 5. 反向推論：遍歷 target 現有屬性，比對是否有能對得上此中文的
    try:
        attrs = dir(target)
    except Exception:
        attrs = []

    # 5.1 如果字典裡有翻譯，即使 hasattr 沒直接命中（例如大小寫微差），做大小寫不敏感比對
    if name in ALL_LEXICON:
        target_en = ALL_LEXICON[name].lower()
        for attr in attrs:
            if attr.lower() == target_en:
                return attr

    # 5.2 檢查是否有現有屬性的反向別名包含此中文名
    for attr in attrs:
        attr_lower = attr.lower()
        if attr_lower in REVERSE_LEXICON:
            if name in REVERSE_LEXICON[attr_lower]:
                return attr

    # 6. 未能解析
    return None


def suggest_available_attributes(target: Any, attempted_name: str, limit: int = 5) -> List[str]:
    """
    當使用者調用找不到的屬性時，從目標物件中給出友善的文言/英文建議。
    """
    try:
        attrs = [a for a in dir(target) if not a.startswith("_")]
    except Exception:
        return []

    # 嘗試找出相似的英文屬性
    candidates = []
    # 收集底層物件屬性對應的所有中文別名
    for attr in attrs:
        aliases = REVERSE_LEXICON.get(attr.lower(), [])
        for alias in aliases:
            candidates.append(f"{alias} ({attr})")

    # 模糊匹配
    matches = difflib.get_close_matches(attempted_name, candidates, n=limit, cutoff=0.3)
    if not matches:
        # 回退到英文模糊匹配
        matches = difflib.get_close_matches(attempted_name, attrs, n=limit, cutoff=0.3)
    return matches
