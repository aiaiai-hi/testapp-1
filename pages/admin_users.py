import pandas as pd
import streamlit as st

from ui_shared import apply_admin_theme, render_hero, render_pills, sample_users, section_title


apply_admin_theme()

render_hero(
    "Пользователи и роли",
    "Единый экран для владельцев, администраторов, аналитиков и аудиторов с быстрым контролем прав.",
    "Администрирование",
)

actions = st.columns([1, 1, 1, 2], gap="small")
actions[0].button("Добавить", icon=":material/person_add:", type="primary", width="stretch")
actions[1].button("Импорт", icon=":material/upload_file:", width="stretch")
actions[2].button("Экспорт", icon=":material/download:", width="stretch")
actions[3].text_input("Поиск", placeholder="Имя, email, роль")

tabs = st.tabs(["Команда", "Роли", "Приглашения", "Аудит"])

with tabs[0]:
    users = sample_users()
    st.dataframe(users, hide_index=True, width="stretch")

    left, right = st.columns([1, 1], gap="large")
    with left:
        section_title("Сводка доступа")
        render_pills(
            [
                ("SSO enabled", "ok"),
                ("MFA required", "ok"),
                ("2 risky accounts", "alert"),
                ("SCIM sync", "info"),
            ]
        )
    with right:
        section_title("Быстрое действие")
        selected = st.selectbox("Пользователь", users["Пользователь"].tolist())
        role = st.selectbox("Новая роль", ["Owner", "Admin", "Analyst", "Support", "Auditor"])
        st.button(f"Назначить роль: {role}", icon=":material/admin_panel_settings:")

with tabs[1]:
    roles = pd.DataFrame(
        {
            "Роль": ["Owner", "Admin", "Analyst", "Support", "Auditor"],
            "Пользователей": [2, 8, 42, 26, 3],
            "Доступ": ["Full", "Manage", "Read + export", "Tickets", "Read only"],
            "MFA": ["Required", "Required", "Required", "Required", "Required"],
        }
    )
    st.dataframe(roles, hide_index=True, width="stretch")

with tabs[2]:
    pending = pd.DataFrame(
        {
            "Email": ["finance@company.test", "ops.lead@company.test", "auditor@company.test"],
            "Роль": ["Analyst", "Admin", "Auditor"],
            "Отправлено": ["Сегодня", "Вчера", "30 апреля"],
        }
    )
    st.dataframe(pending, hide_index=True, width="stretch")

with tabs[3]:
    st.markdown(
        """
        <div class="timeline">
            <div class="timeline-item"><b>10:42</b> · Анна назначила роль Admin<br><span>Пользователь: Илья Орлов</span></div>
            <div class="timeline-item"><b>09:57</b> · Система заблокировала рискованный вход<br><span>IP: 203.0.113.42</span></div>
            <div class="timeline-item"><b>08:20</b> · Мария экспортировала список пользователей<br><span>Формат: CSV</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
