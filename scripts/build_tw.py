#!/usr/bin/env python3
"""Build a Taiwan Traditional Chinese Star Citizen global.ini from 42Kit's half localization.

Uses OpenCC s2twp; applies original, narrowly scoped Taiwan phrasing tweaks.
Does NOT copy TCTP translations or alter item/place/ship English names.
"""
from pathlib import Path
from collections import Counter
import hashlib, json, re, sys, datetime
from opencc import OpenCC

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources' / '42kit-half.ini'
OUTPUT = ROOT / 'output' / 'global.ini'
MANIFEST = ROOT / 'output' / 'build-report.json'
cc = OpenCC('s2twp')
# Terminology (common functional labels, not copied from TCTP's copyrightable passages).
TERM = (
    ('展廳開放日', '展覽館開放日'),
    ('空間站', '太空站'),
    ('航天器', '太空船'),
    ('宇宙飛船', '太空船'),
    ('飛船', '太空船'),
    ('揹包', '背包'),
    ('裝置和裝置', '裝備與裝置'),
    ('停機坪', '停機坪'),
    ('當前位置', '目前位置'),
    ('當前地點', '目前地點'),
    ('圖示', '圖示'),
    ('登陸', '登陸'),
    ('客戶端', '用戶端'),
    ('獲取', '取得'),
    ('該選項', '此選項'),
    ('訪問本地庫存', '存取本地庫存'),
    ('訪問儲存容器', '存取儲存容器'),
    ('訪問你的庫存', '存取你的庫存'),
    ('無法訪問', '無法存取'),
    ('進行互動', '互動'),
    ('倉庫管理員', '倉庫管理員'),
    ('請單擊', '請按一下'),
)
# Fresh rewrites of a small, highly visible set of player tips; do not lift full text from TCTP.
REWRITES = {
    'Hints_Shopping1': '多數太空站都設有商店。展開旅程前，不妨先購買需要的物資與裝備。',
    'Hints_Shopping2': '使用互動模式選擇「購買」，或透過商店終端機瀏覽並購買商品。',
    'Hints_Shopping3': '購買前，你可以先在商店中「試穿」或「檢視」商品。',
    'Hints_Shopping_Title': '購物',
    'Hints_Inventory_Title': '物品庫存',
    'Hints_Inventory_ItemPurchased': '購買的商品已送往當地物品庫存。身處該地點時，可從本地庫存取出。',
    'Hints_Inventory_ItemPurchased_Title': '本地庫存',
    'Hints_Inventory_ContainerFull': '儲物容器有容量限制。若空間不足，便無法再放入超出容量的物品。',
    'Hints_Inventory_ContainerSizeLimits': '儲物容器也有尺寸限制，太大的物品將無法放入。',
    'Hints_Inventory_Open': '拖放物品，即可在儲物容器與個人物品庫存之間移動裝備，包含身上穿戴或手持的物品。',
    'Hints_Inventory_OpenInVehicle': '使用畫面兩側的分頁，切換個人物品庫存與各個儲物容器。',
    'Hints_Inventory_OpenWithNoContainer': '穿戴衣物、護甲和背包，以使用它們的儲物空間。開啟儲物容器即可管理物品；若要丟棄物品，請將它拖曳到張開手掌的圖示。',
    'Hints_Inventory_HomeItemAdded_Title': '庫存新增物品',
    'Hints_Inventory_VehicleDestroyed': '載具遭到摧毀時，部分物品可能倖存。請搜尋殘骸找回物品，牽引光束或許能派上用場。',
    'Hints_Inventory_SpawnPointExit': '想查看物品放在哪裡？開啟 mobiGlas 的「資產」應用程式，即可追蹤物品及其目前位置。',
    'Hints_Inventory_VehicleStorageUsed': '使用 mobiGlas 的「資產」應用程式查詢物品所在位置。',
    'Hints_Inventory_InvalidClothingArmorEquip_Title': '衣物與太空衣',
    'Hints_Inventory_Tracking_Title': '物品庫存追蹤',
    'Hints_Inventory_ContainerSizeLimits_Title': '儲物容器',
    '2019_Ann_Sale_Day1': '展覽館開放日第 1 天',
}
# Guard source's formatting syntax, placeholder and token stream. OpenCC works on Chinese chars
# and should not touch these, but fail fast if it ever does.
TOKENS = re.compile(r'(~[A-Za-z_][\w.]*\([^\r\n]*?\)|<[A-Za-z/][^>\r\n]*>|\\[nrt]|%(?:\d+\$)?[-+ #0]*(?:\d+)?(?:\.\d+)?[a-zA-Z]|\{[A-Za-z_][\w.]*\}|\$\{[^}]+\})')
raw = SOURCE.read_bytes()
if not raw.startswith(b'\xef\xbb\xbf'): raise RuntimeError('Expected source UTF-8 BOM')
lines = raw.decode('utf-8-sig').splitlines()
keys = set(); output = []; diffs = 0; rewrite_hits = []; terminology_hits = Counter(); token_fail = []
for idx,line in enumerate(lines,1):
    if '=' not in line: raise ValueError(f'Non KV line {idx}')
    key, value = line.split('=', 1)
    if key in keys:raise ValueError(f'Duplicate {key} at line {idx}')
    keys.add(key)
    converted = cc.convert(value)
    for source, replacement in TERM:
        if source != replacement and source in converted:
            count = converted.count(source)
            terminology_hits[source+' -> '+replacement]+=count
            converted = converted.replace(source,replacement)
    if key in REWRITES:
        if TOKENS.findall(value) == TOKENS.findall(REWRITES[key]):
            converted = REWRITES[key];rewrite_hits.append(key)
        else:
            raise ValueError('Unsafe manually edited tokens: '+key)
    if TOKENS.findall(value)!=TOKENS.findall(converted):
        token_fail.append([idx,key,TOKENS.findall(value)[:5],TOKENS.findall(converted)[:5]])
        if len(token_fail)>8:raise ValueError('Token changes: '+repr(token_fail))
    if converted!=value:diffs+=1
    output.append(key+'='+converted)
if token_fail:raise ValueError('Token changes: '+repr(token_fail))
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_bytes(b'\xef\xbb\xbf'+('\n'.join(output)+'\n').encode('utf-8'))
report={'date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source':'https://ini.42kit.com/half/global.ini',
        'source_index':'https://github.com/StarCitizenToolBox/Api/blob/main/localizations/chinese_(simplified).json',
        'declared_source_version':'4.10.2(PU)_CNE_V2 (2026-10-14)',
        'source_sha256':hashlib.sha256(raw).hexdigest(),
        'source_bytes':len(raw),'output_bytes':OUTPUT.stat().st_size,
        'output_sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        'key_count':len(keys),'updated_value_count':diffs,'manual_rewrite_count':len(rewrite_hits),
        'manual_rewrite_keys':rewrite_hits, 'term_replacement_counts':dict(terminology_hits),
        'unmodified_key_structure':True,'place_item_names':'left in source English; manual spot-check needed',
        'notes':'OpenCC s2twp + curated common Taiwanese terms + limited hand edits; not human proofread in entirety'}
MANIFEST.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['key_count','updated_value_count','manual_rewrite_count','output_bytes','output_sha256']},ensure_ascii=False))
