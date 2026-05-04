"""
Narxoz University Student Helper Bot
Supports: Russian, Kazakh, English
"""

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8733242894:AAHioxiQ7QguRdKAln6fvGjRrj9cstwMqRQ"
ADMIN_ID = 2018648930


# ─────────────────────────────────────────────────────────────────────────────
# TRANSLATIONS
# ─────────────────────────────────────────────────────────────────────────────

TEXTS = {
    "ru": {
        "welcome": (
            "👋 Добро пожаловать в <b>Narxoz Student Helper</b>!\n\n"
            "🎓 Я помогу тебе найти всю нужную информацию об Университете Нархоз.\n\n"
            "Выбери раздел:"
        ),
        "menu_iup": "📚 ИУП (Расписание предметов)",
        "menu_session": "📅 Расписание сессий",
        "menu_payment": "💳 Оплата",
        "menu_dorm": "🏠 Общежитие",
        "menu_contacts": "📞 Контакты",
        "menu_schools": "🏛️ Школы Нархоз",
        "menu_schedule": "📋 Прикрепить расписание",
        "menu_info": "ℹ️ О университете",
        "menu_lang": "🌐 Язык / Language / Тіл",
        "back": "⬅️ Назад",
        "choose_lang": "Выберите язык:",

        "info_title": "🎓 <b>Университет Нархоз</b>",
        "info_body": (
            "📍 <b>Адрес:</b> г. Алматы, ул. Жандосова, 55\n"
            "🪖 <b>Военная кафедра:</b> Алматы, мкр. 1, дом 81а\n\n"
            "🌐 <b>Сайты:</b>\n"
            "• <a href='https://canvas.narxoz.kz'>canvas.narxoz.kz</a> — учёба\n"
            "• <a href='https://platonus.narxoz.kz'>platonus.narxoz.kz</a> — личный кабинет\n"
            "• <a href='http://shd.narxoz.kz'>shd.narxoz.kz</a> — заявки (Help Desk)\n\n"
            "📣 <b>Миссия:</b> Подготовка лидеров, способных решать комплексные задачи реальной жизни.\n\n"
            "🏆 <b>Аккредитации:</b> FIBAA, IQAA, QS Stars ⭐⭐⭐⭐\n"
            "🌍 <b>Партнёр:</b> Illinois Institute of Technology (США)"
        ),

        "schools_title": "🏛️ <b>Школы Университета Нархоз</b>",
        "schools_body": (
            "В Нархозе 4 школы:\n\n"
            "1️⃣ <b>Школа цифровых технологий (SDT)</b>\n"
            "   • Digital Engineering\n"
            "   • Digital Management & Design\n"
            "   • Cybersecurity\n"
            "   • Statistics & Data Science\n"
            "   • Applied Mathematics in Digital Economy\n\n"
            "2️⃣ <b>Школа экономики и менеджмента</b>\n"
            "   • Финансы, Маркетинг, Менеджмент, BBA и др.\n\n"
            "3️⃣ <b>Гуманитарная школа</b>\n"
            "   • Международные отношения, Журналистика и др.\n\n"
            "4️⃣ <b>Школа права и государственного управления</b>\n"
            "   • Юриспруденция, Государственное управление"
        ),

        "session_title": "📅 <b>Академический календарь 2025–2026</b>",
        "session_body": (
            "<b>🍂 Осенний семестр</b>\n"
            "• Начало: <b>1 сентября</b>\n"
            "• Add/Drop период: 2–6 сентября\n"
            "• Период отказа: до 20 сентября\n"
            "• ВСК 1 (Midterm): 20–25 октября\n"
            "• ВСК 2 (Endterm): 8–13 декабря\n"
            "• Зимняя сессия: <b>15 декабря – 3 января</b>\n"
            "• Регистрация на FX-экзамен: 5–10 января\n"
            "• FX-пересдача: 12–17 января\n\n"
            "<b>🌱 Весенний семестр</b>\n"
            "• Начало: <b>26 января</b>\n"
            "• Add/Drop период: 26–31 января\n"
            "• Период отказа: до 14 февраля\n"
            "• ВСК 1 (Midterm): 16–21 марта\n"
            "• ВСК 2 (Endterm): 11–16 мая\n"
            "• Весенняя сессия: <b>18 мая – 6 июня</b>\n"
            "• Регистрация на FX-экзамен: 4–10 июня\n"
            "• FX-пересдача: 15–19 июня\n\n"
            "<b>☀️ Летний семестр:</b> 22 июня – 1 августа\n\n"
            "📌 <b>Система оценивания:</b>\n"
            "• ВСК1 — 30% | ВСК2 — 30% | Экзамен — 40%\n"
            "• Для допуска к экзамену: ВСК1+ВСК2 ≥ 100, посещ. ≥ 75%\n"
            "• Экзамен ≥50 — сдано | 25–49 — FX | <25 — Fail\n"
            "• FX-экзамен: ≥50 — сдано | <50 — Fail"
        ),

        "payment_title": "💳 <b>Оплата обучения</b>",
        "payment_body": (
            "📱 <b>Метод оплаты через Kaspi:</b>\n"
            "Kaspi → Платежи → Образование → ВУЗы и колледжи → <b>Университет Нархоз</b>\n\n"
            "💰 <b>Стоимость 1 кредита (бакалавриат):</b>\n"
            "• SDT / Инженерные / ИКТ: <b>~30 000 – 38 700 тенге</b>\n"
            "• Экономика, Финансы, Менеджмент: <b>~38 700 тенге</b>\n"
            "• Право, Гуманитарные: <b>~23 000 – 26 700 тенге</b>\n"
            "• Рекомендуемое кол-во кредитов в год: <b>62–70</b>\n\n"
            "🔁 <b>Пересдача (Retake / FX):</b>\n"
            "• FX-экзамен: оплата за кредит пересдаваемого предмета\n"
            "• Retake (повтор курса летом): полная стоимость кредитов\n"
            "• Летнее обучение: <b>22 июня – 1 августа</b>\n"
            "• Оплата по той же ставке, что и основной семестр\n\n"
            "🪖 <b>Военная кафедра:</b>\n"
            "• На договорной основе: ~45 000 тг/мес\n"
            "• Один учебный сбор: ~58 000 тг\n\n"
            "ℹ️ Уточнить точные суммы можно в Центре обслуживания студентов или на сайте narxoz.edu.kz"
        ),

        "dorm_title": "🏠 <b>Общежития Нархоз</b>",
        "dorm_body": (
            "Нархоз предлагает несколько вариантов общежитий:\n\n"
            "🏢 <b>Emen Housing</b> (новое, 424 места)\n"
            "   Отдельные санузлы, кухни, коворкинг, магазин, медпункт\n"
            "   💲 <b>82 000 тг/месяц</b>\n\n"
            "🏢 <b>Taugul</b>\n"
            "   💲 <b>55 000 тг/месяц</b>\n\n"
            "🏢 <b>Taugul 32</b>\n"
            "   💲 <b>55 000 тг/месяц</b>\n\n"
            "🏢 <b>Sain</b>\n"
            "   💲 <b>55 000 тг/месяц</b>\n\n"
            "🎾 На территории кампуса: стадион, фитнес-центр Grandpool, спортзал\n\n"
            "📞 По вопросам заселения: +7 727 377 1111"
        ),

        "contacts_title": "📞 <b>Важные контакты</b>",
        "contacts_body": (
            "🎓 <b>Центр обслуживания студентов:</b>\n"
            "   📱 +7 727 377 1111\n\n"
            "📋 <b>Приёмная комиссия:</b>\n"
            "   📱 +7 747 347 88 99\n\n"
            "🌍 <b>International Office:</b>\n"
            "   📱 +7 727 377 12 97\n\n"
            "🔒 <b>Комплаенс / Сенім телефоны:</b>\n"
            "   📱 8 (727) 377-11-02\n\n"
            "🏫 <b>Dean's Office SDT:</b>\n"
            "   📧 deansoffice.sdt@narxoz.kz\n\n"
            "👤 <b>Декан SDT:</b> Rassim Suliyev\n"
            "   🚪 Каб. 548 | rassim.suliyev@narxoz.kz\n\n"
            "👤 <b>Зам. Декана:</b> Assem Berniyazova\n"
            "   🚪 Каб. 543 | assem.berniyazova@narxoz.kz\n\n"
            "👤 <b>Зам. Декана:</b> Gulnur Abisheva\n"
            "   🚪 Каб. 552 | gulnur.abisheva@narxoz.kz\n\n"
            "📍 <b>Адрес:</b> Алматы, ул. Жандосова, 55\n"
            "🪖 <b>Военная кафедра:</b> мкр. 1, дом 81а"
        ),

        "iup_title": "📚 <b>ИУП — Выбери специальность:</b>",
        "iup_de": "💻 Digital Engineering",
        "iup_dmd": "🎨 Digital Management & Design",
        "iup_cyber": "🔐 Cybersecurity",
        "iup_amde": "📐 Applied Math in Digital Economy",
        "iup_sds": "📊 Statistics & Data Science",

        "schedule_title": "📋 <b>Расписание занятий</b>",
        "schedule_body": (
            "Здесь администраторы могут прикрепить актуальный файл расписания.\n\n"
            "📎 Чтобы прикрепить новый файл Excel/PDF:\n"
            "1. Отправь файл боту (только для администраторов)\n"
            "2. Файл станет доступен всем студентам\n\n"
            "Пока файл не загружен, расписание доступно на:\n"
            "• <a href='https://platonus.narxoz.kz'>platonus.narxoz.kz</a>"
        ),
        "schedule_uploaded": "✅ Расписание успешно обновлено! Студенты теперь могут его скачать.",
        "schedule_file_available": "📥 Актуальное расписание:",
        "schedule_no_file": "📭 Файл расписания ещё не загружен. Проверь на platonus.narxoz.kz",
        "admin_only": "⚠️ Загружать файлы могут только администраторы.",
    },

    "kz": {
        "welcome": (
            "👋 <b>Narxoz Student Helper</b> ботына қош келдіңіз!\n\n"
            "🎓 Мен Нархоз университеті туралы барлық қажетті ақпаратты табуға көмектесемін.\n\n"
            "Бөлімді таңдаңыз:"
        ),
        "menu_iup": "📚 ЖОЖ (Пәндер кестесі)",
        "menu_session": "📅 Сессия кестесі",
        "menu_payment": "💳 Төлем",
        "menu_dorm": "🏠 Жатақхана",
        "menu_contacts": "📞 Байланыстар",
        "menu_schools": "🏛️ Нархоз мектептері",
        "menu_schedule": "📋 Кесте тіркеу",
        "menu_info": "ℹ️ Университет туралы",
        "menu_lang": "🌐 Язык / Language / Тіл",
        "back": "⬅️ Артқа",
        "choose_lang": "Тілді таңдаңыз:",

        "info_title": "🎓 <b>Нархоз Университеті</b>",
        "info_body": (
            "📍 <b>Мекенжай:</b> Алматы қ., Жандосов к-сі, 55\n"
            "🪖 <b>Әскери кафедра:</b> Алматы, 1 мкр, 81а үй\n\n"
            "🌐 <b>Сайттар:</b>\n"
            "• <a href='https://canvas.narxoz.kz'>canvas.narxoz.kz</a> — оқу\n"
            "• <a href='https://platonus.narxoz.kz'>platonus.narxoz.kz</a> — жеке кабинет\n"
            "• <a href='http://shd.narxoz.kz'>shd.narxoz.kz</a> — өтініштер\n\n"
            "📣 <b>Миссия:</b> Нақты өмірде күрделі міндеттерді шеше алатын көшбасшыларды дайындау.\n\n"
            "🏆 <b>Аккредитациялар:</b> FIBAA, IQAA, QS Stars ⭐⭐⭐⭐\n"
            "🌍 <b>Серіктес:</b> Illinois Institute of Technology (АҚШ)"
        ),

        "schools_title": "🏛️ <b>Нархоз университетінің мектептері</b>",
        "schools_body": (
            "Нархозда 4 мектеп бар:\n\n"
            "1️⃣ <b>Цифрлық технологиялар мектебі (SDT)</b>\n"
            "   • Digital Engineering\n"
            "   • Digital Management & Design\n"
            "   • Cybersecurity\n"
            "   • Statistics & Data Science\n"
            "   • Applied Mathematics in Digital Economy\n\n"
            "2️⃣ <b>Экономика және менеджмент мектебі</b>\n"
            "   • Қаржы, Маркетинг, Менеджмент, BBA және т.б.\n\n"
            "3️⃣ <b>Гуманитарлық мектеп</b>\n"
            "   • Халықаралық қатынастар, Журналистика және т.б.\n\n"
            "4️⃣ <b>Құқық және мемлекеттік басқару мектебі</b>\n"
            "   • Заңтану, Мемлекеттік басқару"
        ),

        "session_title": "📅 <b>Академиялық күнтізбе 2025–2026</b>",
        "session_body": (
            "<b>🍂 Күзгі семестр</b>\n"
            "• Басталуы: <b>1 қыркүйек</b>\n"
            "• Add/Drop кезеңі: 2–6 қыркүйек\n"
            "• Бас тарту кезеңі: 20 қыркүйекке дейін\n"
            "• ВСК 1: 20–25 қазан\n"
            "• ВСК 2: 8–13 желтоқсан\n"
            "• Қысқы сессия: <b>15 желтоқсан – 3 қаңтар</b>\n"
            "• FX тіркеу: 5–10 қаңтар\n"
            "• FX қайта тапсыру: 12–17 қаңтар\n\n"
            "<b>🌱 Көктемгі семестр</b>\n"
            "• Басталуы: <b>26 қаңтар</b>\n"
            "• Add/Drop: 26–31 қаңтар\n"
            "• Бас тарту: 14 ақпанға дейін\n"
            "• ВСК 1: 16–21 наурыз\n"
            "• ВСК 2: 11–16 мамыр\n"
            "• Көктемгі сессия: <b>18 мамыр – 6 маусым</b>\n"
            "• FX тіркеу: 4–10 маусым\n"
            "• FX қайта тапсыру: 15–19 маусым\n\n"
            "<b>☀️ Жазғы семестр:</b> 22 маусым – 1 тамыз\n\n"
            "📌 <b>Бағалау жүйесі:</b>\n"
            "• ВСК1 — 30% | ВСК2 — 30% | Емтихан — 40%\n"
            "• Жіберілу үшін: ВСК1+ВСК2 ≥ 100, қатысу ≥ 75%\n"
            "• ≥50 — өтті | 25–49 — FX | <25 — Fail"
        ),

        "payment_title": "💳 <b>Оқу ақысы</b>",
        "payment_body": (
            "📱 <b>Kaspi арқылы төлем:</b>\n"
            "Kaspi → Төлемдер → Білім → ЖОО және колледждер → <b>Нархоз Университеті</b>\n\n"
            "💰 <b>1 кредит құны (бакалавриат):</b>\n"
            "• SDT / Инженерлік: <b>~30 000 – 38 700 тг</b>\n"
            "• Экономика, Қаржы: <b>~38 700 тг</b>\n"
            "• Құқық, Гуманитарлық: <b>~23 000 – 26 700 тг</b>\n"
            "• Жылына ұсынылатын кредиттер саны: <b>62–70</b>\n\n"
            "🔁 <b>Қайта тапсыру (Retake / FX):</b>\n"
            "• FX емтиханы: пән кредиттері бойынша төлем\n"
            "• Retake (жазда қайталау): толық кредит құны\n"
            "• Жазғы оқу: <b>22 маусым – 1 тамыз</b>\n\n"
            "🪖 <b>Әскери кафедра:</b>\n"
            "• Шартты негізде: ~45 000 тг/ай\n"
            "• Бір оқу жиыны: ~58 000 тг"
        ),

        "dorm_title": "🏠 <b>Нархоз жатақханалары</b>",
        "dorm_body": (
            "Нархоз бірнеше жатақхана ұсынады:\n\n"
            "🏢 <b>Emen Housing</b> (жаңа, 424 орын)\n"
            "   Жеке санузел, асхана, коворкинг, дүкен, медпункт\n"
            "   💲 <b>82 000 тг/ай</b>\n\n"
            "🏢 <b>Taugul</b>\n"
            "   💲 <b>55 000 тг/ай</b>\n\n"
            "🏢 <b>Taugul 32</b>\n"
            "   💲 <b>55 000 тг/ай</b>\n\n"
            "🏢 <b>Sain</b>\n"
            "   💲 <b>55 000 тг/ай</b>\n\n"
            "🎾 Кампуста: стадион, Grandpool фитнес орталығы, спортзал\n\n"
            "📞 Тұру мәселелері бойынша: +7 727 377 1111"
        ),

        "contacts_title": "📞 <b>Маңызды байланыстар</b>",
        "contacts_body": (
            "🎓 <b>Студенттерге қызмет көрсету орталығы:</b>\n"
            "   📱 +7 727 377 1111\n\n"
            "📋 <b>Қабылдау комиссиясы:</b>\n"
            "   📱 +7 747 347 88 99\n\n"
            "🌍 <b>International Office:</b>\n"
            "   📱 +7 727 377 12 97\n\n"
            "🔒 <b>Комплаенс / Сенім телефоны:</b>\n"
            "   📱 8 (727) 377-11-02\n\n"
            "🏫 <b>SDT Деканат:</b>\n"
            "   📧 deansoffice.sdt@narxoz.kz\n\n"
            "👤 <b>Декан SDT:</b> Rassim Suliyev\n"
            "   🚪 Каб. 548 | rassim.suliyev@narxoz.kz\n\n"
            "📍 <b>Мекенжай:</b> Алматы, Жандосов к-сі, 55\n"
            "🪖 <b>Әскери кафедра:</b> 1 мкр, 81а үй"
        ),

        "iup_title": "📚 <b>ЖОЖ — Мамандықты таңдаңыз:</b>",
        "iup_de": "💻 Digital Engineering",
        "iup_dmd": "🎨 Digital Management & Design",
        "iup_cyber": "🔐 Cybersecurity",
        "iup_amde": "📐 Applied Math in Digital Economy",
        "iup_sds": "📊 Statistics & Data Science",

        "schedule_title": "📋 <b>Сабақ кестесі</b>",
        "schedule_body": (
            "Мұнда әкімшілер өзекті кесте файлын тіркей алады.\n\n"
            "Файл жүктелмеген жағдайда кестені мына жерден қараңыз:\n"
            "• <a href='https://platonus.narxoz.kz'>platonus.narxoz.kz</a>"
        ),
        "schedule_uploaded": "✅ Кесте сәтті жаңартылды!",
        "schedule_file_available": "📥 Өзекті кесте:",
        "schedule_no_file": "📭 Кесте файлы жүктелмеген. platonus.narxoz.kz сайтын тексеріңіз.",
        "admin_only": "⚠️ Файлдарды тек әкімшілер жүктей алады.",
        "back": "⬅️ Артқа",
        "choose_lang": "Тілді таңдаңыз:",
    },

    "en": {
        "welcome": (
            "👋 Welcome to <b>Narxoz Student Helper</b>!\n\n"
            "🎓 I'll help you find all the information you need about Narxoz University.\n\n"
            "Choose a section:"
        ),
        "menu_iup": "📚 IUP (Course Curriculum)",
        "menu_session": "📅 Academic Calendar",
        "menu_payment": "💳 Payment",
        "menu_dorm": "🏠 Dormitories",
        "menu_contacts": "📞 Contacts",
        "menu_schools": "🏛️ Schools at Narxoz",
        "menu_schedule": "📋 Attach Schedule",
        "menu_info": "ℹ️ About the University",
        "menu_lang": "🌐 Язык / Language / Тіл",
        "back": "⬅️ Back",
        "choose_lang": "Choose a language:",

        "info_title": "🎓 <b>Narxoz University</b>",
        "info_body": (
            "📍 <b>Address:</b> Almaty, Zhandosov St., 55\n"
            "🪖 <b>Military Dept.:</b> Almaty, mkr. 1, building 81a\n\n"
            "🌐 <b>Websites:</b>\n"
            "• <a href='https://canvas.narxoz.kz'>canvas.narxoz.kz</a> — studies\n"
            "• <a href='https://platonus.narxoz.kz'>platonus.narxoz.kz</a> — personal cabinet\n"
            "• <a href='http://shd.narxoz.kz'>shd.narxoz.kz</a> — requests (Help Desk)\n\n"
            "📣 <b>Mission:</b> Training leaders who solve complex real-life tasks.\n\n"
            "🏆 <b>Accreditations:</b> FIBAA, IQAA, QS Stars ⭐⭐⭐⭐\n"
            "🌍 <b>Partner:</b> Illinois Institute of Technology (USA)"
        ),

        "schools_title": "🏛️ <b>Schools at Narxoz University</b>",
        "schools_body": (
            "Narxoz has 4 schools:\n\n"
            "1️⃣ <b>School of Digital Technologies (SDT)</b>\n"
            "   • Digital Engineering\n"
            "   • Digital Management & Design\n"
            "   • Cybersecurity\n"
            "   • Statistics & Data Science\n"
            "   • Applied Mathematics in Digital Economy\n\n"
            "2️⃣ <b>School of Economics & Management</b>\n"
            "   • Finance, Marketing, Management, BBA, etc.\n\n"
            "3️⃣ <b>Humanities School</b>\n"
            "   • International Relations, Journalism, etc.\n\n"
            "4️⃣ <b>School of Law & Public Administration</b>\n"
            "   • Law, Public Administration"
        ),

        "session_title": "📅 <b>Academic Calendar 2025–2026</b>",
        "session_body": (
            "<b>🍂 Fall Semester</b>\n"
            "• Start: <b>September 1</b>\n"
            "• Add/Drop period: Sep 2–6\n"
            "• Withdrawal period: before Sep 20\n"
            "• 1st Attestation (Midterm): Oct 20–25\n"
            "• 2nd Attestation (Endterm): Dec 8–13\n"
            "• Winter exam session: <b>Dec 15 – Jan 3</b>\n"
            "• FX exam registration: Jan 5–10\n"
            "• FX exam resit: Jan 12–17\n\n"
            "<b>🌱 Spring Semester</b>\n"
            "• Start: <b>January 26</b>\n"
            "• Add/Drop: Jan 26–31\n"
            "• Withdrawal: before Feb 14\n"
            "• 1st Attestation (Midterm): Mar 16–21\n"
            "• 2nd Attestation (Endterm): May 11–16\n"
            "• Spring exam session: <b>May 18 – Jun 6</b>\n"
            "• FX exam registration: Jun 4–10\n"
            "• FX exam resit: Jun 15–19\n\n"
            "<b>☀️ Summer Semester:</b> Jun 22 – Aug 1\n\n"
            "📌 <b>Grading System:</b>\n"
            "• VSK1 — 30% | VSK2 — 30% | Exam — 40%\n"
            "• To pass: VSK1+VSK2 ≥ 100, attendance ≥ 75%\n"
            "• ≥50 — Pass | 25–49 — FX | <25 — Fail\n"
            "• FX exam: ≥50 — Pass | <50 — Fail"
        ),

        "payment_title": "💳 <b>Tuition Payment</b>",
        "payment_body": (
            "📱 <b>Payment via Kaspi:</b>\n"
            "Kaspi → Payments → Education → Universities & Colleges → <b>Narxoz University</b>\n\n"
            "💰 <b>Cost per credit (bachelor's):</b>\n"
            "• SDT / Engineering / ICT: <b>~30,000 – 38,700 KZT</b>\n"
            "• Economics, Finance, Management: <b>~38,700 KZT</b>\n"
            "• Law, Humanities: <b>~23,000 – 26,700 KZT</b>\n"
            "• Recommended credits per year: <b>62–70</b>\n\n"
            "🔁 <b>Retakes (FX / Retake):</b>\n"
            "• FX exam: pay per credit of the retaken subject\n"
            "• Retake (summer repeat): full credit cost\n"
            "• Summer semester: <b>Jun 22 – Aug 1</b>\n\n"
            "🪖 <b>Military Department:</b>\n"
            "• Contract basis: ~45,000 KZT/month\n"
            "• One training session: ~58,000 KZT"
        ),

        "dorm_title": "🏠 <b>Narxoz Dormitories</b>",
        "dorm_body": (
            "Narxoz offers several dormitory options:\n\n"
            "🏢 <b>Emen Housing</b> (new, 424 rooms)\n"
            "   Private bathrooms, kitchens, coworking, store, medical center\n"
            "   💲 <b>82,000 KZT/month</b>\n\n"
            "🏢 <b>Taugul</b>\n"
            "   💲 <b>55,000 KZT/month</b>\n\n"
            "🏢 <b>Taugul 32</b>\n"
            "   💲 <b>55,000 KZT/month</b>\n\n"
            "🏢 <b>Sain</b>\n"
            "   💲 <b>55,000 KZT/month</b>\n\n"
            "🎾 On campus: stadium, Grandpool fitness center, sports hall\n\n"
            "📞 For accommodation questions: +7 727 377 1111"
        ),

        "contacts_title": "📞 <b>Important Contacts</b>",
        "contacts_body": (
            "🎓 <b>Student Services Center:</b>\n"
            "   📱 +7 727 377 1111\n\n"
            "📋 <b>Admissions Office:</b>\n"
            "   📱 +7 747 347 88 99\n\n"
            "🌍 <b>International Office:</b>\n"
            "   📱 +7 727 377 12 97\n\n"
            "🔒 <b>Compliance / Trust Hotline:</b>\n"
            "   📱 8 (727) 377-11-02\n\n"
            "🏫 <b>SDT Dean's Office:</b>\n"
            "   📧 deansoffice.sdt@narxoz.kz\n\n"
            "👤 <b>Dean SDT:</b> Rassim Suliyev\n"
            "   🚪 Room 548 | rassim.suliyev@narxoz.kz\n\n"
            "📍 <b>Address:</b> Almaty, Zhandosov St., 55\n"
            "🪖 <b>Military Dept.:</b> mkr. 1, building 81a"
        ),

        "iup_title": "📚 <b>IUP — Choose your program:</b>",
        "iup_de": "💻 Digital Engineering",
        "iup_dmd": "🎨 Digital Management & Design",
        "iup_cyber": "🔐 Cybersecurity",
        "iup_amde": "📐 Applied Math in Digital Economy",
        "iup_sds": "📊 Statistics & Data Science",

        "schedule_title": "📋 <b>Class Schedule</b>",
        "schedule_body": (
            "Admins can attach the current schedule file here.\n\n"
            "Until uploaded, check:\n"
            "• <a href='https://platonus.narxoz.kz'>platonus.narxoz.kz</a>"
        ),
        "schedule_uploaded": "✅ Schedule updated successfully!",
        "schedule_file_available": "📥 Current schedule:",
        "schedule_no_file": "📭 No schedule file uploaded yet. Check platonus.narxoz.kz",
        "admin_only": "⚠️ Only admins can upload files.",
    }
}

# IUP Data
IUP_DATA = {
    "de": {
        "title": "💻 <b>Digital Engineering — ИУП</b>",
        "body": (
            "<b>📗 1-й год</b>\n"
            "<b>Осень:</b> Иностранный язык, ИКТ, Линейная алгебра, Математический анализ 1, Алгоритмизация и программирование\n"
            "<b>Весна:</b> Иностранный язык, Этика и письмо, Дискретная математика, Математический анализ 2, Объектно-ориентированное программирование\n\n"
            "<b>📘 2-й год</b>\n"
            "<b>Осень:</b> История Казахстана, Физкультура, Теория вероятностей и мат. статистика, Основы веб-технологий, Алгоритмы и структуры данных, Основы информационной безопасности, СУБД\n"
            "<b>Весна:</b> Соц.-полит. знания, Физкультура, Компьютерная архитектура и ОС, Back-end разработка, Front-end разработка, Электив G1\n\n"
            "<b>📙 3-й год</b>\n"
            "<b>Осень:</b> Казахский/Русский язык, Физкультура, Программная инженерия, Введение в компьютерные сети, Электив G2 (×3)\n"
            "<b>Весна:</b> Казахский/Русский язык, Физкультура, Философия, Методы исследования, Электив G3 (×3)\n\n"
            "<b>📕 4-й год</b>\n"
            "<b>Осень/Весна:</b> Профессиональная практика, Лидерство и инновации, Карьерное развитие, Итоговый экзамен, Электив G4 (×5)\n\n"
            "<b>🎯 Треки:</b> Full-stack Dev | AI Developer | DevOps Engineer | Free Elective"
        )
    },
    "dmd": {
        "title": "🎨 <b>Digital Management & Design — ИУП</b>",
        "body": (
            "<b>📗 1-й год</b>\n"
            "<b>Осень:</b> Иностранный язык, ИКТ, Линейная алгебра, Математический анализ 1, Алгоритмизация и программирование\n"
            "<b>Весна:</b> Иностранный язык, Этика и письмо, Дискретная математика, Математический анализ 2, Объектно-ориентированное программирование\n\n"
            "<b>📘 2-й год</b>\n"
            "<b>Осень:</b> История Казахстана, Физкультура, ТВ и мат. статистика, Основы веб-технологий, Алгоритмы и структуры данных, Основы ИБ, СУБД\n"
            "<b>Весна:</b> Соц.-полит. знания, Физкультура, Компьютерная архитектура и ОС, Back-end, Front-end, Электив G1\n\n"
            "<b>📙 3-й год</b>\n"
            "<b>Осень:</b> Каз./Рус. язык, Физкультура, Принципы маркетинга, Введение в экономику, Электив G2 (×3)\n"
            "<b>Весна:</b> Каз./Рус. язык, Физкультура, Философия, Методы исследования, Электив G3 (×3)\n\n"
            "<b>📕 4-й год:</b> Практика, Лидерство, Карьера, Итоговый экзамен, G4-электив (×5)\n\n"
            "<b>🎯 Треки:</b> Digital Manager | Digital Designer | Free Elective"
        )
    },
    "cyber": {
        "title": "🔐 <b>Cybersecurity — ИУП</b>",
        "body": (
            "<b>📗 1-й год</b>\n"
            "<b>Осень:</b> Иностранный язык, Этика и письмо, Линейная алгебра, Математический анализ 1, Алгоритмизация\n"
            "<b>Весна:</b> Иностранный язык, ИКТ, Дискретная математика, Математический анализ 2, ООП\n\n"
            "<b>📘 2-й год</b>\n"
            "<b>Осень:</b> История Казахстана, Физкультура, ТВ и мат. статистика, Маршрутизация и коммутация, Алгоритмы и структуры данных, Основы ИБ, Основы электроники\n"
            "<b>Весна:</b> Соц.-полит. знания, Физкультура, Компьютерная архитектура и ОС, Введение в криптографию, Цифровая электроника, Электив G1\n\n"
            "<b>📙 3-й год</b>\n"
            "<b>Осень:</b> Каз./Рус. язык, Физкультура, Введение в кибербезопасность, IT-инфраструктура, Электив G2 (×3)\n"
            "<b>Весна:</b> Каз./Рус. язык, Физкультура, Философия, Методы исследования, Электив G3 (×3)\n\n"
            "<b>📕 4-й год:</b> Практика, Лидерство, Карьера, Итоговый экзамен, G4-электив (×5)\n\n"
            "<b>🎯 Треки:</b> Software Security Engineer | Systems Security Engineer | Free Elective"
        )
    },
    "amde": {
        "title": "📐 <b>Applied Mathematics in Digital Economy — ИУП</b>",
        "body": (
            "<b>📗 1-й год</b>\n"
            "<b>Осень:</b> Иностранный язык, Этика и письмо, Линейная алгебра и аналитическая геометрия, Математический анализ 1, Основы программирования\n"
            "<b>Весна:</b> Иностранный язык, ИКТ, Дискретная математика, Математический анализ 2, Программирование технологии\n\n"
            "<b>📘 2-й год</b>\n"
            "<b>Осень:</b> История Казахстана, Физкультура, Философия, ТВ и мат. статистика, Математический анализ III, Алгоритмы и структуры данных, Дифференциальные уравнения\n"
            "<b>Весна:</b> Соц.-полит. знания, Физкультура, Мат. анализ IV, Статистика, Численные методы, Электив G1\n\n"
            "<b>📙 3-й год</b>\n"
            "<b>Осень:</b> Каз./Рус. язык, Физкультура, Введение в экономику, Уравнения мат. физики, Электив G2 (×3)\n"
            "<b>Весна:</b> Каз./Рус. язык, Физкультура, Методы исследования, Математическое моделирование, Электив G3 (×3)\n\n"
            "<b>📕 4-й год:</b> Практика, Лидерство, Карьера, Итоговый экзамен, G4-электив (×5)\n\n"
            "<b>🎯 Треки:</b> Applied Data Analysis | Risk Analysis & Modelling | Free Elective"
        )
    },
    "sds": {
        "title": "📊 <b>Statistics & Data Science — ИУП</b>",
        "body": (
            "<b>📗 1-й год</b>\n"
            "<b>Осень:</b> Иностранный язык, Этика и письмо, Линейная алгебра и аналитическая геометрия, Математический анализ 1, Основы программирования\n"
            "<b>Весна:</b> Иностранный язык, ИКТ, Дискретная математика, Математический анализ 2, Программирование технологии\n\n"
            "<b>📘 2-й год</b>\n"
            "<b>Осень:</b> История Казахстана, Физкультура, Философия, ТВ и мат. статистика, Мат. анализ III, Алгоритмы и структуры данных, Дифференциальные уравнения\n"
            "<b>Весна:</b> Соц.-полит. знания, Физкультура, Мат. анализ IV, Статистика, Численные методы, Электив G1\n\n"
            "<b>📙 3-й год</b>\n"
            "<b>Осень:</b> Каз./Рус. язык, Физкультура, Прикладная статистика, Анализ больших данных, Электив G2 (×3)\n"
            "<b>Весна:</b> Каз./Рус. язык, Физкультура, Методы исследования, Временные ряды и прогнозирование, Электив G3 (×3)\n\n"
            "<b>📕 4-й год:</b> Практика, Лидерство, Карьера, Итоговый экзамен, G4-электив (×5)\n\n"
            "<b>🎯 Треки:</b> Data Science | Business Statistics | Free Elective"
        )
    }
}

# Admin IDs — replace with real Telegram user IDs
ADMIN_IDS = {123456789}  # 👈 Add your Telegram ID here

# In-memory schedule file storage
schedule_file = {"file_id": None, "file_name": None}

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def get_lang(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("lang", "ru")

def t(key: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    lang = get_lang(context)
    return TEXTS[lang].get(key, TEXTS["ru"].get(key, key))

def main_menu_keyboard(context):
    lang = get_lang(context)
    tx = TEXTS[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(tx["menu_iup"], callback_data="iup"),
         InlineKeyboardButton(tx["menu_session"], callback_data="session")],
        [InlineKeyboardButton(tx["menu_payment"], callback_data="payment"),
         InlineKeyboardButton(tx["menu_dorm"], callback_data="dorm")],
        [InlineKeyboardButton(tx["menu_contacts"], callback_data="contacts"),
         InlineKeyboardButton(tx["menu_schools"], callback_data="schools")],
        [InlineKeyboardButton(tx["menu_schedule"], callback_data="schedule"),
         InlineKeyboardButton(tx["menu_info"], callback_data="info")],
        [InlineKeyboardButton(tx["menu_lang"], callback_data="lang")],
    ])

def back_button(context):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(t("back", context), callback_data="back")
    ]])

def iup_keyboard(context):
    lang = get_lang(context)
    tx = TEXTS[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(tx["iup_de"], callback_data="iup_de")],
        [InlineKeyboardButton(tx["iup_dmd"], callback_data="iup_dmd")],
        [InlineKeyboardButton(tx["iup_cyber"], callback_data="iup_cyber")],
        [InlineKeyboardButton(tx["iup_amde"], callback_data="iup_amde")],
        [InlineKeyboardButton(tx["iup_sds"], callback_data="iup_sds")],
        [InlineKeyboardButton(t("back", context), callback_data="back")],
    ])

# ─────────────────────────────────────────────────────────────────────────────
# HANDLERS
# ─────────────────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "lang" not in context.user_data:
        context.user_data["lang"] = "ru"
    await update.message.reply_text(
        t("welcome", context),
        reply_markup=main_menu_keyboard(context),
        parse_mode="HTML"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Language selection
    if data == "lang":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🇷🇺 Русский", callback_data="set_lang_ru")],
            [InlineKeyboardButton("🇰🇿 Қазақша", callback_data="set_lang_kz")],
            [InlineKeyboardButton("🇬🇧 English", callback_data="set_lang_en")],
            [InlineKeyboardButton(t("back", context), callback_data="back")],
        ])
        await query.edit_message_text(t("choose_lang", context), reply_markup=kb)
        return

    if data.startswith("set_lang_"):
        lang = data.split("_")[-1]
        context.user_data["lang"] = lang
        await query.edit_message_text(
            t("welcome", context),
            reply_markup=main_menu_keyboard(context),
            parse_mode="HTML"
        )
        return

    # Back to main menu
    if data == "back":
        await query.edit_message_text(
            t("welcome", context),
            reply_markup=main_menu_keyboard(context),
            parse_mode="HTML"
        )
        return

    # IUP menu
    if data == "iup":
        await query.edit_message_text(
            t("iup_title", context),
            reply_markup=iup_keyboard(context),
            parse_mode="HTML"
        )
        return

    # IUP program detail
    if data.startswith("iup_"):
        prog = data[4:]  # de, dmd, cyber, amde, sds
        if prog in IUP_DATA:
            info = IUP_DATA[prog]
            await query.edit_message_text(
                f"{info['title']}\n\n{info['body']}",
                reply_markup=back_button(context),
                parse_mode="HTML"
            )
        return

    # Session
    if data == "session":
        await query.edit_message_text(
            f"{t('session_title', context)}\n\n{t('session_body', context)}",
            reply_markup=back_button(context),
            parse_mode="HTML"
        )
        return

    # Payment
    if data == "payment":
        await query.edit_message_text(
            f"{t('payment_title', context)}\n\n{t('payment_body', context)}",
            reply_markup=back_button(context),
            parse_mode="HTML"
        )
        return

    # Dorm
    if data == "dorm":
        await query.edit_message_text(
            f"{t('dorm_title', context)}\n\n{t('dorm_body', context)}",
            reply_markup=back_button(context),
            parse_mode="HTML"
        )
        return

    # Contacts
    if data == "contacts":
        await query.edit_message_text(
            f"{t('contacts_title', context)}\n\n{t('contacts_body', context)}",
            reply_markup=back_button(context),
            parse_mode="HTML"
        )
        return

    # Schools
    if data == "schools":
        await query.edit_message_text(
            f"{t('schools_title', context)}\n\n{t('schools_body', context)}",
            reply_markup=back_button(context),
            parse_mode="HTML"
        )
        return

    # Schedule
    if data == "schedule":
        if schedule_file["file_id"]:
            await query.edit_message_text(
                f"{t('schedule_title', context)}\n\n{t('schedule_file_available', context)}",
                reply_markup=back_button(context),
                parse_mode="HTML"
            )
            await context.bot.send_document(
                chat_id=query.message.chat_id,
                document=schedule_file["file_id"],
                filename=schedule_file["file_name"] or "schedule.xlsx"
            )
        else:
            await query.edit_message_text(
                f"{t('schedule_title', context)}\n\n{t('schedule_body', context)}\n\n{t('schedule_no_file', context)}",
                reply_markup=back_button(context),
                parse_mode="HTML",
                disable_web_page_preview=True
            )
        return

    # Info
    if data == "info":
        await query.edit_message_text(
            f"{t('info_title', context)}\n\n{t('info_body', context)}",
            reply_markup=back_button(context),
            parse_mode="HTML",
            disable_web_page_preview=True
        )
        return


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admins can upload an Excel/PDF schedule file"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text(t("admin_only", context))
        return

    doc = update.message.document
    schedule_file["file_id"] = doc.file_id
    schedule_file["file_name"] = doc.file_name
    await update.message.reply_text(t("schedule_uploaded", context))


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    logger.info("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
