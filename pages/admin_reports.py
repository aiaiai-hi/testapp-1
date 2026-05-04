import pandas as pd
import streamlit as st

from ui_shared import apply_admin_theme, render_hero, sample_audit_log, sample_timeseries, section_title


apply_admin_theme()

render_hero(
    "Отчеты и аудит",
    "Готовые управленческие срезы, журнал действий, расписания экспорта и контроль качества данных.",
    "Администрирование",
)

tabs = st.tabs(["Дашборды", "Журнал", "Экспорты", "Качество данных"])

with tabs[0]:
    data = sample_timeseries()
    col_a, col_b = st.columns([1.4, 1], gap="large")
    with col_a:
        section_title("SLA по дням")
        st.bar_chart(data.set_index("День")[["SLA"]], height=300, width="stretch")
    with col_b:
        section_title("Параметры отчета")
        st.date_input("Период", value=None)
        st.selectbox("Сегмент", ["Все клиенты", "Enterprise", "SMB", "Trial"])
        st.multiselect("Метрики", ["SLA", "Ошибки", "Выручка", "Активность"], default=["SLA", "Ошибки"])
        st.button("Обновить", icon=":material/refresh:", type="primary")

with tabs[1]:
    st.dataframe(sample_audit_log(), hide_index=True, width="stretch")

with tabs[2]:
    exports = pd.DataFrame(
        {
            "Отчет": ["Weekly SLA", "Finance close", "Access review", "Usage pulse"],
            "Расписание": ["Пн 09:00", "1 число", "Пт 18:00", "Ежедневно"],
            "Получатели": [8, 4, 3, 12],
            "Формат": ["PDF", "XLSX", "CSV", "PDF"],
        }
    )
    st.dataframe(exports, hide_index=True, width="stretch")

with tabs[3]:
    checks = pd.DataFrame(
        {
            "Проверка": ["Дубликаты клиентов", "Пустые SLA", "Ошибки валют", "Сломанные webhooks"],
            "Статус": ["Passed", "Passed", "Warning", "Passed"],
            "Покрытие": ["100%", "99.8%", "96.2%", "100%"],
        }
    )
    st.dataframe(checks, hide_index=True, width="stretch")
    st.progress(0.962, text="96.2% качества данных по последнему прогону")
