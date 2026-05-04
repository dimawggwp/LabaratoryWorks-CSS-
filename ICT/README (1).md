# 🎓 Narxoz Student Helper — Веб-сайт

**Студентке Көмекші** | Студенческий помощник | Student Helper

Нархоз университетінің студенттеріне арналған толық ақпараттық сайт + ИИ агент.

---

## 📁 Файл құрылымы

```
narxoz_site/
├── app.py              # Flask бэкенд + Anthropic API
├── requirements.txt    # Python тәуелділіктері
├── templates/
│   └── index.html      # Негізгі бет (барлық HTML/CSS/JS)
└── README.md
```

---

## 🚀 Іске қосу (Запуск)

### 1. Тәуелділіктерді орнату
```bash
pip install -r requirements.txt
```

### 2. API кілтін орнату
```bash
# Linux / Mac
export ANTHROPIC_API_KEY="your_api_key_here"

# Windows (CMD)
set ANTHROPIC_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="your_api_key_here"
```

> 🔑 API кілтін https://console.anthropic.com сайтынан алыңыз

### 3. Серверді іске қосу
```bash
python app.py
```

### 4. Браузерде ашу
```
http://localhost:5000
```

---

## ✨ Функционал

| Бөлім | Мазмұн |
|-------|--------|
| 🏠 **Басты бет** | Нархоз туралы жалпы ақпарат, статистика |
| 📚 **ИУП / ЖОЖ** | SDT-ның 5 бағдарламасы бойынша 4 жылдық пәндер |
| 📅 **Сессия** | 2025–2026 академиялық күнтізбе + бағалау жүйесі |
| 💳 **Оплата** | Кредит бағасы, Retake/FX, Kaspi төлем |
| 🏠 **Общежитие** | 4 жатақхана + бағалар (55 000–82 000 ₸) |
| 📞 **Контакттар** | Барлық маңызды телефондар мен email |
| 🔗 **Сілтемелер** | Canvas, Platonus, Help Desk, Telegram bot |
| 🤖 **ИИ Агент** | Claude AI-мен чат (қаз/рус/eng) |

---

## 🎨 Дизайн

- **Цвет**: Нархоз бренд-бояулары — қызыл (`#C8102E`) + ақ
- **Шрифттар**: Bebas Neue (заголовки) + Montserrat (мәтін)
- **Responsive**: Мобильді дизайн қолдауы
- **Анимациялар**: Scroll-reveal, hover эффектілері

---

## 🤖 ИИ Агент туралы

- **Модель**: Claude Sonnet 4 (claude-sonnet-4-20250514)
- **Тілдер**: Қазақша, орысша, ағылшынша
- **Білім базасы**: ИУП, сессия, оплата, жатақхана, контакттар
- **Endpoint**: `POST /api/chat`

---

## 📱 Telegram Bot

**@helpertostudentsbot** — https://t.me/helpertostudentsbot

Бот сайтпен бірдей функцияларды қолдайды, тек Telegram арқылы.

---

## 📞 Маңызды контакттар

- ЦОС: +7 727 377 1111
- Қабылдау: +7 747 347 88 99  
- International: +7 727 377 12 97
- Адрес: Алматы, Жандосов 55
