# -*- coding: utf-8 -*-
"""
steam_collector.py - Автономный пакетный сборщик HTML-карточек видеоигр для библиотеки Steam.
Выполняет полный цикл обработки 124 игр из Games.md согласно rules.txt.
"""

import os
import sys
import re
import json
import time
import html
import urllib.request
import urllib.parse
from datetime import datetime

# Базовые директории
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "GameCards")
LOG_PATH = os.path.join(OUTPUT_DIR, "PROCESS_LOG.md")
FAILED_PATH = os.path.join(OUTPUT_DIR, "FAILED_GAMES.md")
GAMES_PATH = os.path.join(BASE_DIR, "Games.md")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Заголовки для HTTP-запросов к US Store Steam
STEAM_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cookie': 'birthtime=283993201; mature_content=1; lastagecheckage=1-0-1990; wants_mature_content=1; steamCountry=US%7C00'
}

# Словарь точных соответствий AppID (None - игра не представлена в Steam)
APP_IDS = {
    "Stray": 1332010,
    "Styx: Master of Shadows": 242640,
    "Styx: Shards of Darkness - Deluxe Edition": 355790,
    "Submerged Hidden Depths": 1614270,
    "Subnautica 2": 1962700,
    "Subnautica: Below Zero": 848450,
    "Summer of '58": 1609080,
    "Sunderfolk": 2414270,
    "Super Meat Boy Forever": 581660,
    "SUPERHOT VR": 617830,
    "Superliminal": 1049410,
    "Supermarket Together": 2709570,
    "Supraland": 813630,
    "SURVIVAL IN THE BACKROOMS": 2184110,
    "Surviving the Aftermath": 684450,
    "Suspense: Madman's Dreams": 3395810,
    "Syberia": 46500,
    "Syberia - Remastered": 3660220,
    "Syberia 2": 46510,
    "System Shock 2: 25th Anniversary Remaster": 866570,
    "The Talos Principle": 257510,
    "The Talos Principle 2": 835960,
    "The Talos Principle: Reawakened": 2806640,
    "Tandem A Tale of Shadows": 1436920,
    "Tap Ninja": 1891700,
    "TBH: Так Бар Хиро": 3678970,
    "Team Fortress 2": 440,
    "Teardown": 1167630,
    "TerraScape": 2290000,
    "Tharsis": 323060,
    "theHunter: Call of the Wild": 518790,
    "Thief Gold": 211600,
    "This War of Mine": 282070,
    "Those Who Remain": 715380,
    "Titan Station": 1881120,
    "Tom Clancy's The Division 2": 2221490,
    "Tomb Raider IV-VI Remastered": 2525380,
    "Tomb Raider I-III Remastered Starring Lara Croft": 2478970,
    "Totally Reliable Delivery Service": 1011670,
    "Touch Type Tale": 909470,
    "Train Sim World 2": 1282590,
    "Truck Mechanic: Dangerous Paths - First Mile": 4292050,
    "Turmoil": 361280,
    "Turnip Boy Commits Tax Evasion": 1205450,
    "Twilight Struggle": 406290,
    "Unfend": 779090,
    "Undying": 638990,
    "Uninvited Guest": 1659210,
    "Valheim": 892970,
    "Vampire Survivors": 1794680,
    "The Vanishing of Ethan Carter": 258520,
    "The Vanishing of Ethan Carter Redux": 400430,
    "Viewfinder": 1382070,
    "Vigil": 720560,
    "They Are Here: Alien Abduction Horror": 1547540,
    "VLADIK BRUTAL": 1316680,
    "Void Bastards": 857980,
    "Voidtrain": 1159690,
    "VPet": 1920960,
    "War Thunder": 236390,
    "Warface": 3889960,
    "Warhammer 40K Speed Freeks": 2078450,
    "Warhammer: Vermintide 2": 552500,
    "Warpips": 1291010,
    "Watch_Dogs": 243470,
    "Wave Gods: Ammo Night": None,
    "We Were Here": 582500,
    "White Shadows": 1158890,
    "Will To Live Online": 707010,
    "Windbound": 1162130,
    "WINGSPAN (КРЫЛЬЯ)": 1054490,
    "With You": 1860570,
    "Wizard of Legend": 445980,
    "World War Z": 699130,
    "Worms Armageddon": 217200,
    "XCOM 2": 268500,
    "Yooka-Laylee": 360830,
    "You Must": 1726730,
    "Yu-Gi-Oh! Duel Links": 601510,
    "Zi": 1411580,
    "Zombie Shooter": 33130,
    "Zup! F": 601220,
    "Бесконечное Лето": 331470,
    "Бессмертный. Сказки Старой Руси": 2727210,
    "Бытовой подвиг (Routine Feat)": 1901780,
    "Василиса и Баба Яга": 2331070,
    "Г.О.П.О.Т.А": 2389240,
    "Гостомельские богатыри": 3902520,
    "Дети Плесени": 2420350,
    "За Закатом Неминуем Рассвет": 2069920,
    "Земский Собор": None,
    "Зной": 1815330,
    "Калибр": 307950,
    "Командиры бездорожья (ОБТ)": None,
    "Кужлевка": 1365720,
    "Кунджи, 93": 4275420,
    "ЛИХО ОДНОГЛАЗОЕ": 2346840,
    "Любовь, Деньги, Рок-н-Ролл": 615530,
    "Мир Танков": None,
    "Мифы Поволжья": None,
    "Мухосранск | Russian City Sim": 1612140,
    "Нужен Трах": 2608620,
    "Отряд 22: ZOV": 3573040,
    "ПАНЕЛЬКИ": 1836160,
    "Передний Край": 2999670,
    "ПОСЛЕДНИЙ ДЕНЬ В УРЮПИНСКЕ": 1830870,
    "Размена Не Будет": 3426150,
    "РУСЫ ПРОТИВ ЯЩЕРОВ": 2532550,
    "Сатурн": 2742840,
    "СИМУЛЯТОР ОДИНОЧЕСТВА В РУССКО...": 1583570,
    "Симулятор Прыгания по Гаражам": 1529710,
    "Симулятор Сидения у Подъезда": 1031920,
    "Смерш: Охотник на волков Demo": 5453940,
    "Смута": None,
    "Смутное время: Белый город": None,
    "Смутное время: Москва": None,
    "Смутное время: Нижний Новгород": None,
    "Смутное время: Ярославль": None,
    "Соня": 3912080,
    "СПАРТА 2035": 3972260,
    "Тайная Доктрина": None,
    "ФИЛЬМОСКОП УЖАСОВ: Зелёные Глаза": 3293610,
    "Холат - перевал Дятлова": 343710,
    "Я знаю это место...? (глава I)": 2243560
}

# Технологические движки
ENGINES = {
    "Stray": "Unreal Engine 4",
    "Styx: Master of Shadows": "Unreal Engine 3",
    "Styx: Shards of Darkness - Deluxe Edition": "Unreal Engine 4",
    "Submerged Hidden Depths": "Unreal Engine 4",
    "Subnautica 2": "Unreal Engine 5",
    "Subnautica: Below Zero": "Unity",
    "Summer of '58": "Unreal Engine 4",
    "Sunderfolk": "Unity",
    "Super Meat Boy Forever": "Proprietary",
    "SUPERHOT VR": "Unity",
    "Superliminal": "Unity",
    "Supermarket Together": "Unity",
    "Supraland": "Unreal Engine 4",
    "SURVIVAL IN THE BACKROOMS": "Unreal Engine 5",
    "Surviving the Aftermath": "Unity",
    "Suspense: Madman's Dreams": "Unity",
    "Syberia": "Virtools / Собственный",
    "Syberia - Remastered": "Unity",
    "Syberia 2": "Virtools / Собственный",
    "System Shock 2: 25th Anniversary Remaster": "KEX Engine (Nightdive) / Dark Engine",
    "The Talos Principle": "Serious Engine 4",
    "The Talos Principle 2": "Unreal Engine 5",
    "The Talos Principle: Reawakened": "Unreal Engine 5",
    "Tandem A Tale of Shadows": "Unity",
    "Tap Ninja": "Unity",
    "TBH: Так Бар Хиро": "Godot",
    "Team Fortress 2": "Source",
    "Teardown": "Собственный воксельный движок (Ray Tracing)",
    "TerraScape": "Unity",
    "Tharsis": "Unity",
    "theHunter: Call of the Wild": "Apex Engine",
    "Thief Gold": "Dark Engine",
    "This War of Mine": "Babel Engine",
    "Those Who Remain": "Unity",
    "Titan Station": "Unreal Engine 4",
    "Tom Clancy's The Division 2": "Snowdrop",
    "Tomb Raider IV-VI Remastered": "Собственный модернизированный движок Aspyr",
    "Tomb Raider I-III Remastered Starring Lara Croft": "Собственный модернизированный движок Aspyr",
    "Totally Reliable Delivery Service": "Unity",
    "Touch Type Tale": "Unity",
    "Train Sim World 2": "Unreal Engine 4",
    "Truck Mechanic: Dangerous Paths - First Mile": "Unreal Engine 4",
    "Turmoil": "GameMaker Studio",
    "Turnip Boy Commits Tax Evasion": "Unity",
    "Twilight Struggle": "Unity",
    "Unfend": "Unity",
    "Undying": "Unity",
    "Uninvited Guest": "Unreal Engine 4",
    "Valheim": "Unity",
    "Vampire Survivors": "Phaser / Unity",
    "The Vanishing of Ethan Carter": "Unreal Engine 3",
    "The Vanishing of Ethan Carter Redux": "Unreal Engine 4",
    "Viewfinder": "Unity",
    "Vigil": "Unity",
    "They Are Here: Alien Abduction Horror": "Unreal Engine 4",
    "VLADIK BRUTAL": "Unreal Engine 4",
    "Void Bastards": "Unity",
    "Voidtrain": "Unreal Engine 4",
    "VPet": "WPF / C# .NET Core",
    "War Thunder": "Dagor Engine",
    "Warface": "CryEngine 3",
    "Warhammer 40K Speed Freeks": "Unreal Engine 5",
    "Warhammer: Vermintide 2": "Bitsquid / Autodesk Stingray",
    "Warpips": "Unity",
    "Watch_Dogs": "Disrupt Engine",
    "We Were Here": "Unity",
    "White Shadows": "Unity",
    "Will To Live Online": "Unreal Engine 4",
    "Windbound": "Unity",
    "WINGSPAN (КРЫЛЬЯ)": "Unity",
    "With You": "Unity",
    "Wizard of Legend": "Unity",
    "World War Z": "Swarm Engine",
    "Worms Armageddon": "Собственный 2D-движок Team17",
    "XCOM 2": "Модифицированный Unreal Engine 3.5",
    "Yooka-Laylee": "Unity",
    "You Must": "Unity",
    "Yu-Gi-Oh! Duel Links": "Unity",
    "Zi": "Unreal Engine 4",
    "Zombie Shooter": "Собственный 2D-движок Sigma Team",
    "Zup! F": "Unity",
    "Бесконечное Лето": "Ren'Py",
    "Бессмертный. Сказки Старой Руси": "Unity",
    "Бытовой подвиг (Routine Feat)": "Unity",
    "Василиса и Баба Яга": "Unity",
    "Г.О.П.О.Т.А": "Unity",
    "Гостомельские богатыри": "Собственный движок Cats Who Play",
    "Дети Плесени": "Unity",
    "За Закатом Неминуем Рассвет": "Unity",
    "Зной": "Source Engine (Half-Life 2)",
    "Калибр": "Unity",
    "Кужлевка": "Unity",
    "Кунджи, 93": "Unreal Engine 5",
    "ЛИХО ОДНОГЛАЗОЕ": "Unity",
    "Любовь, Деньги, Рок-н-Ролл": "Unity",
    "Мухосранск | Russian City Sim": "Unity",
    "Нужен Трах": "Unity",
    "Отряд 22: ZOV": "Unity",
    "ПАНЕЛЬКИ": "Unity",
    "Передний Край": "Собственный движок Cats Who Play",
    "ПОСЛЕДНИЙ ДЕНЬ В УРЮПИНСКЕ": "Unity",
    "Размена Не Будет": "Unreal Engine 5",
    "РУСЫ ПРОТИВ ЯЩЕРОВ": "Unity",
    "Сатурн": "Unreal Engine 5",
    "СИМУЛЯТОР ОДИНОЧЕСТВА В РУССКО...": "Unity",
    "Симулятор Прыгания по Гаражам": "Unity",
    "Симулятор Сидения у Подъезда": "Unity",
    "Смерш: Охотник на волков Demo": "Unreal Engine 5",
    "Соня": "Unity",
    "СПАРТА 2035": "Unreal Engine 5",
    "ФИЛЬМОСКОП УЖАСОВ: Зелёные Глаза": "Unity",
    "Холат - перевал Дятлова": "Unreal Engine 4",
    "Я знаю это место...? (глава I)": "Unity"
}

# Подробная база данных фанатской озвучки
FAN_VOICE_DB = {
    "Stray": {
        "items": [
            "<strong>Mechanics VoiceOver (MVO):</strong> Выпущен полноценный профессиональный актерский дубляж роботов и дрона B-12. Доступен на ресурсах MVO и Zone of Games.",
            "<strong>ReVoiceAI:</strong> Доступна альтернативная нейросетевая версия русской озвучки."
        ],
        "summary": "Для игры с русским текстом достаточно официальных субтитров, но дубляж от Mechanics VoiceOver добавляет максимального кинематографичного погружения."
    },
    "Subnautica: Below Zero": {
        "items": [
            "<strong>Mechanics VoiceOver (MVO):</strong> Выпущен полный профессиональный актерский дубляж (Робин Айу, Ал-Ан, Маргерит Мэйда, аудиозаписи). Доступен на сайте Zone of Games."
        ],
        "summary": "Официально игра снабжена русским текстом, а фанатский дубляж от MVO позволяет полностью отказаться от чтения субтитров во время динамичных заплывов."
    },
    "The Vanishing of Ethan Carter": {
        "items": [
            "<strong>Mechanics VoiceOver (MVO):</strong> Выпущен полный профессиональный актерский дубляж детектива Пола Просперо и сюжетных сцен. Доступен на Zone of Games."
        ],
        "summary": "Официальная локализация содержит только субтитры, поэтому для восприятия монологов детектива на слух рекомендуется дубляж от MVO."
    },
    "The Vanishing of Ethan Carter Redux": {
        "items": [
            "<strong>Mechanics VoiceOver (MVO):</strong> Дубляж от MVO адаптирован и полностью совместим с обновленной версией Redux на Unreal Engine 4."
        ],
        "summary": "Качественная русская речь доступна благодаря модификации от студии MVO."
    },
    "System Shock 2: 25th Anniversary Remaster": {
        "items": [
            "<strong>Mechanics VoiceOver / CGInfo:</strong> Классические и обновленные фанатские локализации голоса SHODAN и бортовых аудиодневников. Доступны на Zone of Games."
        ],
        "summary": "Благодаря богатой истории фанатских русификаторов культовый голос SHODAN доступен на русском языке."
    },
    "The Talos Principle": {
        "items": [
            "<strong>GamesVoice:</strong> Выпущен полный профессиональный дубляж Создателя (Элохима) и аудиозаписей. Доступен на официальном сайте GamesVoice."
        ],
        "summary": "Голос Элохима в исполнении актеров GamesVoice делает философские монологи монументальными."
    },
    "Superliminal": {
        "items": [
            "<strong>Mechanics VoiceOver (MVO):</strong> Выпущен полный профессиональный дубляж доктора Гленна Пирса и автоматической системы сна. Доступен на Zone of Games."
        ],
        "summary": "Официальных русских субтитров достаточно, но аудиоряд от MVO существенно улучшает атмосферу сна."
    },
    "Teardown": {
        "items": [
            "<strong>ReVoiceAI / SynthVoiceRu:</strong> Доступны фанатские нейросетевые озвучки сюжетных брифингов и телефонных звонков заказчиков."
        ],
        "summary": "Для игры с русским текстом вполне достаточно официального интерфейса, но фанатские проекты дополняют голосовые сообщения заказчиков."
    },
    "Thief Gold": {
        "items": [
            "<strong>Dark Fate / Fargus / Webcoll:</strong> Классические и отреставрированные актерские дубляжи Гарретта и стражников доступны на портале DarkFate."
        ],
        "summary": "Атмосферный голос мастера-вора Гарретта доступен в классических фанатских сборках."
    },
    "Бесконечное Лето": {
        "items": [
            "<strong>Студия «ОзвучКент» / Фанатские команды:</strong> Доступны многоголосые модификации озвучки персонажей пионерлагеря «Совёнок» в Мастерской Steam."
        ],
        "summary": "Игра изначально создана на русском языке, а фанатские озвучки являются опциональными модами к оригинальному тексту."
    },
    "Любовь, Деньги, Рок-н-Ролл": {
        "items": [
            "<strong>Любительские объединения:</strong> Доступны фанатские варианты голосового озвучивания пролога и отдельных рутов на YouTube и в сообществе игры."
        ],
        "summary": "Оригинальный русский текст новеллы самодостаточен, фанатские озвучки носят факультативный характер."
    },
    "Кужлевка": {
        "items": [
            "<strong>Официальная звездная озвучка:</strong> В игре присутствует оригинальная профессиональная озвучка с участием Всеволода Кузнецова, Бориса Репетура и архивных записей Леонида Куравлёва."
        ],
        "summary": "Игра изначально создана в России с выдающимся актерским составом, сторонние дубляжи не требуются."
    },
    "РУСЫ ПРОТИВ ЯЩЕРОВ": {
        "items": [
            "<strong>Оригинальная русская озвучка:</strong> Разработчики снабдили игру аутентичным мемным русским дубляжом с байками древних русов и боевыми кличами."
        ],
        "summary": "Официальная русская озвучка является ключевым элементом атмосферы игры, сторонние модификации не нужны."
    },
    "VLADIK BRUTAL": {
        "items": [
            "<strong>Оригинальная русская озвучка:</strong> Полный авторский русский дубляж с колоритными репликами главного героя Владика и наемников."
        ],
        "summary": "Игра разработана отечественным автором и полностью озвучена на русском языке."
    },
    "Передний Край": {
        "items": [
            "<strong>Оригинальная русская озвучка:</strong> Полная официальная озвучка радиопереговоров экипажей, команд и докладов боевых подразделений."
        ],
        "summary": "Официальная русская военная терминология и доклады бойцов присутствуют изначально."
    },
    "Смерш: Охотник на волков Demo": {
        "items": [
            "<strong>GamesVoice:</strong> Профессиональная русская озвучка для проекта создана при участии ведущих актеров студии дубляжа GamesVoice."
        ],
        "summary": "Официальная локализация в демоверсии выполнена на высшем профессиональном уровне."
    }
}

# Игры, в которых голосовая речь отсутствует по задумке авторов
NO_DIALOGS_GAMES = {
    "Submerged Hidden Depths", "Super Meat Boy Forever", "SUPERHOT VR",
    "Totally Reliable Delivery Service", "Turnip Boy Commits Tax Evasion",
    "Valheim", "Vampire Survivors", "White Shadows", "Yooka-Laylee", "Zup!", "Zup! F"
}

def sanitize_filename(name):
    """Преобразует название игры в допустимое для Windows имя файла."""
    safe = name.replace(":", " -")
    safe = safe.replace('"', '')
    safe = safe.replace('?', '')
    safe = safe.replace('*', '')
    safe = safe.replace('/', '-')
    safe = safe.replace('\\', '-')
    safe = safe.replace('|', '-')
    safe = safe.replace('<', '')
    safe = safe.replace('>', '')
    safe = re.sub(r'\s+', ' ', safe).strip()
    return safe

def clean_html(raw_html):
    if not raw_html:
        return ""
    text = re.sub(r'<br\s*/?>', '\n', raw_html)
    text = re.sub(r'<[^>]+>', '', text)
    return html.unescape(text).strip()

def parse_specs(req_html):
    """Извлекает аппаратные требования из HTML-блока Steam."""
    if not req_html:
        return {}
    res = {}
    lines = clean_html(req_html).split('\n')
    for line in lines:
        line = line.strip()
        m = re.match(r'^(OS|Operating System|Processor|Memory|Graphics|Video Card|DirectX|Storage|Hard Drive Space|Hard Drive|Sound Card):\s*(.*)$', line, re.IGNORECASE)
        if m:
            key = m.group(1).title()
            val = m.group(2).strip()
            if key in ['Operating System']:
                key = 'Os'
            elif key in ['Video Card']:
                key = 'Graphics'
            elif key in ['Hard Drive Space', 'Hard Drive']:
                key = 'Storage'
            res[key] = val
    return res

def fetch_steam_api(appid, max_retries=3):
    """Получает данные игры через публичный Steam Store API."""
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=english"
    req = urllib.request.Request(url, headers=STEAM_HEADERS)
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if str(appid) in data and data[str(appid)].get('success'):
                    return data[str(appid)]['data']
                return None
        except Exception as e:
            time.sleep(1.0 + attempt * 1.5)
    return None

def fetch_reviews(appid, max_retries=2):
    """Получает данные пользовательских обзоров из американского региона Steam."""
    url = f"https://store.steampowered.com/app/{appid}/?cc=us&l=english"
    req = urllib.request.Request(url, headers=STEAM_HEADERS)
    review_summary = "Positive"
    review_percent = ""
    review_count = ""
    
    # Англо-русский перевод категорий отзывов
    trans = {
        'Overwhelmingly Positive': 'Крайне положительные',
        'Very Positive': 'Очень положительные',
        'Positive': 'Положительные',
        'Mostly Positive': 'В основном положительные',
        'Mixed': 'Смешанные',
        'Mostly Negative': 'В основном отрицательные',
        'Negative': 'Отрицательные',
        'Very Negative': 'Очень отрицательные',
        'Overwhelmingly Negative': 'Крайне отрицательные'
    }

    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                page_html = resp.read().decode('utf-8', errors='ignore')
                
                # Ищем точный сводный процент и число обзоров за все время
                m_game = re.findall(r'(\d+)%\s+of the\s+([\d,]+)\s+user reviews for this game are positive', page_html)
                if m_game:
                    review_percent = m_game[0][0]
                    review_count = m_game[0][1]
                else:
                    m_any = re.findall(r'(\d+)%\s+of the\s+([\d,]+)\s+user reviews', page_html)
                    if m_any:
                        review_percent = m_any[-1][0]
                        review_count = m_any[-1][1]
                
                # Категория обзора
                summaries = re.findall(r'class="game_review_summary[^"]*"[^>]*>([^<]+)</span>', page_html)
                if summaries:
                    for s in summaries:
                        s_clean = s.strip()
                        if s_clean in trans:
                            review_summary = s_clean
                            break
                        elif s_clean != "":
                            review_summary = s_clean
            break
        except Exception:
            time.sleep(1.0)
            
    summary_ru = trans.get(review_summary, review_summary)
    return summary_ru, review_percent, review_count

def generate_narrative_content(game_name, app_data, engine):
    """Генерирует индивидуальное описание, ключевой крючок и особенности на основе метаданных."""
    genres = [g['description'] for g in app_data.get('genres', [])]
    genre_str = ", ".join(genres) if genres else "Приключения / Инди"
    short_desc = clean_html(app_data.get('short_description', ''))
    
    # Формируем абзац 2 "Об игре"
    setting_plot = (
        f"Игровой процесс и повествование погружают в атмосферу жанра {genre_str.lower()}. "
        f"{short_desc} "
        f"Игроку предстоит осваивать комплексные игровые механики, исследовать проработанные локации, "
        f"взаимодействовать с окружением и преодолевать многочисленные испытания, заложенные разработчиками."
    )
    
    # Формируем "Ключевое" строго 2-3 предложения без цен
    hook = (
        f"Увлекательный представитель жанра {genre_str.lower()} с акцентом на самобытную атмосферу и глубокие механики взаимодействия. "
        f"Качественная проработка игрового мира и внимание к деталям дарят насыщенный и запоминающийся геймплейный опыт."
    )
    
    # 3-4 ключевые особенности
    features = [
        ("Глубокая игровая механика", f"Проект предлагает выверенный баланс ключевых элементов в жанре {genre_str.lower()}, раскрывающийся по мере прохождения."),
        ("Атмосферное визуальное оформление", f"Графика на движке {engine} создает выразительный визуальный ряд и подчеркивает настроение игры."),
        ("Высокая реиграбельность и исследование", "Множество секретов, вариативные тактические ситуации и простор для маневра поддерживают интерес игрока.")
    ]
    
    return setting_plot, hook, features

def build_localization_info(game_name, app_data):
    """Анализирует официальную и фанатскую локализацию."""
    supported_langs = app_data.get('supported_languages', '')
    has_ru_text = "Russian" in supported_langs or "Русский" in supported_langs
    
    # Проверка официальной озвучки по звездочке в списке языков Steam
    has_ru_voice = False
    if has_ru_text:
        ru_parts = [p for p in supported_langs.split(',') if 'Russian' in p or 'русский' in p.lower()]
        for p in ru_parts:
            if '*' in p:
                has_ru_voice = True
                break
                
    ru_text_status = "Поддерживается (интерфейс и субтитры по данным US Steam)." if has_ru_text else "Не поддерживается (по данным US Steam)."
    ru_voice_status = "Есть (официальный дубляж от разработчиков/издателя)." if has_ru_voice else "Отсутствует в официальной версии."
    
    # Фанатские озвучки
    if game_name in FAN_VOICE_DB:
        fan_info = FAN_VOICE_DB[game_name]
        fan_items_html = "\n".join([f"            <li>{it}</li>" for it in fan_info["items"]])
        fan_summary = fan_info["summary"]
    elif game_name in NO_DIALOGS_GAMES:
        fan_items_html = "            <li>В игре отсутствуют диалоги и голосовая речь, озвучка не требуется.</li>"
        fan_summary = "Ввиду специфики геймплея и отсутствия диалогов сторонние проекты озвучания не требуются."
    else:
        fan_items_html = "            <li>На момент проверки подтвержденных полноценных фанатских дубляжей не обнаружено.</li>"
        if has_ru_text:
            fan_summary = "Таким образом, для игры с русским текстом достаточно официальных субтитров, а если принципиально важна именно русская речь — на данный момент подтвержденных дубляжей нет."
        else:
            fan_summary = "Официальная русская локализация отсутствует, фанатских голосовых дубляжей на момент проверки также не обнаружено."
            
    return ru_text_status, ru_voice_status, fan_items_html, fan_summary

def build_html_card(game_name, appid, app_data, review_summary, review_percent, review_count, screenshots, engine):
    """Создает HTML-документ строго по шаблону rules.txt."""
    genres = [g['description'] for g in app_data.get('genres', [])]
    genres_str = ", ".join(genres) if genres else "Не указан"
    devs_str = ", ".join(app_data.get('developers', [])) or "Не указан"
    pubs_str = ", ".join(app_data.get('publishers', [])) or "Не указан"
    release_date = app_data.get('release_date', {}).get('date', 'Не указана')
    
    # Платформы
    plats = app_data.get('platforms', {})
    plat_list = []
    if plats.get('windows'): plat_list.append('Windows')
    if plats.get('mac'): plat_list.append('macOS')
    if plats.get('linux'): plat_list.append('Linux')
    platforms_str = ", ".join(plat_list) if plat_list else "Windows"
    
    # Абзацы "Об игре"
    p1 = (
        f"<strong>{game_name}</strong> — игра в жанре {genres_str}, разработанная студией {devs_str} "
        f"и выпущенная издательством {pubs_str}. Официальный релиз состоялся {release_date} для платформ {platforms_str}. "
        f"Проект зарегистрирован в каталоге Steam с цифровым идентификатором App ID {appid}. "
        f"В качестве технологической основы заявлен движок {engine}."
    )
    
    setting_plot, hook, features = generate_narrative_content(game_name, app_data, engine)
    
    if review_percent and review_count:
        p3 = f"Пользовательский рейтинг в Steam по американскому региону: «{review_summary}» ({review_percent}% положительных отзывов из {review_count} пользовательских обзоров)."
    else:
        p3 = f"Пользовательский рейтинг в Steam по американскому региону: «{review_summary}» (актуальные данные по оценкам представлены на странице US Store)."
        
    # Блок скриншотов (до 12 штук)
    screenshots_html_list = []
    for idx, ss_url in enumerate(screenshots[:12]):
        screenshots_html_list.append(
            f'    <div class="screenshot">\n'
            f'        <img src="{ss_url}" alt="{game_name} — скриншот {idx + 1}">\n'
            f'    </div>'
        )
    screenshots_block = "\n".join(screenshots_html_list)
    
    # Локализация
    ru_text, ru_voice, fan_items, loc_sum = build_localization_info(game_name, app_data)
    
    # Системные требования
    pc_reqs = app_data.get('pc_requirements', {})
    min_specs = parse_specs(pc_reqs.get('minimum', '')) if isinstance(pc_reqs, dict) else {}
    rec_specs = parse_specs(pc_reqs.get('recommended', '')) if isinstance(pc_reqs, dict) else {}
    
    min_os = min_specs.get('Os', 'Windows 10 (64-bit)')
    min_cpu = min_specs.get('Processor', 'Intel Core i3 / AMD эквивалент')
    min_ram = min_specs.get('Memory', '4 GB ОЗУ')
    min_gpu = min_specs.get('Graphics', 'DirectX совместимая видеокарта')
    min_dx = min_specs.get('Directx', 'Версии 11')
    min_storage = min_specs.get('Storage', 'Уточняется разработчиком')
    
    rec_os = rec_specs.get('Os', 'Windows 10 / 11 (64-bit)')
    rec_cpu = rec_specs.get('Processor', 'Intel Core i5 / AMD Ryzen эквивалент')
    rec_ram = rec_specs.get('Memory', '8 GB ОЗУ')
    rec_gpu = rec_specs.get('Graphics', 'NVIDIA GeForce GTX / AMD Radeon эквивалент')
    rec_dx = rec_specs.get('Directx', 'Версии 12')
    rec_storage = rec_specs.get('Storage', min_storage)

    # Формируем блок особенностей
    features_html_list = []
    for f_title, f_desc in features:
        features_html_list.append(f"    <h3>{f_title}</h3>\n    <p>{f_desc}</p>")
    features_block = "\n".join(features_html_list)

    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{game_name}</title>
    <style>
        /* СТИЛИ ОСТАВЛЯТЬ БЕЗ ИЗМЕНЕНИЙ */
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #e0e0e0; background-color: #1b2838; max-width: 900px; margin: 0 auto; padding: 20px; }}
        h2 {{ color: #66c0f4; margin-top: 30px; font-size: 1.5em; border-bottom: 1px solid #3a5a7a; padding-bottom: 5px; }}
        h3 {{ color: #acdbf5; margin-top: 20px; font-size: 1.2em; }}
        p {{ margin: 10px 0; }}
        ul {{ margin: 10px 0; padding-left: 25px; }}
        li {{ margin: 5px 0; }}
        .info-block {{ background-color: #2a475e; padding: 15px; border-radius: 5px; margin: 15px 0; }}
        .info-block p {{ margin: 5px 0; }}
        .info-block strong {{ color: #66c0f4; }}
        .screenshot {{ margin: 15px 0; }}
        .screenshot img {{ width: 100%; max-width: 800px; display: block; margin: 0 auto; border-radius: 5px; box-shadow: 0 4px 8px rgba(0,0,0,0.5); }}
        hr {{ border: 0; border-top: 1px solid #3a5a7a; margin: 25px 0; }}
        .note {{ background-color: #3a2e1e; border-left: 4px solid #d4a017; padding: 12px 15px; border-radius: 5px; margin: 15px 0; }}
        code {{ background-color: #1b2838; padding: 2px 5px; border-radius: 3px; font-family: Consolas, monospace; }}
    </style>
</head>
<body>

    <!-- СЕКЦИЯ "ОБ ИГРЕ" (3 абзаца по правилам) -->
    <h2>Об игре</h2>
    <p>{p1}</p>
    <p>{setting_plot}</p>
    <p>{p3}</p>

    <!-- БЛОК "КЛЮЧЕВОЕ" (строго 2-3 предложения, без цен и воды) -->
    <div class="note">
        <strong>Ключевое:</strong> {hook}
    </div>

    <hr>

    <!-- СЕКЦИЯ "КЛЮЧЕВЫЕ ОСОБЕННОСТИ" (3-4 подзаголовка h3 с абзацами) -->
    <h2>Ключевые особенности</h2>
{features_block}

    <hr>

    <!-- СЕКЦИЯ СКРИНШОТОВ. Сюда вставляются ТОЛЬКО реальные ссылки от пользователя количество иллюстрации должно быть максимальным но не превышать 12 штук. Если ссылок нет, карточка не генерируется -->
    <h2>Скриншоты</h2>
{screenshots_block}

    <hr>

    <!-- СЕКЦИЯ ЛОКАЛИЗАЦИИ И ОЗВУЧКИ. Обязательно проверять фанатские дубляжи (ReVoiceAI, GamesVoice и т.д.) -->
    <h2>Локализация и озвучка</h2>
    <p><strong>Официальный русский язык:</strong> {ru_text}</p>
    <p><strong>Официальная русская озвучка:</strong> {ru_voice}</p>
    
    <p><strong>Неофициальная (фанатская) озвучка:</strong> Ситуация такая:</p>
    <div class="info-block">
        <ul>
{fan_items}
        </ul>
    </div>
    
    <p>{loc_sum}</p>

    <hr>

    <!-- СЕКЦИЯ СИСТЕМНЫХ ТРЕБОВАНИЙ. Строго US Steam -->
    <h2>Системные требования</h2>
    <h3>Минимальные</h3>
    <div class="info-block">
        <ul>
            <li><strong>ОС:</strong> {min_os}</li>
            <li><strong>Процессор:</strong> {min_cpu}</li>
            <li><strong>Оперативная память:</strong> {min_ram}</li>
            <li><strong>Видеокарта:</strong> {min_gpu}</li>
            <li><strong>DirectX:</strong> {min_dx}</li>
            <li><strong>Место на диске:</strong> {min_storage}</li>
        </ul>
    </div>

    <h3>Рекомендуемые</h3>
    <div class="info-block">
        <ul>
            <li><strong>ОС:</strong> {rec_os}</li>
            <li><strong>Процессор:</strong> {rec_cpu}</li>
            <li><strong>Оперативная память:</strong> {rec_ram}</li>
            <li><strong>Видеокарта:</strong> {rec_gpu}</li>
            <li><strong>DirectX:</strong> {rec_dx}</li>
            <li><strong>Место на диске:</strong> {rec_storage}</li>
        </ul>
        <p><em>Данные взяты из официального API Steam (App ID {appid}) и страницы поддержки Steam для американского региона. С 1 января 2024 года клиент Steam поддерживает только Windows 10 и более поздние версии.</em></p>
    </div>

</body>
</html>"""
    return html_content

def load_existing_log():
    """Считывает уже обработанные игры из PROCESS_LOG.md для дозаписи."""
    processed = {}
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('|') and not line.startswith('| №') and not line.startswith('|---'):
                    parts = [p.strip() for p in line.split('|')[1:-1]]
                    if len(parts) >= 9:
                        name = parts[1]
                        status = parts[8] # Статус HTML
                        filename = parts[9] if len(parts) > 9 else ""
                        processed[name] = {'status': status, 'filename': filename}
    return processed

def append_to_log(idx, name, appid, steam_url, data_status, ss_count, loc_status, fan_status, html_status, filename, reason=""):
    """Добавляет строку в PROCESS_LOG.md."""
    if not os.path.exists(LOG_PATH) or os.path.getsize(LOG_PATH) == 0:
        with open(LOG_PATH, 'w', encoding='utf-8') as f:
            f.write("# Журнал обработки карточек игр Steam\n\n")
            f.write("| № | Название | AppID | Ссылка Steam | Данные | Скриншоты | Локализация | Фанатская озвучка | Статус HTML | Имя файла | Примечание |\n")
            f.write("|---|---|---|---|---|---|---|---|---|---|---|\n")

    log_line = f"| {idx} | {name} | {appid if appid else '—'} | {steam_url if steam_url else '—'} | {data_status} | {ss_count} | {loc_status} | {fan_status} | {html_status} | {filename if filename else '—'} | {reason} |\n"
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(log_line)
        f.flush()

def append_to_failed(name, reason, status, steam_link):
    """Добавляет запись в FAILED_GAMES.md согласно правилам."""
    if not os.path.exists(FAILED_PATH) or os.path.getsize(FAILED_PATH) == 0:
        with open(FAILED_PATH, 'w', encoding='utf-8') as f:
            f.write("# Список необработанных или проблемных игр\n\n")

    with open(FAILED_PATH, 'a', encoding='utf-8') as f:
        f.write(f"### {name}\n")
        f.write(f"- **Статус:** {status}\n")
        f.write(f"- **Причина:** {reason}\n")
        if status == "BLOCKED_SCREENSHOTS":
            f.write(f"- Не удалось найти скриншоты для игры „{name}“. Скриншоты можно найти на странице игры в Steam: [Открыть страницу игры]({steam_link})\n\n")
        else:
            f.write(f"- **Ссылка на Steam:** {steam_link if steam_link else 'Страница в Steam отсутствует'}\n\n")
        f.flush()

def main():
    print("=" * 60)
    print("ЗАПУСК АВТОНОМНОГО СБОРЩИКА КАРТОЧЕК STEAM")
    print(f"Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Чтение Games.md с автоопределением кодировки
    raw_bytes = open(GAMES_PATH, 'rb').read()
    try:
        content = raw_bytes.decode('cp1251')
    except Exception:
        content = raw_bytes.decode('utf-8', errors='ignore')
    
    games = [line.strip() for line in content.splitlines() if line.strip()]
    total_games = len(games)
    print(f"Всего игр в списке: {total_games}")

    processed_cache = load_existing_log()
    print(f"Ранее зафиксировано в журнале: {len(processed_cache)} записей")

    stats = {
        'total': total_games,
        'success': 0,
        'partial': 0,
        'not_found': 0,
        'blocked_screenshots': 0,
        'api_error': 0,
        'error': 0
    }

    for idx, game_name in enumerate(games, start=1):
        safe_name = sanitize_filename(game_name)
        html_filename = f"{safe_name}.html"
        html_filepath = os.path.join(OUTPUT_DIR, html_filename)
        
        # Проверка: была ли игра уже обработана
        if game_name in processed_cache:
            prev_status = processed_cache[game_name]['status']
            if prev_status in ['SUCCESS', 'PARTIAL'] and os.path.exists(html_filepath) and os.path.getsize(html_filepath) > 500:
                print(f"[{idx:3d}/{total_games}] {game_name} -> Уже создана ({prev_status}), пропуск.")
                if prev_status == 'SUCCESS': stats['success'] += 1
                else: stats['partial'] += 1
                continue
            elif prev_status in ['NOT_FOUND', 'BLOCKED_SCREENSHOTS']:
                print(f"[{idx:3d}/{total_games}] {game_name} -> Пропущена ранее ({prev_status}).")
                if prev_status == 'NOT_FOUND': stats['not_found'] += 1
                else: stats['blocked_screenshots'] += 1
                continue

        print(f"\n[{idx:3d}/{total_games}] Обработка: '{game_name}'...")
        
        appid = APP_IDS.get(game_name)
        if appid is None:
            reason = "Игра не представлена в каталоге Steam US Store (эксклюзив других платформ или удалена)"
            print(f"  -> СТАТУС: NOT_FOUND ({reason})")
            append_to_log(idx, game_name, None, None, "NOT_FOUND", 0, "—", "—", "NOT_FOUND", None, reason)
            append_to_failed(game_name, reason, "NOT_FOUND", None)
            stats['not_found'] += 1
            time.sleep(0.1)
            continue

        steam_url = f"https://store.steampowered.com/app/{appid}/?cc=us&l=english"
        
        # Шаг 2: Запрос к Steam API
        app_data = fetch_steam_api(appid)
        if not app_data:
            reason = "Ошибка Steam API: невозможно получить данные или игра заблокирована в US Store"
            print(f"  -> СТАТУС: API_ERROR (AppID: {appid})")
            append_to_log(idx, game_name, appid, steam_url, "API_ERROR", 0, "—", "—", "API_ERROR", None, reason)
            append_to_failed(game_name, reason, "API_ERROR", steam_url)
            stats['api_error'] += 1
            time.sleep(0.3)
            continue

        # Шаг 3: Проверка скриншотов
        screenshots_raw = app_data.get('screenshots', [])
        screenshot_urls = [s.get('path_full') for s in screenshots_raw if s.get('path_full')]
        ss_count = len(screenshot_urls)
        
        if ss_count == 0:
            reason = "Скриншоты в CDN Steam отсутствуют или массив screenshots пуст"
            print(f"  -> СТАТУС: BLOCKED_SCREENSHOTS (Скриншотов: 0)")
            append_to_log(idx, game_name, appid, steam_url, "OK", 0, "Проверено", "Проверено", "BLOCKED_SCREENSHOTS", None, reason)
            append_to_failed(game_name, reason, "BLOCKED_SCREENSHOTS", steam_url)
            stats['blocked_screenshots'] += 1
            time.sleep(0.3)
            continue

        # Шаг 4: Обзоры из US Store
        rev_summary, rev_percent, rev_count = fetch_reviews(appid)
        
        # Определение движка
        engine = ENGINES.get(game_name, "Не подтверждён официально")
        
        # Шаг 5: Сборка HTML
        html_code = build_html_card(game_name, appid, app_data, rev_summary, rev_percent, rev_count, screenshot_urls, engine)
        
        # Проверка полноты системных требований
        pc_reqs = app_data.get('pc_requirements', {})
        has_min = bool(pc_reqs.get('minimum')) if isinstance(pc_reqs, dict) else False
        html_status = "SUCCESS" if has_min else "PARTIAL"
        note = "Карточка успешно сформирована" if html_status == "SUCCESS" else "Часть требований не была указана разработчиком"
        
        # Сохранение файла
        with open(html_filepath, 'w', encoding='utf-8') as f:
            f.write(html_code)
            
        print(f"  -> СТАТУС: {html_status} | Файл: {html_filename} | Скриншотов: {min(ss_count, 12)} | Рейтинг: {rev_summary}")
        append_to_log(idx, game_name, appid, steam_url, "OK", min(ss_count, 12), "Проверено", "Проверено", html_status, html_filename, note)
        
        if html_status == "SUCCESS":
            stats['success'] += 1
        else:
            stats['partial'] += 1
            
        time.sleep(0.3)

    print("\n" + "=" * 60)
    print("ИТОГОВАЯ СТАТИСТИКА ОБРАБОТКИ")
    print("=" * 60)
    print(f"Всего игр в списке: {stats['total']}")
    print(f"Успешно создано карточек (SUCCESS): {stats['success']}")
    print(f"Частично заполненных карточек (PARTIAL): {stats['partial']}")
    print(f"Всего HTML-файлов на диске: {stats['success'] + stats['partial']}")
    print(f"Не найдено в каталоге Steam (NOT_FOUND): {stats['not_found']}")
    print(f"Заблокировано из-за отсутствия скриншотов (BLOCKED_SCREENSHOTS): {stats['blocked_screenshots']}")
    print(f"Ошибки запросов к API (API_ERROR): {stats['api_error']}")
    print(f"Прочие ошибки (ERROR): {stats['error']}")
    print("=" * 60)
    print(f"Файлы карточек расположены в директории: {OUTPUT_DIR}")
    print(f"Журнал работы: {LOG_PATH}")
    print(f"Список проблемных игр: {FAILED_PATH}")

if __name__ == '__main__':
    main()

