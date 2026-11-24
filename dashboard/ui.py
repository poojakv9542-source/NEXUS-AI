
import sys
import html
import math
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
import json
import urllib.request
import urllib.error
import urllib.parse

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.agent import NexusAgent
from app.memory import NexusMemory
# ============================================================
# FASTAPI BACKEND CONNECTION
# ============================================================

API_URL = "http://127.0.0.1:8000"


def api_request(endpoint, method="GET", params=None, payload=None):
    url = f"{API_URL}{endpoint}"

    if params:
        url += "?" + urllib.parse.urlencode(params)

    data = None
    headers = {}

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as error:
        try:
            detail = json.loads(error.read().decode("utf-8"))
        except Exception:
            detail = str(error)
        raise RuntimeError(f"Backend error {error.code}: {detail}")

    except Exception as error:
        raise RuntimeError(f"Cannot connect to NEXUS backend: {error}")


# ============================================================
# PAGE + DATABASE
# ============================================================

st.set_page_config(
    page_title="NEXUS AI | Command Center",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_tasks():
    """Read the existing local SQLite task database; never recreate or erase it."""
    memory = NexusMemory()
    try:
        return memory.get_all_tasks()
    finally:
        memory.close()


tasks = load_tasks()

total = len(tasks)
completed = sum(t.get("status") == "COMPLETED" for t in tasks)
running = sum(t.get("status") == "RUNNING" for t in tasks)
pending = sum(t.get("status") == "PENDING" for t in tasks)

awaiting_approval = sum(
    t.get("status") == "AWAITING_APPROVAL" for t in tasks
)
failed = sum(t.get("status") == "FAILED" for t in tasks)


# ============================================================
# HELPERS
# ============================================================

def safe_text(value):
    return html.escape(str(value if value is not None else ""))


def status_class(status):
    return {
        "COMPLETED": "green",
        "RUNNING": "blue",
        "PENDING": "yellow",
        "AWAITING_APPROVAL": "yellow",
        "FAILED": "red",
    }.get(status, "blue")


def task_created_date(task):
    raw = str(task.get("created_at", ""))
    try:
        return datetime.fromisoformat(raw[:19]).date()
    except (ValueError, TypeError):
        try:
            return datetime.strptime(raw[:10], "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return None


def make_line_chart_svg(labels, created_values, completed_values):
    """Create a responsive SVG chart using actual task counts."""
    width, height = 760, 230
    left, right, top, bottom = 48, 12, 18, 42
    plot_w = width - left - right
    plot_h = height - top - bottom
    max_value = max([1] + created_values + completed_values)
    max_value = max(5, math.ceil(max_value / 5) * 5)

    def point(index, value):
        x = left + (plot_w * index / max(1, len(labels) - 1))
        y = top + plot_h - (value / max_value * plot_h)
        return x, y

    def path_for(values):
        coords = [point(i, v) for i, v in enumerate(values)]
        return " ".join(
            ("M" if i == 0 else "L") + f" {x:.1f},{y:.1f}"
            for i, (x, y) in enumerate(coords)
        )

    grid = []
    for tick in range(5):
        value = max_value * tick / 4
        y = top + plot_h - (plot_h * tick / 4)
        grid.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" class="gridline"/>'
            f'<text x="{left-12}" y="{y+4:.1f}" text-anchor="end" class="axis">{int(value)}</text>'
        )

    xlabels = []
    dots = []
    for i, label in enumerate(labels):
        x, y1 = point(i, created_values[i])
        _, y2 = point(i, completed_values[i])
        xlabels.append(
            f'<text x="{x:.1f}" y="{height-12}" text-anchor="middle" class="axis">{safe_text(label)}</text>'
        )
        dots.append(
            f'<circle cx="{x:.1f}" cy="{y1:.1f}" r="4.5" class="dot-blue"/>'
            f'<circle cx="{x:.1f}" cy="{y2:.1f}" r="4.5" class="dot-green"/>'
        )

    created_path = path_for(created_values)
    completed_path = path_for(completed_values)

    return f"""
    <svg viewBox="0 0 {width} {height}" role="img" aria-label="Daily tasks created and completed">
      <style>
        .gridline{{stroke:#263957;stroke-width:1}}
        .axis{{fill:#9aaccb;font:12px Inter,Arial,sans-serif}}
        .line-blue{{fill:none;stroke:#278bff;stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round}}
        .line-green{{fill:none;stroke:#35d0a3;stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round}}
        .dot-blue{{fill:#278bff;stroke:#d8eaff;stroke-width:1}}
        .dot-green{{fill:#35d0a3;stroke:#d8fff2;stroke-width:1}}
      </style>
      {''.join(grid)}
      <path d="{created_path}" class="line-blue"/>
      <path d="{completed_path}" class="line-green"/>
      {''.join(dots)}
      {''.join(xlabels)}
    </svg>
    """



def make_donut():
    values = [completed, running, pending, awaiting_approval, failed]

    colors = [
        "#35cfa2",
        "#8c70ed",
        "#278bff",
        "#f5ae45",
        "#f06470"
    ]

    total_value = sum(values)

    if total_value == 0:
        background = "conic-gradient(#263957 0deg 360deg)"
    else:
        stops = []
        current = 0.0

        for value, color in zip(values, colors):
            next_value = current + (value / total_value * 360)
            stops.append(f"{color} {current:.2f}deg {next_value:.2f}deg")
            current = next_value

        background = "conic-gradient(" + ", ".join(stops) + ")"

    labels = [
        ("Completed", completed, colors[0]),
        ("Running", running, colors[1]),
        ("Pending", pending, colors[2]),
        ("Awaiting approval", awaiting_approval, colors[3]),
        ("Failed", failed, colors[4])
    ]

    legend = ""

    for label, value, color in labels:
        percent = (value / total_value * 100) if total_value > 0 else 0

        legend += (
            '<div class="legend-row">'
            '<span class="legend-left">'
            f'<i style="background:{color}"></i>{label}'
            '</span>'
            f'<strong>{percent:.1f}%</strong>'
            '</div>'
        )

    return f"""
    <div class="donut-layout">
        <div class="donut" style="background:{background}">
            <div class="donut-hole">
                <strong>{total_value:,}</strong>
                <span>Total Tasks</span>
            </div>
        </div>
        <div class="legend">{legend}</div>
    </div>
    """
# ============================================================
# DESIGN SYSTEM
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #071226;
    --panel: #0d1d38;
    --panel2: #102442;
    --border: #203b63;
    --muted: #91a7ca;
    --text: #eef4ff;
    --blue: #278bff;
    --green: #35cfa2;
}
* { font-family: Inter, sans-serif; }
.stApp {
    background:
      radial-gradient(ellipse at 68% 0%, rgba(20,74,155,.30), transparent 42%),
      linear-gradient(125deg,#071226 0%,#08152b 55%,#071226 100%);
    color: var(--text);
}
header[data-testid="stHeader"] { background: transparent; }
.block-container {
    max-width: 1720px;
    padding: 1.35rem 2rem 2.5rem;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0d1b35 0%,#08152b 100%);
    border-right: 1px solid #1e365c;
}
section[data-testid="stSidebar"] * { color: #dce8ff; }
section[data-testid="stSidebar"] hr { border-color: #233b60; }
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #9db1d2;
}
.brand {font-size:25px;font-weight:800;letter-spacing:-.8px;color:#fff;}
.brand span {color:#55a5ff;}
.brand-mark {
    display:inline-flex;align-items:center;justify-content:center;
    width:42px;height:42px;border-radius:13px;
    color:#fff;font-size:25px;margin-bottom:10px;
    background:linear-gradient(145deg,#176bdc,#203d92);
    box-shadow:0 0 25px #267cff55;
}
.brand-sub {color:#839bc1;font-size:9px;letter-spacing:1.7px;margin-top:5px;}
.side-caption {font-size:10px;letter-spacing:1.5px;color:#7088ae;font-weight:700;}
.side-status {font-size:11px;padding:8px 0;color:#8fa8ca;}
.side-status .ok {color:#35d0a3;}
.side-status .wait {color:#f4bd5d;}
.topline {color:#86a0c7;font-size:10px;letter-spacing:2px;font-weight:700;}
.page-title {color:#f5f8ff;font-size:31px;font-weight:800;letter-spacing:-1px;margin-top:5px;}
.page-subtitle {color:#9aafd0;font-size:12px;margin-top:4px;}
.live-pill {
    display:inline-flex;align-items:center;gap:7px;
    color:#49ddb0;font-size:11px;font-weight:700;
}
.live-dot {width:8px;height:8px;border-radius:50%;background:#35d0a3;display:inline-block;box-shadow:0 0 10px #35d0a3;}
.kpi {
    min-height:112px;padding:17px 18px;border-radius:13px;
    background:linear-gradient(145deg,rgba(19,39,70,.98),rgba(12,26,48,.98));
    border:1px solid #24436d;position:relative;overflow:hidden;
}
.kpi:after {
    content:"";position:absolute;width:110px;height:70px;right:-15px;bottom:-42px;
    border-radius:50%;filter:blur(24px);background:#287cff55;
}
.kpi-label {color:#a7bad9;font-size:11px;font-weight:600;}
.kpi-value {color:#fff;font-size:29px;font-weight:800;margin-top:9px;line-height:1.1;}
.kpi-note {color:#5cdbb0;font-size:10px;margin-top:7px;}
.kpi-icon {
    float:right;width:37px;height:37px;border-radius:11px;
    display:flex;align-items:center;justify-content:center;font-size:19px;
    background:#1b4c8c;color:#70b8ff;
}
.panel {
    background:linear-gradient(145deg,rgba(17,36,66,.97),rgba(10,25,47,.97));
    border:1px solid #24416b;border-radius:13px;padding:17px 18px;
    box-shadow:0 8px 28px rgba(0,0,0,.12);
}
.panel-title {color:#f0f5ff;font-size:14px;font-weight:700;}
.panel-subtitle {color:#8fa6ca;font-size:10px;margin-top:4px;}
.chart-legend {display:flex;gap:18px;justify-content:flex-end;margin:0 0 3px;color:#c7d6ef;font-size:10px;}
.legend-key {display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;}
.donut-layout {display:flex;align-items:center;justify-content:space-around;gap:18px;padding:20px 4px 10px;min-height:230px;}
.donut {
    width:174px;height:174px;border-radius:50%;display:flex;align-items:center;justify-content:center;
    flex-shrink:0;box-shadow:0 0 28px #0005;
}
.donut-hole {
    width:116px;height:116px;border-radius:50%;background:#0b1a32;
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    border:1px solid #233c61;
}
.donut-hole strong {font-size:22px;color:white;}
.donut-hole span {font-size:10px;color:#9db0cf;margin-top:2px;}
.legend {min-width:150px;flex:1;}
.legend-row {display:flex;justify-content:space-between;align-items:center;gap:10px;padding:9px 0;border-bottom:1px solid #233957;color:#c8d7ef;font-size:11px;}
.legend-row:last-child {border-bottom:0;}
.legend-left {display:flex;align-items:center;gap:8px;}
.legend-left i {width:9px;height:9px;border-radius:50%;display:inline-block;}
.legend-row strong {color:#f2f6ff;font-size:11px;}
.pipeline-row {margin:15px 0;}
.pipeline-head {display:flex;justify-content:space-between;color:#c7d6ed;font-size:11px;margin-bottom:7px;}
.pipeline-track {height:8px;background:#243957;border-radius:20px;overflow:hidden;}
.pipeline-fill {height:100%;border-radius:20px;}
.activity {padding:11px 0;border-bottom:1px solid #233957;}
.activity:last-child {border-bottom:0;}
.activity-name {color:#e8efff;font-size:11px;font-weight:600;overflow-wrap:anywhere;}
.activity-meta {color:#839abd;font-size:10px;margin-top:4px;}
.pill {display:inline-block;border-radius:20px;padding:4px 9px;font-size:9px;font-weight:700;}
.green {background:#123c34;color:#6de2b5;}
.blue {background:#193963;color:#91c5ff;}
.yellow {background:#44371c;color:#f5d17b;}
.red {background:#481f2c;color:#ff9cac;}
.stTextInput input,.stTextArea textarea {
    background:#101f39!important;color:white!important;
    border:1px solid #304a70!important;border-radius:8px!important;
}
.stTextInput label,.stTextArea label {color:#cbd9f3!important;}
.stButton button,.stFormSubmitButton button {
    background:linear-gradient(110deg,#2878ed,#6250e9);
    color:white!important;border:1px solid #5279d9;border-radius:8px;font-weight:700;
}
.stButton button:hover,.stFormSubmitButton button:hover {
    box-shadow:0 0 17px #3679e977;border-color:#8db6ff;
}
div[role="radiogroup"] label {background:transparent;border-radius:8px;padding:8px 10px;}
div[role="radiogroup"] label:hover {background:#1a2e53;}
.footer {text-align:center;color:#637b9f;font-size:10px;padding-top:28px;}
div[data-testid="stAlert"] {border-radius:10px;}
@media(max-width:900px) {
    .block-container {padding:1rem 1rem 2rem;}
    .donut-layout {flex-wrap:wrap;}
}
.donut-layout {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 30px;
}

.donut {
    width: 170px;
    height: 170px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.donut-hole {
    width: 110px;
    height: 110px;
    background: #101b2d;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.legend {
    flex: 1;
}

.legend-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;
    color: white;
}

.legend-left {
    display: flex;
    align-items: center;
    gap: 8px;
}

.legend-left i {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("""
    <div class="brand-mark">◈</div>
    <div class="brand">NEXUS <span>AI</span></div>
    <div class="brand-sub">INTELLIGENT DIGITAL EMPLOYEE</div>
    """, unsafe_allow_html=True)

    st.write("")
    st.divider()
    st.markdown('<div class="side-caption">WORKSPACE</div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
    "Overview",
    "AI Employee",
    "My Tasks",
    "File Management",
    "Approval Center",
    "Reports"
],
        label_visibility="collapsed",
        format_func=lambda x: {
            "File Management": "▣   File Management",
            "Overview": "⌂   Overview",
            "AI Employee": "✦   AI Employee",
            "My Tasks": "▤   My Tasks",
            "Approval Center": "◇   Approvals",
            "Reports": "▧   Reports",
        }[x],
    )

    st.divider()
    st.markdown('<div class="side-caption">SYSTEM STATUS</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="side-status"><span class="ok">●</span> Local Workspace Active</div>
    <div class="side-status"><span class="ok">●</span> SQLite Database Connected</div>
    <div class="side-status"><span class="wait">◉</span> Ollama Integration Pending</div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div style="font-size:11px;color:#8298bc;text-align:center;line-height:1.8">
        ◈ NEXUS AI<br>VERSION 0.3<br>
        <span style="font-size:9px">INTELLIGENT DIGITAL WORKFORCE</span>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# TOP BAR
# ============================================================

top_left, top_right = st.columns([3, 2])
with top_left:
    st.markdown('<div class="topline">NEXUS / COMMAND CENTER</div>', unsafe_allow_html=True)
with top_right:
    search = st.text_input(
        "Search tasks",
        placeholder="⌕  Search employee tasks...",
        label_visibility="collapsed",
    )


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":
    heading_left, heading_right = st.columns([4, 1])
    with heading_left:
        st.markdown('<div class="page-title">Workforce Dashboard</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="page-subtitle">Real-time insights into your task activity and workforce operations.</div>',
            unsafe_allow_html=True,
        )
    with heading_right:
        st.markdown(
            '<div style="text-align:right;padding-top:16px"><span class="live-pill"><i class="live-dot"></i> Local data</span></div>',
            unsafe_allow_html=True,
        )

    st.write("")

    # KPI cards - values come from the existing SQLite database.
    kpis = [
        ("TOTAL TASKS", total, "All recorded tasks", "▤"),
        ("COMPLETED TASKS", completed, "Successfully completed", "✓"),
        ("RUNNING TASKS", running, "Currently executing", "▷"),
        ("PENDING REVIEW", pending, "Waiting for attention", "◷"),
    ]
    cols = st.columns(4)
    for col, (label, value, note, icon) in zip(cols, kpis):
        with col:
            st.markdown(f"""
            <div class="kpi">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value:,}</div>
                <div class="kpi-note">✦ {note}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    # Build actual daily created/completed series for the last seven days.
    dates = [datetime.now().date() - timedelta(days=i) for i in range(6, -1, -1)]
    created_values = []
    completed_values = []
    for day in dates:
        created_values.append(sum(1 for t in tasks if task_created_date(t) == day))
        completed_values.append(
            sum(
                1 for t in tasks
                if t.get("status") == "COMPLETED"
                and str(t.get("updated_at", ""))[:10] == day.isoformat()
            )
        )
    day_labels = [d.strftime("%a") for d in dates]

    left, right = st.columns([1.35, 1], gap="medium")
    with left:
        st.markdown("""
        <div class="panel">
          <div class="panel-title">Daily Task Performance</div>
          <div class="panel-subtitle">Tasks created versus tasks completed · last seven days</div>
          <div style="height:12px"></div>
          <div class="chart-legend">
            <span><i class="legend-key" style="background:#278bff"></i>Created</span>
            <span><i class="legend-key" style="background:#35cfa2"></i>Completed</span>
          </div>
        """, unsafe_allow_html=True)
        st.markdown(
            make_line_chart_svg(day_labels, created_values, completed_values),
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="panel">
          <div class="panel-title">Workforce Task Distribution</div>
          <div class="panel-subtitle">Current status of recorded tasks</div>
        """, unsafe_allow_html=True)
        st.markdown(
    make_donut(),
    unsafe_allow_html=True
)
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # Lower dashboard panels.
    a, b = st.columns([1, 1.15], gap="medium")

    with a:
        st.markdown("""
        <div class="panel">
          <div class="panel-title">Execution Pipeline</div>
          <div class="panel-subtitle">Task workflow status</div>
        """, unsafe_allow_html=True)

        stages = [
            ("Submitted", total, "#278bff"),
            ("Running", running, "#8c70ed"),
            ("Completed", completed, "#35cfa2"),
            ("Needs review", pending, "#f5ae45"),
        ]
        maximum = max(total, 1)
        for label, value, color in stages:
            width = max(0, min(100, value / maximum * 100))
            st.markdown(f"""
            <div class="pipeline-row">
              <div class="pipeline-head"><span>{label}</span><strong>{value:,}</strong></div>
              <div class="pipeline-track"><div class="pipeline-fill" style="width:{width:.1f}%;background:{color}"></div></div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="panel">
          <div class="panel-title">Recent Employee Activity</div>
          <div class="panel-subtitle">Latest instructions received by NEXUS</div>
        """, unsafe_allow_html=True)

        if tasks:
            for task in tasks[:5]:
                instruction = safe_text(str(task.get("instruction", ""))[:75])
                status = safe_text(task.get("status", "UNKNOWN"))
                css = status_class(task.get("status", ""))
                task_id = safe_text(task.get("task_id", ""))
                st.markdown(f"""
                <div class="activity">
                  <div style="display:flex;justify-content:space-between;gap:10px;align-items:center">
                    <div class="activity-name">◈ {instruction}</div>
                    <span class="pill {css}">{status.replace("_", " ")}</span>
                  </div>
                  <div class="activity-meta">Task #{task_id}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="activity-meta" style="padding:20px 0">No employee activity yet. Assign a task to NEXUS to get started.</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("### Tasks Requiring Attention")
    attention = [t for t in tasks if t.get("status") in ("AWAITING_APPROVAL", "FAILED")]
    if attention:
        for task in attention[:5]:
            st.warning(
                f"Task #{task.get('task_id')} — {task.get('instruction', '')} ({task.get('status')})"
            )
    else:
        st.success("No failed or review-pending tasks.")


# ============================================================
# AI EMPLOYEE
# ============================================================

elif page == "AI Employee":
    st.markdown('<div class="page-title">NEXUS AI Employee</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Assign work to your intelligent digital employee.</div>', unsafe_allow_html=True)
    st.write("")

    with st.container(border=True):
        st.markdown("### New Employee Assignment")
        with st.form("nexus_assignment"):
            instruction = st.text_area(
                "Assigned Task",
                placeholder="Tell NEXUS what work needs to be done...",
                height=150,
            )
            submit = st.form_submit_button("✦ Assign to NEXUS", use_container_width=True)

        if submit:
            if not instruction.strip():
                st.warning("Please enter an instruction.")
            else:
                agent = NexusAgent()
                try:
                    with st.spinner("NEXUS is processing your assignment..."):
                        result = agent.process_instruction(instruction.strip())
                    st.success(f"Task #{result['task_id']} recorded successfully.")
                    st.write("**Objective:**", result["objective"])
                    st.write("**Status:**", result["status"])
                    for item in result["execution_results"]:
                        st.write(item)
                except Exception as error:
                    st.error(str(error))
                finally:
                    agent.close()
                st.rerun()


# ============================================================
# MY TASKS
# ============================================================

elif page == "My Tasks":
    st.markdown('<div class="page-title">My Tasks</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">All employee assignments and their current status.</div>', unsafe_allow_html=True)

    filtered = [
        t for t in tasks
        if search.lower() in str(t.get("instruction", "")).lower()
    ]
    if filtered:
        for task in filtered:
            with st.container(border=True):
                st.markdown(f"**Task #{task.get('task_id')}**")
                st.write(task.get("instruction", ""))
                st.caption(
                    f"Status: {task.get('status')} · Created: {task.get('created_at')}"
                )
                if task.get("error"):
                    st.error(task["error"])
    else:
        st.info("No tasks match your search." if search else "No tasks have been assigned yet.")

# ============================================================
# FILE MANAGEMENT
# ============================================================

elif page == "File Management":
    st.markdown(
        '<div class="page-title">File Management</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-subtitle">Manage files in your NEXUS workspace.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    folder = st.text_input(
        "Workspace folder",
        value="sample_docs",
        help="Enter a folder relative to the NEXUS workspace."
    )

    # List workspace files
    st.markdown("### Workspace Files")

    if st.button("↻ Refresh file list"):
        st.rerun()

    try:
        file_data = api_request(
            "/files/list",
            params={"folder": folder}
        )

        st.caption(
            f"{file_data['count']} items in {file_data['folder']}"
        )

        if file_data["items"]:
            st.dataframe(
                [
                    {
                        "Name": item["name"],
                        "Type": item["type"],
                        "Size (bytes)": item["size_bytes"],
                        "Path": item["relative_path"]
                    }
                    for item in file_data["items"]
                ],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("This folder is empty.")

    except Exception as error:
        st.error(str(error))

    st.divider()

    # File operations
    read_tab, find_tab, duplicate_tab, organize_tab, rename_tab, summary_tab = st.tabs(
        [
            "Read File",
            "Find File",
            "Duplicates",
            "Organize",
            "Rename",
            "Summarize"
        ]
    )

    with read_tab:
        st.markdown("#### Read a document")

        read_path = st.text_input(
            "File path",
            placeholder="sample_docs/employee_weekly_report.txt",
            key="read_path"
        )

        if st.button("Read Document"):
            if not read_path.strip():
                st.warning("Enter a file path.")
            else:
                try:
                    result = api_request(
                        "/files/read",
                        params={"path": read_path.strip()}
                    )
                    st.text_area(
                        "Document contents",
                        value=result["content"],
                        height=300
                    )
                except Exception as error:
                    st.error(str(error))

    with find_tab:
        st.markdown("#### Search workspace files")

        search_name = st.text_input(
            "File name or part of the name",
            key="find_name"
        )

        if st.button("Search Files"):
            if not search_name.strip():
                st.warning("Enter a filename to search.")
            else:
                try:
                    result = api_request(
                        "/files/find",
                        params={
                            "name": search_name.strip(),
                            "folder": folder
                        }
                    )

                    st.write(f"Found {result['count']} matching files.")

                    for match in result["matches"]:
                        st.write("📄", match)

                except Exception as error:
                    st.error(str(error))

    with duplicate_tab:
        st.markdown("#### Detect duplicate files")

        if st.button("Scan for Duplicates"):
            try:
                result = api_request(
                    "/files/duplicates",
                    params={"folder": folder}
                )

                if result["duplicate_groups"] == 0:
                    st.success("No duplicate files found.")
                else:
                    st.warning(
                        f"Found {result['duplicate_groups']} duplicate groups."
                    )

                    for group in result["duplicates"]:
                        st.write("Matching files:")
                        for filename in group["files"]:
                            st.write("•", filename)

            except Exception as error:
                st.error(str(error))

    with organize_tab:
        st.markdown("#### Move a file to another folder")

        move_source = st.text_input(
            "Source file path",
            key="move_source"
        )

        move_destination = st.text_input(
            "Destination folder",
            key="move_destination"
        )

        if st.button("Preview Move"):
            if not move_source.strip() or not move_destination.strip():
                st.warning("Enter both paths.")
            else:
                try:
                    result = api_request(
                        "/files/organize",
                        method="POST",
                        payload={
                            "source": move_source.strip(),
                            "destination_folder": move_destination.strip(),
                            "confirm": False
                        }
                    )

                    st.session_state["move_preview"] = result
                    st.info(result["message"])

                except Exception as error:
                    st.error(str(error))

        if st.session_state.get("move_preview"):
            preview = st.session_state["move_preview"]

            st.write(f"From: {preview['from']}")
            st.write(f"To: {preview['to']}")

            if st.button("Confirm and Move File"):
                try:
                    result = api_request(
                        "/files/organize",
                        method="POST",
                        payload={
                            "source": move_source.strip(),
                            "destination_folder": move_destination.strip(),
                            "confirm": True
                        }
                    )

                    st.success(result["moved_to"])
                    st.session_state.pop("move_preview", None)
                    st.rerun()

                except Exception as error:
                    st.error(str(error))

    with rename_tab:
        st.markdown("#### Rename a file")

        rename_path = st.text_input(
            "Existing file path",
            key="rename_path"
        )

        new_name = st.text_input(
            "New filename (include extension)",
            key="new_filename"
        )

        if st.button("Preview Rename"):
            if not rename_path.strip() or not new_name.strip():
                st.warning("Enter both the existing path and new filename.")
            else:
                try:
                    result = api_request(
                        "/files/rename",
                        method="POST",
                        payload={
                            "path": rename_path.strip(),
                            "new_name": new_name.strip(),
                            "confirm": False
                        }
                    )

                    st.session_state["rename_preview"] = result
                    st.info(result["message"])

                except Exception as error:
                    st.error(str(error))

        if st.session_state.get("rename_preview"):
            preview = st.session_state["rename_preview"]

            st.write(f"From: {preview['from']}")
            st.write(f"To: {preview['to']}")

            if st.button("Confirm and Rename"):
                try:
                    result = api_request(
                        "/files/rename",
                        method="POST",
                        payload={
                            "path": rename_path.strip(),
                            "new_name": new_name.strip(),
                            "confirm": True
                        }
                    )

                    st.success(result["renamed_to"])
                    st.session_state.pop("rename_preview", None)
                    st.rerun()

                except Exception as error:
                    st.error(str(error))

    with summary_tab:
        st.markdown("#### Generate a document summary")

        summary_path = st.text_input(
            "Document path",
            key="summary_path"
        )

        if st.button("Summarize Document"):
            if not summary_path.strip():
                st.warning("Enter a document path.")
            else:
                try:
                    result = api_request(
                        "/files/summarize",
                        method="POST",
                        payload={"path": summary_path.strip()}
                    )

                    st.write("**Summary**")
                    st.write(result["summary"])
                    st.caption(
                        f"Method: {result['method']} · {result['note']}"
                    )

                except Exception as error:
                    st.error(str(error))


# ============================================================
# APPROVAL CENTER
# ============================================================

elif page == "Approval Center":
    st.markdown('<div class="page-title">Approval Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Review tasks awaiting employee approval.</div>', unsafe_allow_html=True)

    approval_tasks = [t for t in tasks if t.get("status") == "AWAITING_APPROVAL"]
    if approval_tasks:
        for task in approval_tasks:
            with st.container(border=True):
                st.markdown(f"**Task #{task.get('task_id')}**")
                st.write(task.get("instruction", ""))
                st.warning("Awaiting employee review.")
        st.info(
            "Approval controls are not enabled yet. "
            "No task can be approved from this screen."
        )
    else:
        st.success("No pending approvals.")


# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":
    st.markdown('<div class="page-title">Reports Workspace</div>', unsafe_allow_html=True)
    report_dir = BASE_DIR / "reports"
    report_dir.mkdir(exist_ok=True)
    report_files = [f for f in report_dir.iterdir() if f.is_file()]

    if report_files:
        for file in report_files:
            st.write(f"▧ {file.name}")
    else:
        st.info("No generated reports are available yet.")


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
  ◈ NEXUS AI &nbsp; | &nbsp; INTELLIGENT DIGITAL WORKFORCE &nbsp; | &nbsp; LOCAL-FIRST AI PLATFORM
</div>
""", unsafe_allow_html=True)
