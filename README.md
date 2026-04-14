# FX Revenue Dashboard · Stape

Интерактивный дашборд для анализа и симуляции выручки FX-платформы.  
Развёрнут на [Streamlit Community Cloud](https://streamlit.io/cloud).

![Stape](https://img.shields.io/badge/Powered%20by-Stape-7B2FF7?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=flat-square&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python)

---

## Возможности

| Раздел | Функционал |
|--------|-----------|
| **Обзор** | KPI-карточки, стековая динамика по месяцам, тиры, источники, разбивка по парам |
| **Калькулятор** | Слайдеры спреда на каждую пару, эластичность объёма, таблица безубыточности, сравнение база vs симуляция |
| **Анализ** | Тепловая карта пара × месяц, распределение кастомных спредов, паттерны по часам и дням недели |
| **Экспорт** | CSV (выборка), Excel (4 листа), настройки спреда, сырые данные |

## Импорт данных

Загрузите CSV или Excel через боковую панель. Ожидаемые колонки:

```
updated_at | source | from_currency | to_currency
from_amount | to_amount | spread | fx_revenue_usd
original_rate_fixed | rate_usd_fixed
```

## Формула расчёта выручки

```
fx_revenue_usd = (from_amount × original_rate_fixed – to_amount) × rate_usd_fixed
```

Симуляция с эластичностью:

```
sim_rev = base_rev × (new_spread / real_spread) × (1 + elasticity × max(0, old − new))
```

## Деплой на Streamlit Cloud

1. Форкните / скопируйте этот репозиторий на GitHub
2. Перейдите на [share.streamlit.io](https://share.streamlit.io)
3. Нажмите **New app** → выберите репозиторий → `app.py`
4. **Deploy!**

## Локальный запуск

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Структура проекта

```
├── app.py                  # Основное приложение
├── requirements.txt        # Python-зависимости
├── .streamlit/
│   └── config.toml         # Тема и настройки сервера
└── README.md
```

---

© Stape · FX Analytics
