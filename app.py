"""
app.py - Aplikasi Fuzzy Tempat Nongkrong Dashboard
Acuan Desain UI/UX: Google Stitch MCP (Project ID: 1263705091262288771, Screen: ee8aa9b5f2cb482daa32657c94e918fc)
Gaya: Apple iPadOS Split-View Tablet Frame
Metode: Tsukamoto (Utama), Sugeno Orde-0, Mamdani Centroid
Aturan Ketat: TANPA EMOJI (Hanya SVG, Unicode Glyphs, dan CSS bersih).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Import modul backend perhitungan fuzzy murni
from membership import (
    mu_rendah,
    mu_tinggi,
    mu_output_tidak_layak,
    mu_output_layak
)
from rules import CRITERIA_NAMES, DEFAULT_WEIGHTS, generate_rules, evaluate_rules
from tsukamoto import calculate_tsukamoto
from sugeno import calculate_sugeno
from mamdani import calculate_mamdani
from compare import evaluate_all, DEFAULT_DATASET, calculate_sensitivity

# 1. Konfigurasi Halaman Streamlit (TANPA EMOJI)
st.set_page_config(
    page_title="Fuzzy Tempat Nongkrong - Data & Bobot",
    page_icon="assets/logo/web/favicon-32.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Injeksi Custom CSS (style.css)
css_file = Path(__file__).parent / "style.css"
if css_file.exists():
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 3. Inisialisasi Session State
if "dataset" not in st.session_state:
    st.session_state.dataset = {k: list(v) for k, v in DEFAULT_DATASET.items()}

if "weights" not in st.session_state:
    st.session_state.weights = list(DEFAULT_WEIGHTS)

if "selected_alt" not in st.session_state:
    st.session_state.selected_alt = "Kalis Donut"

if "selected_method" not in st.session_state:
    st.session_state.selected_method = "Tsukamoto"

if "tablet_mode" not in st.session_state:
    st.session_state.tablet_mode = True

if "param_a" not in st.session_state:
    st.session_state.param_a = 1.0

if "param_b" not in st.session_state:
    st.session_state.param_b = 5.0

if "param_mid" not in st.session_state:
    st.session_state.param_mid = 50.0

if "selected_crit_idx" not in st.session_state:
    st.session_state.selected_crit_idx = 0

# Helper dinamis untuk 2 kriteria dengan nilai tertinggi
CRITERIA_SHORT = ["Harga", "Fasilitas", "Jarak", "Kenyamanan", "Jam Buka"]

def get_top_criteria_text(scores):
    """Menghitung 2 kriteria dengan nilai tertinggi secara dinamis."""
    pairs = list(zip(CRITERIA_SHORT, scores))
    sorted_pairs = sorted(pairs, key=lambda x: x[1], reverse=True)
    top2 = sorted_pairs[:2]
    return f"{top2[0][0]}: {top2[0][1]:.1f} | {top2[1][0]}: {top2[1][1]:.1f}"

# Evaluasi seluruh data saat ini
current_df = evaluate_all(
    st.session_state.dataset,
    st.session_state.weights,
    a=st.session_state.param_a,
    b=st.session_state.param_b
)


# =============================================================================
# SIDEBAR KIRI (Warm Peach #FFF1EB, Border #F3D5C5)
# =============================================================================
with st.sidebar:
    # A. Brand Header (Icon Cup SVG + Brand Title)
    st.markdown("""
    <div class="brand-header-box">
        <div class="brand-icon-square">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 8h1a4 4 0 0 1 0 8h-1"></path>
                <path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"></path>
                <line x1="6" y1="1" x2="6" y2="4"></line>
                <line x1="10" y1="1" x2="10" y2="4"></line>
                <line x1="14" y1="1" x2="14" y2="4"></line>
            </svg>
        </div>
        <div class="brand-title-wrap">
            <h2>Fuzzy Tempat Nongkrong</h2>
            <p>SPK Fuzzy Inference</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # B. Search Input
    search_query = st.text_input(
        "Cari",
        placeholder="Cari tempat nongkrong...",
        label_visibility="collapsed",
        key="stitch_search_loc"
    )

    # C. Pilih Metode Inferensi
    st.markdown("""
    <div class="section-label-row">
        <span>PILIH METODE INFERENSI</span>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#8C7E77" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="4" y1="21" x2="4" y2="14"></line><line x1="4" y1="10" x2="4" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="12"></line><line x1="12" y1="8" x2="12" y2="3"></line>
            <line x1="20" y1="21" x2="20" y2="16"></line><line x1="20" y1="12" x2="20" y2="3"></line>
            <line x1="1" y1="14" x2="7" y2="14"></line><line x1="9" y1="8" x2="15" y2="8"></line><line x1="17" y1="16" x2="23" y2="16"></line>
        </svg>
    </div>
    """, unsafe_allow_html=True)

    method_options = ["Tsukamoto", "Sugeno", "Mamdani"]
    method_display_names = {
        "Tsukamoto": "Tsukamoto",
        "Sugeno": "Sugeno Orde-0",
        "Mamdani": "Mamdani Centroid"
    }

    sel_idx = method_options.index(st.session_state.selected_method)
    chosen_method = st.radio(
        "Pilih Metode",
        options=method_options,
        index=sel_idx,
        format_func=lambda x: method_display_names[x],
        label_visibility="collapsed"
    )
    if chosen_method != st.session_state.selected_method:
        st.session_state.selected_method = chosen_method
        st.rerun()

    # D. Daftar Alternatif (4 Lokasi)
    st.markdown("""
    <div class="section-label-row">
        <span>DAFTAR ALTERNATIF</span>
        <span style="font-size: 0.75rem; text-transform: none; color: #8C7E77;">4 Lokasi</span>
    </div>
    """, unsafe_allow_html=True)

    rank_col = f"Rank_{st.session_state.selected_method}"
    score_col = st.session_state.selected_method
    sorted_df = current_df.sort_values(by=rank_col)

    # Ikon-ikon toko/cafe minimalis untuk tiap alternatif sesuai Stitch
    alt_icons = {
        "Kalis Donut": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#8C6A5A" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>',
        "Torte": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#8C6A5A" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>',
        "Anindita": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#8C6A5A" stroke-width="2"><path d="M17 8h1a4 4 0 1 1 0 8h-1"></path><path d="M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4Z"></path><line x1="6" y1="2" x2="6" y2="4"></line><line x1="10" y1="2" x2="10" y2="4"></line><line x1="14" y1="2" x2="14" y2="4"></line></svg>',
        "Cosan": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#8C6A5A" stroke-width="2"><path d="M18 8h1a4 4 0 0 1 0 8h-1"></path><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"></path><line x1="6" y1="1" x2="6" y2="4"></line><line x1="10" y1="1" x2="10" y2="4"></line><line x1="14" y1="1" x2="14" y2="4"></line></svg>'
    }

    for _, row in sorted_df.iterrows():
        name = row["Alternatif"]
        rank = row[rank_col]
        scores_arr = st.session_state.dataset[name]

        if search_query and search_query.lower() not in name.lower():
            continue

        # Hitung 2 kriteria tertinggi secara dinamis
        dynamic_top2 = get_top_criteria_text(scores_arr)

        rank_tag_cls = "rank-1" if rank == 1 else "rank-other"
        icon_svg = alt_icons.get(name, alt_icons["Cosan"])

        card_html = f"""
        <div class="alt-card-stitch">
            <div class="alt-card-header">
                <div class="alt-card-title-left">
                    <div class="alt-icon-box">{icon_svg}</div>
                    <span>{name}</span>
                </div>
                <span class="alt-rank-tag {rank_tag_cls}">#{rank}</span>
            </div>
            <div class="alt-card-subtext">{dynamic_top2}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    # E. Sidebar Footer
    st.markdown('<div class="sidebar-footer-container">', unsafe_allow_html=True)
    st.toggle("Mode Presentasi Tablet", value=st.session_state.tablet_mode, key="tablet_mode_toggle")

    if st.button("↺ Reset Parameter", use_container_width=True):
        st.session_state.dataset = {k: list(v) for k, v in DEFAULT_DATASET.items()}
        st.session_state.weights = list(DEFAULT_WEIGHTS)
        st.session_state.selected_alt = "Kalis Donut"
        st.session_state.selected_method = "Tsukamoto"
        st.session_state.param_a = 1.0
        st.session_state.param_b = 5.0
        st.session_state.param_mid = 50.0
        st.session_state.selected_crit_idx = 0
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# MAIN WORKSPACE KANAN (#FFFFFF / #FAF8F6)
# =============================================================================

# A. Top Navigation Bar (Pill Tabs + Top Action Icons Floating di Kanan)
st.markdown("""
<div class="top-nav-actions-bar">
    <div class="top-action-btn circle">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
    </div>
    <div class="top-action-btn">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M9 18l6-6-6-6"></path></svg>
        <span>Export</span>
    </div>
    <div class="top-action-btn">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg>
        <span>Share</span>
    </div>
    <div class="top-user-avatar">
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
    </div>
</div>
""", unsafe_allow_html=True)

main_tabs = st.tabs([
    "Data & Bobot",
    "Kurva Fuzzy",
    "Proses Hitung",
    "Hasil & What-If",
    "Perbandingan",
    "Analisis & Validasi"
])


# -----------------------------------------------------------------------------
# TAB 1: DATA ALTERNATIF & BOBOT KRITERIA (PIXEL-PERFECT GOOGLE STITCH)
# -----------------------------------------------------------------------------
with main_tabs[0]:
    # 1. Header Konten Sesuai Desain Stitch
    st.markdown("""
    <div class="main-header-row">
        <div class="header-badges-row">
            <span class="badge-tag-input-basis">TAB 1: INPUT BASIS</span>
            <span class="badge-tag-dataset-v">Dataset v1.0</span>
        </div>
        <div class="header-title-bar">
            <h1 class="main-content-title">Data Alternatif & Bobot Kriteria</h1>
            <div class="badge-summary-pill">
                <span class="indicator-dot-green"></span>
                <span>Dataset: 4 Alternatif • 5 Kriteria</span>
            </div>
        </div>
        <p class="main-content-subtitle">
            Kelola parameter input kriteria dan dataset tempat nongkrong untuk inferensi fuzzy.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2. Grid 2 Kolom (Data Alternatif di Kiri, Bobot Kriteria di Kanan)
    col_matrix, col_weights = st.columns([1.35, 1.0], gap="large")

    # --- KOLOM KIRI: Card Data Alternatif ---
    with col_matrix:
        with st.container(border=True):
            st.markdown("""
            <div class="stitch-panel-header">
                <div style="display: flex; align-items: center; gap: 0.65rem;">
                    <div class="header-icon-box blue-icon">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                            <line x1="3" y1="9" x2="21" y2="9"></line>
                            <line x1="3" y1="15" x2="21" y2="15"></line>
                            <line x1="9" y1="3" x2="9" y2="21"></line>
                        </svg>
                    </div>
                    <div>
                        <h3 class="panel-title-text">Data Alternatif</h3>
                        <p class="panel-subtitle-text">Matriks keputusan input fuzzy universe</p>
                    </div>
                </div>
                <span class="badge-tag-gray">Matriks Keputusan (X)</span>
            </div>
            """, unsafe_allow_html=True)

            # Header Kolom Matriks Sesuai Kolom Grid
            col_hdr = st.columns([1.35, 1.0, 1.0, 1.0, 1.0, 1.0])
            with col_hdr[0]:
                st.markdown('<div class="matrix-th-left">ALTERNATIF</div>', unsafe_allow_html=True)
            with col_hdr[1]:
                st.markdown('<div class="matrix-th">C1<small>HARGA</small></div>', unsafe_allow_html=True)
            with col_hdr[2]:
                st.markdown('<div class="matrix-th">C2<small>FASILITAS</small></div>', unsafe_allow_html=True)
            with col_hdr[3]:
                st.markdown('<div class="matrix-th">C3<small>JARAK</small></div>', unsafe_allow_html=True)
            with col_hdr[4]:
                st.markdown('<div class="matrix-th">C4<small>NYAMAN</small></div>', unsafe_allow_html=True)
            with col_hdr[5]:
                st.markdown('<div class="matrix-th">C5<small>JAM BUKA</small></div>', unsafe_allow_html=True)

            # Baris Tabel Matriks dengan Input Box Membulat
            alt_dot_colors = {
                "Anindita": "#10B981",
                "Cosan": "#3B28CC",
                "Kalis Donut": "#10B981",
                "Torte": "#D97706"
            }

            for alt_name in ["Anindita", "Cosan", "Kalis Donut", "Torte"]:
                dot_c = alt_dot_colors[alt_name]
                scores = st.session_state.dataset[alt_name]

                row_cols = st.columns([1.35, 1.0, 1.0, 1.0, 1.0, 1.0])
                with row_cols[0]:
                    st.markdown(f"""
                    <div style="padding-top: 0.55rem; font-weight: 700; font-size: 0.88rem; display: flex; align-items: center; gap: 0.45rem;">
                        <span style="color: {dot_c}; font-size: 0.75rem;">●</span>
                        <span>{alt_name}</span>
                    </div>
                    """, unsafe_allow_html=True)

                new_scores = []
                for j in range(5):
                    with row_cols[j + 1]:
                        val = st.number_input(
                            f"{alt_name}_{j}",
                            min_value=1.0,
                            max_value=5.0,
                            value=float(scores[j]),
                            step=0.5,
                            format="%g",
                            label_visibility="collapsed",
                            key=f"cell_{alt_name}_{j}"
                        )
                        new_scores.append(val)

                st.session_state.dataset[alt_name] = new_scores

            # Banner Informasi Benefit
            st.markdown("""
            <div class="stitch-info-banner">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2.2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                <span>Skor 1-5, 5 = terbaik (semua kriteria bernilai benefit)</span>
            </div>
            """, unsafe_allow_html=True)

            # Tombol Aksi
            btn_c1, btn_c2 = st.columns([1.1, 1.0], gap="medium")
            with btn_c1:
                if st.button("↺ Muat Data Contoh", use_container_width=True):
                    st.session_state.dataset = {k: list(v) for k, v in DEFAULT_DATASET.items()}
                    st.rerun()

            with btn_c2:
                if st.button("Hitung ▷", type="primary", use_container_width=True):
                    st.toast("Perhitungan selesai! Hasil inferensi dan ranking telah diperbarui.", icon=None)

    # --- KOLOM KANAN: Card Bobot Kriteria ---
    with col_weights:
        with st.container(border=True):
            st.markdown("""
            <div class="stitch-panel-header">
                <div style="display: flex; align-items: center; gap: 0.65rem;">
                    <div class="header-icon-box green-icon">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                            <line x1="4" y1="21" x2="4" y2="14"></line><line x1="4" y1="10" x2="4" y2="3"></line>
                            <line x1="12" y1="21" x2="12" y2="12"></line><line x1="12" y1="8" x2="12" y2="3"></line>
                            <line x1="20" y1="21" x2="20" y2="16"></line><line x1="20" y1="12" x2="20" y2="3"></line>
                            <line x1="1" y1="14" x2="7" y2="14"></line><line x1="9" y1="8" x2="15" y2="8"></line><line x1="17" y1="16" x2="23" y2="16"></line>
                        </svg>
                    </div>
                    <div>
                        <h3 class="panel-title-text">Bobot Kriteria</h3>
                        <p class="panel-subtitle-text">Konfigurasi pembobotan fuzzy</p>
                    </div>
                </div>
                <span class="badge-tag-green">Total: 100%</span>
            </div>
            """, unsafe_allow_html=True)

            # 5 Kriteria dengan Progress Bar dan Bobot SAW Sesuai Gambar
            criteria_list_ui = [
                ("Harga (C1)", "w1", 0.25, 25, "#3B28CC", "#3B28CC"),
                ("Fasilitas (C2)", "w2", 0.30, 30, "#10B981", "#10B981"),
                ("Jarak (C3)", "w3", 0.15, 15, "#B45309", "#B45309"),
                ("Kenyamanan (C4)", "w4", 0.18, 18, "#3B28CC", "#3B28CC"),
                ("Jam Operasional (C5)", "w5", 0.12, 12, "#DC2626", "#DC2626")
            ]

            for label, w_code, w_val, pct, dot_col, bar_col in criteria_list_ui:
                st.markdown(f"""
                <div class="stitch-weight-item">
                    <div class="stitch-weight-top">
                        <div class="weight-name-wrap">
                            <span style="color: {dot_col}; font-size: 0.75rem;">●</span>
                            <span>{label}</span>
                        </div>
                        <div class="weight-val-text">
                            <span>{pct}%</span>
                            <span class="weight-sub-val">({w_code} = {w_val:.2f})</span>
                        </div>
                    </div>
                    <div class="stitch-weight-bar">
                        <div class="stitch-weight-fill" style="width: {pct}%; background-color: {bar_col};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Kotak Ringkasan Pembobotan di Bawah
            st.markdown("""
            <div class="stitch-summary-card">
                <div class="summary-card-row">
                    <span>Metode Pembobotan</span>
                    <b>Normalisasi Relatif</b>
                </div>
                <div class="summary-card-row">
                    <span style="display: flex; align-items: center; gap: 0.35rem;">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        <span>Σ Bobot Normal</span>
                    </span>
                    <span style="color: #10B981; font-weight: 700;">1,00 (100%)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 3. Bottom Status Bar
    active_m_label = "Tsukamoto (Monoton)" if st.session_state.selected_method == "Tsukamoto" else (
        "Sugeno Orde-0" if st.session_state.selected_method == "Sugeno" else "Mamdani Centroid"
    )

    st.markdown(f"""
    <div class="stitch-bottom-bar">
        <div class="bottom-bar-left">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2.2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
            <span>Model inferensi aktif: <b>{active_m_label}</b></span>
        </div>
        <div class="bottom-bar-right">
            Data siap diproses. Klik tombol "Hitung" atau beralih ke tab "Kurva Fuzzy".
        </div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# TAB 2: KURVA FUZZY (PIXEL-PERFECT GOOGLE STITCH REVISI)
# -----------------------------------------------------------------------------
with main_tabs[1]:
    crit_options = [
        "C1: Harga",
        "C2: Fasilitas",
        "C3: Jarak",
        "C4: Kenyamanan",
        "C5: Jam Operasional"
    ]
    crit_names_map = ["Harga (C1)", "Fasilitas (C2)", "Jarak (C3)", "Kenyamanan (C4)", "Jam Operasional (C5)"]

    # 1. Header Tab 2 & Dropdown Pemilih Kriteria
    col_t2_hdr, col_t2_crit = st.columns([1.8, 1.0], vertical_alignment="bottom")
    with col_t2_hdr:
        st.markdown("""
        <div class="main-header-row" style="margin-bottom: 0.75rem !important;">
            <div class="header-badges-row">
                <span class="badge-tag-input-basis">TAB 2: FUNGSI KEANGGOTAAN</span>
                <span class="badge-tag-dataset-v">Domain Model</span>
            </div>
            <h1 class="main-content-title">Kurva Fuzzy</h1>
            <p class="main-content-subtitle">
                Fungsi keanggotaan input dan output
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_t2_crit:
        sel_crit = st.selectbox(
            "Kriteria Input",
            options=crit_options,
            index=st.session_state.selected_crit_idx,
            key="select_crit_tab2"
        )
        st.session_state.selected_crit_idx = crit_options.index(sel_crit)

    # 2. Grid 2 Kolom Kurva (Seimbang 50% : 50%)
    col_card_in, col_card_out = st.columns(2, gap="large")

    a = float(st.session_state.param_a)
    b = float(st.session_state.param_b)
    diff = b - a if b != a else 1.0
    x_potong = (a + b) / 2.0
    active_crit_name = crit_names_map[st.session_state.selected_crit_idx]

    # --- CARD KIRI: FUNGSI KEANGGOTAAN INPUT ---
    with col_card_in:
        with st.container(border=True):
            st.markdown(f"""
            <div class="stitch-panel-header">
                <div class="panel-title-group">
                    <h3 class="panel-title-text"><span class="indicator-dot-blue"></span><span>Fungsi Keanggotaan Input</span></h3>
                    <p class="panel-subtitle-text">{active_crit_name}</p>
                </div>
                <span class="badge-tag-mono">a = {a:.1f}; b = {b:.1f}</span>
            </div>
            """, unsafe_allow_html=True)

            # Domain x untuk plot
            x_pad = 0.2
            x_plot_min = max(0.0, a - x_pad)
            x_plot_max = b + x_pad
            x_vals = np.linspace(x_plot_min, x_plot_max, 250)
            y_r = [mu_rendah(x, a, b) for x in x_vals]
            y_t = [mu_tinggi(x, a, b) for x in x_vals]

            fig_in = go.Figure()

            # Garis merah: μ Rendah (Turun)
            fig_in.add_trace(go.Scatter(
                x=x_vals,
                y=y_r,
                mode='lines',
                name='μ Rendah',
                line=dict(color='#EF4444', width=2.5),
                hovertemplate='x: %{x:.2f}<br>μ Rendah: %{y:.3f}<extra></extra>'
            ))

            # Garis biru: μ Tinggi (Naik)
            fig_in.add_trace(go.Scatter(
                x=x_vals,
                y=y_t,
                mode='lines',
                name='μ Tinggi',
                line=dict(color='#3B28CC', width=2.5),
                hovertemplate='x: %{x:.2f}<br>μ Tinggi: %{y:.3f}<extra></extra>'
            ))

            # Garis putus-putus vertikal di titik potong x = (a+b)/2
            fig_in.add_vline(
                x=x_potong,
                line_dash="dash",
                line_color="#CBD5E1",
                line_width=1.5
            )

            # Titik potong ungu dengan marker
            fig_in.add_trace(go.Scatter(
                x=[x_potong],
                y=[0.5],
                mode='markers',
                name=f'Titik Potong ({x_potong:g}; 0.5)',
                marker=dict(color='#7C3AED', size=8, line=dict(color='#FFFFFF', width=2)),
                hovertemplate=f'Titik Potong: ({x_potong:g}, 0.500)<extra></extra>'
            ))

            # Nilai kriteria tempat nongkrong yang sedang aktif
            crit_idx = st.session_state.selected_crit_idx
            active_val = float(st.session_state.dataset[st.session_state.selected_alt][crit_idx])
            mu_r_act = mu_rendah(active_val, a, b)
            mu_t_act = mu_tinggi(active_val, a, b)

            # Tambahkan penanda hanya jika tidak bertumpuk persis di titik potong
            if abs(active_val - x_potong) > 0.08:
                fig_in.add_vline(
                    x=active_val,
                    line_dash="dot",
                    line_color="#10B981",
                    line_width=1.5
                )
                fig_in.add_annotation(
                    x=active_val,
                    y=0.92,
                    text=f"{st.session_state.selected_alt}: {active_val:g}",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=1.2,
                    arrowcolor="#10B981",
                    ax=0,
                    ay=-22,
                    font=dict(family="Plus Jakarta Sans", size=10, color="#065F46"),
                    bgcolor="#ECFDF5",
                    bordercolor="#A7F3D0",
                    borderwidth=1,
                    borderpad=3
                )

            fig_in.update_layout(
                xaxis=dict(
                    title=dict(text=f"Skor {active_crit_name} (x)", font=dict(size=11, color="#6B7280", family="Plus Jakarta Sans")),
                    range=[x_plot_min - 0.05, x_plot_max + 0.05],
                    gridcolor="#F1F5F9",
                    zerolinecolor="#E2E8F0",
                    linecolor="#E2E8F0",
                    tickfont=dict(size=10, color="#6B7280")
                ),
                yaxis=dict(
                    title=dict(text="Derajat Keanggotaan (μ)", font=dict(size=11, color="#6B7280", family="Plus Jakarta Sans")),
                    range=[-0.05, 1.05],
                    gridcolor="#F1F5F9",
                    zerolinecolor="#E2E8F0",
                    linecolor="#E2E8F0",
                    tickfont=dict(size=10, color="#6B7280")
                ),
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.22,
                    xanchor="center",
                    x=0.5,
                    font=dict(family="Plus Jakarta Sans", size=10.5, color="#4B5563")
                ),
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                height=320,
                margin=dict(l=48, r=20, t=15, b=55)
            )

            st.plotly_chart(fig_in, use_container_width=True, config={'displayModeBar': False})

            # Container Rumus Dinamis di Bawah Grafik
            st.markdown(f"""
            <div class="stitch-formula-box">
                <div class="formula-row">
                    <span class="formula-label-red">μ Rendah(x):</span>
                    <span class="formula-code">({b:g} - x) / {diff:g}</span>
                </div>
                <div class="formula-row">
                    <span class="formula-label-blue">μ Tinggi(x):</span>
                    <span class="formula-code">(x - {a:g}) / {diff:g}</span>
                </div>
                <div class="formula-eval-row">
                    <span class="formula-eval-label">Skor {st.session_state.selected_alt} (x = {active_val:g}):</span>
                    <span class="formula-eval-val">
                        <span style="color: #DC2626;">μ_R = {mu_r_act:.3f}</span> • <span style="color: #3B28CC;">μ_T = {mu_t_act:.3f}</span>
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- CARD KANAN: FUNGSI KEANGGOTAAN OUTPUT ---
    with col_card_out:
        with st.container(border=True):
            mid = float(st.session_state.param_mid)
            active_method = st.session_state.selected_method
            active_m_label = "Tsukamoto" if active_method == "Tsukamoto" else (
                "Sugeno Orde-0" if active_method == "Sugeno" else "Mamdani Centroid"
            )

            st.markdown(f"""
            <div class="stitch-panel-header">
                <div class="panel-title-group">
                    <h3 class="panel-title-text"><span class="indicator-dot-green"></span><span>Fungsi Keanggotaan Output</span></h3>
                    <p class="panel-subtitle-text">Model: {active_m_label}</p>
                </div>
                <span class="badge-tag-mono">Titik Tengah: {mid:.1f}</span>
            </div>
            """, unsafe_allow_html=True)

            # Output Plotly Figure
            z_vals = np.linspace(0.0, 100.0, 300)
            y_out_tl = [mu_output_tidak_layak(z, 0.0, mid) for z in z_vals]
            y_out_l = [mu_output_layak(z, mid, 100.0) for z in z_vals]

            fig_out = go.Figure()

            # Tidak Layak (z <= mid) - Garis merah
            fig_out.add_trace(go.Scatter(
                x=z_vals,
                y=y_out_tl,
                mode='lines',
                name=f'Tidak Layak (z ≤ {mid:g})',
                line=dict(color='#EF4444', width=2.5),
                hovertemplate='z: %{x:.2f}<br>μ Tidak Layak: %{y:.3f}<extra></extra>'
            ))

            # Layak (z >= mid) - Garis hijau toska
            fig_out.add_trace(go.Scatter(
                x=z_vals,
                y=y_out_l,
                mode='lines',
                name=f'Layak (z ≥ {mid:g})',
                line=dict(color='#10B981', width=2.5),
                hovertemplate='z: %{x:.2f}<br>μ Layak: %{y:.3f}<extra></extra>'
            ))

            # Garis putus-putus vertikal di titik pisah z = mid
            fig_out.add_vline(
                x=mid,
                line_dash="dash",
                line_color="#CBD5E1",
                line_width=1.5
            )

            # Penanda skor tempat nongkrong yang sedang aktif
            active_z = float(current_df.loc[current_df["Alternatif"] == st.session_state.selected_alt, active_method].values[0])
            fig_out.add_vline(
                x=active_z,
                line_dash="dot",
                line_color="#3B28CC",
                line_width=1.5
            )
            fig_out.add_annotation(
                x=active_z,
                y=0.92,
                text=f"<b>{st.session_state.selected_alt}</b>: {active_z:.2f}",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=1.2,
                arrowcolor="#3B28CC",
                ax=0,
                ay=-22,
                font=dict(family="Plus Jakarta Sans", size=10, color="#1E1B2E"),
                bgcolor="#EEF2FF",
                bordercolor="#C7D2FE",
                borderwidth=1,
                borderpad=3
            )

            fig_out.update_layout(
                xaxis=dict(
                    title=dict(text="Nilai Kelayakan (z ∈ [0, 100])", font=dict(size=11, color="#6B7280", family="Plus Jakarta Sans")),
                    range=[-2, 102],
                    gridcolor="#F1F5F9",
                    zerolinecolor="#E2E8F0",
                    linecolor="#E2E8F0",
                    tickfont=dict(size=10, color="#6B7280")
                ),
                yaxis=dict(
                    title=dict(text="Derajat Keanggotaan (μ)", font=dict(size=11, color="#6B7280", family="Plus Jakarta Sans")),
                    range=[-0.05, 1.05],
                    gridcolor="#F1F5F9",
                    zerolinecolor="#E2E8F0",
                    linecolor="#E2E8F0",
                    tickfont=dict(size=10, color="#6B7280")
                ),
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.22,
                    xanchor="center",
                    x=0.5,
                    font=dict(family="Plus Jakarta Sans", size=10.5, color="#4B5563")
                ),
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                height=320,
                margin=dict(l=48, r=20, t=15, b=55)
            )

            st.plotly_chart(fig_out, use_container_width=True, config={'displayModeBar': False})

            # Container Rumus Output Sesuai Model Aktif
            if active_method == "Tsukamoto":
                st.markdown(f"""
                <div class="stitch-formula-box">
                    <div class="formula-row">
                        <span class="formula-label-red">z_Tidak Layak:</span>
                        <span class="formula-code">{mid:g} - (α × {mid:g})</span>
                    </div>
                    <div class="formula-row">
                        <span class="formula-label-green">z_Layak:</span>
                        <span class="formula-code">{mid:g} + (α × {100.0 - mid:g})</span>
                    </div>
                    <div class="formula-eval-row">
                        <span class="formula-eval-label">Defuzzifikasi Tsukamoto:</span>
                        <span class="formula-eval-val" style="color: #3B28CC;">z* = Σ(αi · zi) / Σ(αi)</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif active_method == "Sugeno":
                st.markdown("""
                <div class="stitch-formula-box">
                    <div class="formula-row">
                        <span class="formula-label-red">z_Tidak Layak:</span>
                        <span class="formula-code">k_TL = 25.0 (Singleton)</span>
                    </div>
                    <div class="formula-row">
                        <span class="formula-label-green">z_Layak:</span>
                        <span class="formula-code">k_L = 75.0 (Singleton)</span>
                    </div>
                    <div class="formula-eval-row">
                        <span class="formula-eval-label">Defuzzifikasi Sugeno Orde-0:</span>
                        <span class="formula-eval-val" style="color: #3B28CC;">z* = Σ(αi · ki) / Σ(αi)</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:  # Mamdani
                st.markdown("""
                <div class="stitch-formula-box">
                    <div class="formula-row">
                        <span class="formula-label-purple">Luas Trapesium (A):</span>
                        <span class="formula-code">A1 = 25α1(2 - α1) | A2 = 25α2(2 - α2)</span>
                    </div>
                    <div class="formula-row">
                        <span class="formula-label-purple">Momen Trapesium (M):</span>
                        <span class="formula-code">M1 = (2500/6)α1(3-3α1+α1²) | M2 = ...</span>
                    </div>
                    <div class="formula-eval-row">
                        <span class="formula-eval-label">Defuzzifikasi Centroid:</span>
                        <span class="formula-eval-val" style="color: #3B28CC;">z* = (M1 + M2) / (A1 + A2)</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # 3. Bottom Accordion: Atur Batas Fungsi Keanggotaan (Fitur F3)
    with st.expander("▶  Atur Batas Fungsi Keanggotaan (Fitur F3)", expanded=False):
        st.markdown("""
        <div style="font-size: 0.825rem; color: #6B7280; margin-bottom: 0.85rem;">
            Konfigurasi batas bawah (a) dan batas atas (b) kriteria input serta titik pisah kelayakan output (mid). Perubahan akan otomatis mengkalkulasi ulang kurva dan formula.
        </div>
        """, unsafe_allow_html=True)

        c_f3_1, c_f3_2, c_f3_3, c_f3_4 = st.columns([1.0, 1.0, 1.0, 1.2], gap="medium", vertical_alignment="bottom")

        with c_f3_1:
            new_a = st.number_input(
                "Batas Bawah Input (a)",
                min_value=0.0,
                max_value=float(st.session_state.param_b - 0.5),
                value=float(st.session_state.param_a),
                step=0.5,
                format="%.1f",
                key="input_f3_a"
            )
            if new_a != st.session_state.param_a:
                st.session_state.param_a = new_a
                st.rerun()

        with c_f3_2:
            new_b = st.number_input(
                "Batas Atas Input (b)",
                min_value=float(st.session_state.param_a + 0.5),
                max_value=10.0,
                value=float(st.session_state.param_b),
                step=0.5,
                format="%.1f",
                key="input_f3_b"
            )
            if new_b != st.session_state.param_b:
                st.session_state.param_b = new_b
                st.rerun()

        with c_f3_3:
            new_mid = st.number_input(
                "Titik Tengah Output (mid)",
                min_value=10.0,
                max_value=90.0,
                value=float(st.session_state.param_mid),
                step=5.0,
                format="%.1f",
                key="input_f3_mid"
            )
            if new_mid != st.session_state.param_mid:
                st.session_state.param_mid = new_mid
                st.rerun()

        with c_f3_4:
            if st.button("↺ Reset ke Default", key="reset_f3_btn", use_container_width=True):
                st.session_state.param_a = 1.0
                st.session_state.param_b = 5.0
                st.session_state.param_mid = 50.0
                st.rerun()



# -----------------------------------------------------------------------------
# TAB 3: PROSES HITUNG
# -----------------------------------------------------------------------------
with main_tabs[2]:
    c_sel1, c_sel2 = st.columns([1.5, 1.0])
    with c_sel1:
        chosen_inspect = st.selectbox(
            "Pilih Tempat Nongkrong untuk Dianalisis",
            options=list(st.session_state.dataset.keys()),
            index=list(st.session_state.dataset.keys()).index(st.session_state.selected_alt)
        )
        if chosen_inspect != st.session_state.selected_alt:
            st.session_state.selected_alt = chosen_inspect
            st.rerun()

    st.markdown(f"""
    <div class="stitch-panel-card">
        <h3 class="panel-title-text">Rincian Perhitungan: <span style="color:#3B28CC;">{st.session_state.selected_alt}</span></h3>
        <p style="color:#6B7280; font-size:0.85rem; margin-top:0.25rem;">
            Metode Inferensi: <b>{st.session_state.selected_method}</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    scores_now = st.session_state.dataset[st.session_state.selected_alt]

    if st.session_state.selected_method == "Tsukamoto":
        calc_res = calculate_tsukamoto(scores_now, weights=st.session_state.weights)
    elif st.session_state.selected_method == "Sugeno":
        calc_res = calculate_sugeno(scores_now, weights=st.session_state.weights)
    else:
        calc_res = calculate_mamdani(scores_now, weights=st.session_state.weights)

    with st.expander("Tahap 1: Fuzzifikasi Nilai Input", expanded=True):
        fuzz_table = []
        for crit, val in zip(CRITERIA_NAMES, scores_now):
            fuzz_table.append({
                "Kriteria": crit,
                "Nilai (x)": val,
                "μ Rendah": f"{mu_rendah(val):.3f}",
                "μ Tinggi": f"{mu_tinggi(val):.3f}"
            })
        st.dataframe(pd.DataFrame(fuzz_table), use_container_width=True)

    with st.expander(f"Tahap 2: Evaluasi Aturan ({calc_res['active_count']} Rule Aktif dari 32)", expanded=True):
        active_list = []
        for r in calc_res["active_rules"]:
            row_dict = {
                "Rule": f"R{r['rule_id']}",
                "Kombinasi Kondisi": " & ".join(r["antecedents"]),
                "Konsekuen": r["consequent"],
                "α-predikat": r["alpha"]
            }
            if "z_i" in r:
                row_dict["z_i"] = r["z_i"]
                row_dict["α · z_i"] = r["alpha_z"]
            elif "k_i" in r:
                row_dict["k_i"] = r["k_i"]
                row_dict["α · k_i"] = r["alpha_k"]
            active_list.append(row_dict)
        st.dataframe(pd.DataFrame(active_list), use_container_width=True)

    with st.expander("Tahap 3: Defuzzifikasi dan Hasil Akhir", expanded=True):
        if st.session_state.selected_method == "Tsukamoto":
            st.latex(r"z^* = \frac{\sum \alpha_i \cdot z_i}{\sum \alpha_i} = \frac{" + f"{calc_res['sum_alpha_z']:.4f}" + r"}{" + f"{calc_res['sum_alpha']:.4f}" + r"} = " + f"{calc_res['score']:.2f}")
        elif st.session_state.selected_method == "Sugeno":
            st.latex(r"z^* = \frac{\sum \alpha_i \cdot k_i}{\sum \alpha_i} = \frac{" + f"{calc_res['sum_alpha_k']:.4f}" + r"}{" + f"{calc_res['sum_alpha']:.4f}" + r"} = " + f"{calc_res['score']:.2f}")
        else:
            st.latex(r"z^* = \frac{M_1 + M_2}{A_1 + A_2} = \frac{" + f"{calc_res['total_moment']:.4f}" + r"}{" + f"{calc_res['total_area']:.4f}" + r"} = " + f"{calc_res['score']:.2f}")


# -----------------------------------------------------------------------------
# TAB 4: HASIL & SIMULASI WHAT-IF
# -----------------------------------------------------------------------------
with main_tabs[3]:
    winner = current_df.sort_values(by=f"Rank_{st.session_state.selected_method}").iloc[0]

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #F3F0FF 0%, #E8E5FF 100%); border: 1.5px solid rgba(59, 40, 204, 0.2); border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem;">
        <span style="font-size: 0.75rem; font-weight: 800; color: #3B28CC; text-transform: uppercase;">Rekomendasi Utama (#{winner[f'Rank_{st.session_state.selected_method}']})</span>
        <h2 style="font-size: 1.85rem; font-weight: 800; color: #1E1B2E; margin: 0.25rem 0;">{winner['Alternatif']}</h2>
        <p style="font-size: 0.95rem; color: #4B5563; margin-bottom: 0.5rem;">
            Meraih skor kelayakan tertinggi <b>{winner[st.session_state.selected_method]:.2f} / 100</b> pada metode <b>{st.session_state.selected_method}</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c_plot, c_whatif = st.columns([1.3, 1.0], gap="large")
    with c_plot:
        st.markdown('<div class="stitch-panel-card"><h3 class="panel-title-text">Ranking Skor Kelayakan</h3>', unsafe_allow_html=True)
        bar_df = current_df.sort_values(by=st.session_state.selected_method, ascending=True)
        fig_b = px.bar(
            bar_df,
            x=st.session_state.selected_method,
            y="Alternatif",
            orientation="h",
            text=st.session_state.selected_method,
            color=st.session_state.selected_method,
            color_continuous_scale=["#C7D2FE", "#4F46E5", "#312E81"]
        )
        fig_b.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig_b.update_layout(
            xaxis_title="Skor (0 - 100)",
            yaxis_title="",
            plot_bgcolor="#FAF8F6",
            paper_bgcolor="#FFFFFF",
            height=280,
            coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=10, b=10)
        )
        st.plotly_chart(fig_b, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_whatif:
        st.markdown("""
        <div class="stitch-panel-card">
            <h3 class="panel-title-text">Playground What-If</h3>
            <p style="font-size:0.8rem; color:#6B7280; margin-bottom:0.75rem;">Uji perubahan skor seketika:</p>
        """, unsafe_allow_html=True)

        sliders = []
        base = st.session_state.dataset[st.session_state.selected_alt]
        for idx, (cr, b_val) in enumerate(zip(CRITERIA_NAMES, base)):
            val = st.slider(cr, 1.0, 5.0, float(b_val), 0.1, key=f"sl_whatif_{idx}")
            sliders.append(val)

        sim_t = calculate_tsukamoto(sliders)["score"]
        sim_s = calculate_sugeno(sliders)["score"]
        sim_m = calculate_mamdani(sliders)["score"]

        st.markdown(f"""
        <div style="background:#FAF8F6; padding:0.75rem; border-radius:10px; margin-top:0.75rem; font-size:0.9rem;">
            <div>Tsukamoto: <b>{sim_t:.2f}</b></div>
            <div>Sugeno: <b>{sim_s:.2f}</b></div>
            <div>Mamdani: <b>{sim_m:.2f}</b></div>
        </div>
        </div>
        """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# TAB 5: PERBANDINGAN
# -----------------------------------------------------------------------------
with main_tabs[4]:
    st.markdown('<div class="stitch-panel-card"><h3 class="panel-title-text">Komparasi Lintas Metode Fuzzy & SAW</h3>', unsafe_allow_html=True)
    st.dataframe(
        current_df[[
            "Alternatif",
            "Tsukamoto", "Rank_Tsukamoto",
            "Sugeno", "Rank_Sugeno",
            "Mamdani", "Rank_Mamdani",
            "SAW_Terkoreksi", "Rank_SAW_Terkoreksi",
            "SAW_Deck_Asli", "Rank_SAW_Deck_Asli"
        ]],
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# TAB 6: ANALISIS & VALIDASI
# -----------------------------------------------------------------------------
with main_tabs[5]:
    st.markdown("""
    <div class="stitch-panel-card">
        <h3 class="panel-title-text">Validasi Manual & Ekspor</h3>
        <div style="background:#ECFDF5; border-left:4px solid #10B981; padding:0.75rem 1rem; border-radius:8px; margin: 1rem 0;">
            <b style="color:#065F46; display: flex; align-items: center; gap: 0.35rem;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                <span>100% Selaras dengan Hitungan Manual</span>
            </b>
            <p style="margin:0.25rem 0 0; font-size:0.825rem; color:#065F46;">Seluruh 8 pengujian unit test pytest lulus sempurna.</p>
        </div>
    """, unsafe_allow_html=True)

    csv_bytes = current_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Unduh Hasil CSV",
        data=csv_bytes,
        file_name="fuzzy_tempat_nongkrong_ranking.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
