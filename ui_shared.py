from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd
import streamlit as st


@dataclass(frozen=True)
class StatCard:
    label: str
    value: str
    delta: str
    tone: str = "neutral"


def apply_admin_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #f6f7fb;
            --panel: #ffffff;
            --ink: #111827;
            --muted: #667085;
            --line: #e5e7eb;
            --accent: #0f766e;
            --accent-soft: #d9f4ef;
            --blue: #2563eb;
            --amber: #b45309;
            --rose: #be123c;
        }

        .stApp {
            background:
                linear-gradient(180deg, rgba(246,247,251,0.95), rgba(246,247,251,1)),
                radial-gradient(circle at 75% -10%, rgba(15,118,110,0.12), transparent 30%);
            color: var(--ink);
        }

        [data-testid="stSidebar"] {
            background: #0f172a;
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        [data-testid="stSidebar"] * {
            color: #e5e7eb;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #cbd5e1;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1280px;
        }

        h1, h2, h3 {
            letter-spacing: 0;
        }

        .hero {
            padding: 26px 28px;
            border: 1px solid var(--line);
            border-radius: 8px;
            background:
                linear-gradient(135deg, rgba(255,255,255,0.98), rgba(238,246,255,0.92)),
                linear-gradient(90deg, rgba(15,118,110,0.10), rgba(37,99,235,0.08));
            box-shadow: 0 18px 50px rgba(15, 23, 42, 0.08);
            margin-bottom: 20px;
        }

        .eyebrow {
            color: var(--accent);
            font-weight: 700;
            font-size: 0.82rem;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .hero-title {
            color: var(--ink);
            font-size: clamp(2rem, 5vw, 4rem);
            font-weight: 800;
            line-height: 1;
            margin: 0 0 10px 0;
        }

        .hero-copy {
            color: var(--muted);
            max-width: 780px;
            font-size: 1.02rem;
            line-height: 1.6;
            margin: 0;
        }

        .stat-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
            margin: 10px 0 18px;
        }

        .stat-card {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 16px;
            min-height: 122px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
        }

        .stat-card .label {
            color: var(--muted);
            font-size: 0.86rem;
            margin-bottom: 14px;
        }

        .stat-card .value {
            color: var(--ink);
            font-size: 2rem;
            line-height: 1;
            font-weight: 800;
        }

        .delta {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            margin-top: 12px;
            padding: 4px 8px;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
        }

        .delta.good { background: #dcfce7; color: #166534; }
        .delta.warn { background: #fef3c7; color: #92400e; }
        .delta.bad { background: #ffe4e6; color: #9f1239; }
        .delta.neutral { background: #e0f2fe; color: #075985; }

        .section-title {
            font-weight: 800;
            font-size: 1.2rem;
            margin: 8px 0 10px;
        }

        .pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 8px 0 2px;
        }

        .pill {
            border: 1px solid var(--line);
            background: #fff;
            color: #344054;
            border-radius: 999px;
            padding: 6px 10px;
            font-size: 0.82rem;
            font-weight: 650;
        }

        .pill.ok { border-color: #bbf7d0; background: #f0fdf4; color: #166534; }
        .pill.alert { border-color: #fecdd3; background: #fff1f2; color: #9f1239; }
        .pill.info { border-color: #bfdbfe; background: #eff6ff; color: #1d4ed8; }

        .timeline {
            border-left: 2px solid #dbeafe;
            padding-left: 16px;
            margin-top: 10px;
        }

        .timeline-item {
            background: #fff;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 12px 14px;
            margin: 0 0 10px 0;
        }

        .timeline-item b {
            color: var(--ink);
        }

        .timeline-item span {
            color: var(--muted);
            font-size: 0.86rem;
        }

        div[data-testid="stMetric"] {
            background: #fff;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 14px 16px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
        }

        button[kind="primary"] {
            border-radius: 8px;
            background: var(--accent);
            border: 1px solid var(--accent);
        }

        @media (max-width: 900px) {
            .stat-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
            .hero {
                padding: 22px;
            }
        }

        @media (max-width: 520px) {
            .stat-grid {
                grid-template-columns: 1fr;
            }
            .hero-title {
                font-size: 2.15rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(title: str, copy: str, eyebrow: str = "Control Center") -> None:
    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">{eyebrow}</div>
            <div class="hero-title">{title}</div>
            <p class="hero-copy">{copy}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stat_grid(cards: Iterable[StatCard]) -> None:
    cards = list(cards)
    columns = st.columns(len(cards))
    delta_colors = {
        "good": "normal",
        "warn": "off",
        "bad": "inverse",
        "neutral": "off",
    }

    for column, card in zip(columns, cards):
        column.metric(
            label=card.label,
            value=card.value,
            delta=card.delta,
            delta_color=delta_colors.get(card.tone, "off"),
            border=True,
        )


def render_pills(items: Iterable[tuple[str, str]]) -> None:
    html = ['<div class="pill-row">']
    for label, tone in items:
        html.append(f'<span class="pill {tone}">{label}</span>')
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def section_title(label: str) -> None:
    st.markdown(f'<div class="section-title">{label}</div>', unsafe_allow_html=True)


def sample_timeseries() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "День": ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
            "Заявки": [124, 140, 132, 169, 181, 156, 198],
            "SLA": [97.2, 96.8, 98.1, 97.4, 98.7, 99.0, 98.4],
            "Ошибки": [7, 5, 6, 4, 3, 5, 2],
        }
    )


def sample_users() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Пользователь": ["Анна Смирнова", "Илья Орлов", "Мария Волкова", "Тимур Алиев", "Олег Ким"],
            "Роль": ["Owner", "Admin", "Analyst", "Support", "Auditor"],
            "Статус": ["Active", "Active", "Invite sent", "Active", "Suspended"],
            "Последний вход": ["Сегодня, 10:42", "Сегодня, 09:15", "Вчера, 18:10", "3 мая, 13:08", "28 апреля, 11:22"],
            "Риск": ["Low", "Low", "Medium", "Low", "High"],
        }
    )


def sample_audit_log() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Время": ["10:42", "10:18", "09:57", "09:20", "08:48", "08:15"],
            "Событие": [
                "Обновлена политика доступа",
                "Создана группа Finance",
                "Экспортирован отчет SLA",
                "Сработал MFA challenge",
                "Изменены лимиты API",
                "Подключен новый источник",
            ],
            "Исполнитель": ["Ilya", "Anna", "Maria", "Timur", "Anna", "System"],
            "Серьезность": ["Info", "Info", "Info", "Warning", "Info", "Info"],
        }
    )
