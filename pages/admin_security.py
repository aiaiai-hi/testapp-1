import pandas as pd
import streamlit as st

from ui_shared import StatCard, apply_admin_theme, render_hero, render_stat_grid, section_title


apply_admin_theme()

render_hero(
    "Безопасность",
    "Мониторинг политик, сессий, ключей API и событий риска в одном административном контуре.",
    "Администрирование",
)

render_stat_grid(
    [
        StatCard("Security score", "94", "+3 за неделю", "good"),
        StatCard("MFA coverage", "99%", "+2%", "good"),
        StatCard("Risk alerts", "5", "2 high", "warn"),
        StatCard("Open tokens", "128", "-14", "neutral"),
    ]
)

tabs = st.tabs(["Политики", "Сессии", "API-ключи", "События"])

with tabs[0]:
    left, right = st.columns([1, 1], gap="large")
    with left:
        section_title("Вход и MFA")
        st.toggle("Требовать MFA для всех ролей", value=True)
        st.toggle("Блокировать вход из новых стран", value=True)
        st.toggle("Разрешить magic links", value=False)
        st.slider("Длительность сессии, часов", 1, 24, 8)
    with right:
        section_title("Правила доступа")
        st.checkbox("Owner approval для экспорта", value=True)
        st.checkbox("IP allowlist для финансов", value=True)
        st.checkbox("Автоотзыв неактивных токенов", value=True)
        st.button("Сохранить политики", icon=":material/save:", type="primary")

with tabs[1]:
    sessions = pd.DataFrame(
        {
            "Пользователь": ["Anna", "Ilya", "Maria", "Timur"],
            "Устройство": ["MacBook", "Chrome", "Safari", "Windows"],
            "Город": ["Moscow", "Berlin", "Dubai", "Almaty"],
            "Риск": ["Low", "Low", "Medium", "Low"],
        }
    )
    st.dataframe(sessions, hide_index=True, width="stretch")

with tabs[2]:
    keys = pd.DataFrame(
        {
            "Ключ": ["prod-sync", "billing-read", "warehouse-loader", "sandbox-ci"],
            "Scope": ["write", "read", "write", "read"],
            "Последнее использование": ["5 мин назад", "2 ч назад", "Вчера", "7 дней назад"],
            "Ротация": ["12 дней", "28 дней", "4 дня", "Сегодня"],
        }
    )
    st.dataframe(keys, hide_index=True, width="stretch")

with tabs[3]:
    events = pd.DataFrame(
        {
            "Время": ["10:42", "10:18", "09:41", "09:02"],
            "Событие": ["MFA challenge", "Blocked token", "Policy change", "Suspicious export"],
            "Серьезность": ["Info", "Warning", "Info", "High"],
        }
    )
    st.dataframe(events, hide_index=True, width="stretch")
