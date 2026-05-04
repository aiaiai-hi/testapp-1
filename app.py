import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.title("Администрирование")
st.caption("Управление пользователями, ролями и системными настройками")

# Мок-данные вместо реальной БД
@st.cache_data
def load_users(search: str = "", role: str = "все") -> pd.DataFrame:
    data = [
        {"email": "anna.petrova@acme.com", "role": "admin",
         "status": "🟢 активен",      "last_seen": datetime.now() - timedelta(minutes=2)},
        {"email": "m.ivanov@acme.com",    "role": "editor",
         "status": "🟢 активен",      "last_seen": datetime.now() - timedelta(hours=1)},
        {"email": "k.sokolov@acme.com",   "role": "viewer",
         "status": "⚪ оффлайн",      "last_seen": datetime.now() - timedelta(days=3)},
        {"email": "test.user@acme.com",   "role": "viewer",
         "status": "🔴 заблокирован", "last_seen": datetime.now() - timedelta(days=12)},
    ]
    df = pd.DataFrame(data)
    if search:
        df = df[df["email"].str.contains(search, case=False)]
    if role != "все":
        df = df[df["role"] == role]
    return df


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
    df = load_users(search, role)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "email":     st.column_config.TextColumn("Email"),
            "role":      st.column_config.TextColumn("Роль"),
            "status":    st.column_config.TextColumn("Статус"),
            "last_seen": st.column_config.DatetimeColumn("Был онлайн", format="DD.MM.YYYY HH:mm"),
        },
    )

with tab_roles:
    st.info("Здесь будет матрица «роль × право»")

with tab_settings:
    st.info("Здесь будут системные настройки")

with tab_metrics:
    st.info("Здесь будут графики нагрузки")
