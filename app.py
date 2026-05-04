import streamlit as st
import pandas as pd

# Guard
if st.session_state.get("role") != "admin":
    st.error("Доступ запрещён")
    st.stop()

st.title("Администрирование")
st.caption("Управление пользователями, ролями и системными настройками")

tab_users, tab_roles, tab_settings, tab_metrics = st.tabs(
    ["Пользователи", "Роли и доступы", "Настройки", "Метрики"]
)

with tab_users:
    # Метрики
    c1, c2, c3 = st.columns(3)
    c1.metric("Всего юзеров", "1,247")
    c2.metric("Активных за 7д", "892", "+12%")
    c3.metric("Заблокированных", "8")

    # Фильтры
    f1, f2, f3 = st.columns([3, 1, 1])
    search = f1.text_input(
        "Поиск", placeholder="🔍 Поиск по email или имени",
        label_visibility="collapsed",
    )
    role = f2.selectbox(
        "Роль", ["все", "admin", "editor", "viewer"],
        label_visibility="collapsed",
    )
    f3.button("➕ Добавить", type="primary", use_container_width=True)

    # Таблица
    df = load_users(search, role)  # ваша функция с @st.cache_data
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "status": st.column_config.TextColumn("Статус"),
            "last_seen": st.column_config.DatetimeColumn("Был онлайн"),
        },
    )
