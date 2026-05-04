import pandas as pd
import streamlit as st

from ui_shared import StatCard, apply_admin_theme, render_hero, render_pills, render_stat_grid, sample_timeseries, section_title


st.set_page_config(
    page_title="Glossy Admin",
    page_icon="◼",
    layout="wide",
    initial_sidebar_state="expanded",
)


def overview() -> None:
    render_hero(
        "Glossy Admin",
        "Современная админ-панель с быстрыми метриками, живыми вкладками, аудитом действий и управлением доступами.",
        "Streamlit 1.57.0",
    )

    render_stat_grid(
        [
            StatCard("Активные пользователи", "12 840", "+8.6% за неделю", "good"),
            StatCard("Средний SLA", "98.4%", "+1.2 пункта", "good"),
            StatCard("Очередь модерации", "37", "12 срочных", "warn"),
            StatCard("Инциденты", "2", "-4 за сутки", "neutral"),
        ]
    )

    top_left, top_right = st.columns([1.55, 1], gap="large")

    with top_left:
        section_title("Операционная динамика")
        data = sample_timeseries()
        chart_data = data.set_index("День")[["Заявки", "Ошибки"]]
        st.line_chart(chart_data, height=330, width="stretch")

    with top_right:
        section_title("Состояние системы")
        st.metric("Latency P95", "184 ms", "-16 ms")
        st.metric("Успешные задания", "99.12%", "+0.28%")
        st.metric("API budget", "72%", "-6%")
        render_pills(
            [
                ("Core API healthy", "ok"),
                ("Billing sync delayed", "alert"),
                ("Warehouse online", "info"),
            ]
        )

    st.divider()
    tabs = st.tabs(["Очередь", "Финансы", "Интеграции", "Качество"])

    with tabs[0]:
        queue = pd.DataFrame(
            {
                "Задача": ["KYC review", "Refund approval", "Data enrichment", "Priority ticket"],
                "Владелец": ["Support", "Finance", "Ops", "Success"],
                "Приоритет": ["High", "Medium", "Low", "High"],
                "Возраст": ["18 мин", "41 мин", "2 ч", "9 мин"],
            }
        )
        st.dataframe(queue, hide_index=True, width="stretch")

    with tabs[1]:
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("MRR", "$428K", "+5.1%")
        col_b.metric("Churn risk", "3.2%", "-0.4%")
        col_c.metric("Unpaid invoices", "$18K", "-$4K")

    with tabs[2]:
        integrations = pd.DataFrame(
            {
                "Сервис": ["CRM", "Data Lake", "Payments", "Email"],
                "Статус": ["Connected", "Connected", "Degraded", "Connected"],
                "Событий за час": [1840, 920, 312, 1188],
            }
        )
        st.dataframe(integrations, hide_index=True, width="stretch")

    with tabs[3]:
        st.progress(0.84, text="84% сценариев прошли ночной контроль")
        st.progress(0.62, text="62% базы покрыто автоклассификацией")


apply_admin_theme()

overview_page = st.Page(overview, title="Обзор", icon=":material/dashboard:", default=True)
users_page = st.Page("pages/admin_users.py", title="Пользователи", icon=":material/groups:")
security_page = st.Page("pages/admin_security.py", title="Безопасность", icon=":material/shield_lock:")
reports_page = st.Page("pages/admin_reports.py", title="Отчеты", icon=":material/analytics:")

pg = st.navigation(
    {
        "Рабочая область": [overview_page],
        "Администрирование": [users_page, security_page, reports_page],
    }
)

with st.sidebar:
    st.markdown("### Glossy Admin")
    st.caption("Операционная панель на Streamlit 1.57.0")
    st.divider()
    environment = st.selectbox("Среда", ["Production", "Staging", "Sandbox"], index=0)
    st.toggle("Тихий режим", value=True)
    st.divider()
    st.caption(f"Активная среда: {environment}")

pg.run()
