from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def show_ip(request: Request):
    # Берём реальный IP (учитываем прокси/VPN)
    forwarded = request.headers.get("X-Forwarded-For")
    ip = forwarded.split(",")[0].strip() if forwarded else request.client.host

    timestamp = datetime.now().strftime("%H:%M:%S")

    # Выводим в твой терминал PyCharm
    print(f"\n [{timestamp}] Клиент подключился!")
    print(f" IP адрес : {ip}")
    print(f" User-Agent: {request.headers.get('user-agent', '—')}")
    print("-" * 40)

    # Клиент видит свой IP на странице
    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Ваш IP</title>
        <style>
            body {{
                font-family: monospace;
                background: #0d1b26;
                color: #00d4ff;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                flex-direction: column;
                gap: 16px;
            }}
            .ip {{
                font-size: 48px;
                font-weight: bold;
            }}
            .label {{
                font-size: 14px;
                color: #4a7a94;
                letter-spacing: 2px;
            }}
        </style>
    </head>
    <body>
        <div class="label">ВАШ IP АДРЕС</div>
        <div class="ip">{ip}</div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)
