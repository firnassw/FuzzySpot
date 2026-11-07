"""
tests/test_fuzzy.py
Pengujian unit test otomatis untuk seluruh modul mesin fuzzy:
membership, rules, tsukamoto, sugeno, mamdani, dan compare.
"""
import pytest
import numpy as np
import pandas as pd

from membership import mu_rendah, mu_tinggi, mu_output_tidak_layak, mu_output_layak
from rules import generate_rules, evaluate_rules, CRITERIA_NAMES, DEFAULT_WEIGHTS
from tsukamoto import calculate_tsukamoto
from sugeno import calculate_sugeno
from mamdani import calculate_mamdani
from compare import evaluate_all, DEFAULT_DATASET, calculate_saw


def test_membership_boundaries():
    """Menguji fungsi keanggotaan input dan output beserta clamping [0, 1]."""
    # Batas bawah dan atas
    assert mu_rendah(1.0) == 1.0
    assert mu_rendah(5.0) == 0.0
    assert mu_tinggi(1.0) == 0.0
    assert mu_tinggi(5.0) == 1.0

    # Titik tengah (3.0)
    assert mu_rendah(3.0) == 0.5
    assert mu_tinggi(3.0) == 0.5

    # Clamping di luar rentang [1, 5]
    assert mu_rendah(0.0) == 1.0
    assert mu_rendah(6.0) == 0.0
    assert mu_tinggi(0.0) == 0.0
    assert mu_tinggi(6.0) == 1.0

    # Output terbelah pada [0, 100] dengan mid = 50.0
    assert mu_output_tidak_layak(0.0) == 1.0
    assert mu_output_tidak_layak(50.0) == 0.0
    assert mu_output_tidak_layak(25.0) == 0.5
    assert mu_output_layak(50.0) == 0.0
    assert mu_output_layak(100.0) == 1.0
    assert mu_output_layak(75.0) == 0.5


def test_rules_generation():
    """Menguji bahwa tepat 32 rule dibangkitkan, dengan 16 Layak dan 16 Tidak Layak."""
    rules = generate_rules(DEFAULT_WEIGHTS)
    assert len(rules) == 32

    layak_count = sum(1 for r in rules if r["consequent"] == "Layak")
    tidak_layak_count = sum(1 for r in rules if r["consequent"] == "Tidak Layak")

    assert layak_count == 16
    assert tidak_layak_count == 16


def test_anindita():
    """Pengujian Alternatif Anindita: [5, 2, 5, 2, 3]"""
    scores = DEFAULT_DATASET["Anindita"]
    t_res = calculate_tsukamoto(scores)
    s_res = calculate_sugeno(scores)
    m_res = calculate_mamdani(scores)

    assert t_res["score"] == pytest.approx(57.50, abs=0.01)
    assert s_res["score"] == pytest.approx(65.00, abs=0.01)
    assert m_res["score"] == pytest.approx(50.00, abs=0.01)


def test_cosan():
    """Pengujian Alternatif Cosan: [3, 3, 4, 4, 4]"""
    scores = DEFAULT_DATASET["Cosan"]
    t_res = calculate_tsukamoto(scores)
    s_res = calculate_sugeno(scores)
    m_res = calculate_mamdani(scores)

    # Mamdani tepat 50.00
    assert m_res["score"] == pytest.approx(50.00, abs=0.01)

    # Tsukamoto: analitik 52.0833 (dibulatkan di PRD menjadi 52.1 atau 52.14)
    assert abs(t_res["score"] - 52.08) < 0.1 or abs(t_res["score"] - 52.14) < 0.1
    # Sugeno: analitik 51.3889 (dibulatkan di PRD menjadi 51.4 atau 51.43)
    assert abs(s_res["score"] - 51.39) < 0.1 or abs(s_res["score"] - 51.43) < 0.1


def test_kalis_donut():
    """Pengujian Alternatif Kalis Donut: [3, 5, 4, 5, 2]"""
    scores = DEFAULT_DATASET["Kalis Donut"]
    t_res = calculate_tsukamoto(scores)
    s_res = calculate_sugeno(scores)
    m_res = calculate_mamdani(scores)

    assert t_res["score"] == pytest.approx(65.00, abs=0.01)
    assert s_res["score"] == pytest.approx(70.00, abs=0.01)
    assert m_res["score"] == pytest.approx(58.99, abs=0.05) # ~59.0


def test_torte():
    """Pengujian Alternatif Torte: [4, 3, 3, 4, 5]"""
    scores = DEFAULT_DATASET["Torte"]
    t_res = calculate_tsukamoto(scores)
    s_res = calculate_sugeno(scores)
    m_res = calculate_mamdani(scores)

    assert t_res["score"] == pytest.approx(60.00, abs=0.01)
    assert s_res["score"] == pytest.approx(60.00, abs=0.01)
    assert m_res["score"] == pytest.approx(58.99, abs=0.05) # ~59.0


def test_saw_comparison():
    """Pengujian hasil komparasi SAW (Deck Asli vs Terkoreksi)."""
    df = evaluate_all()

    # SAW Terkoreksi (semua Benefit searah)
    saw_benefit = dict(zip(df["Alternatif"], df["SAW_Terkoreksi"]))
    assert saw_benefit["Kalis Donut"] == pytest.approx(0.7980, abs=0.001)
    assert saw_benefit["Torte"] == pytest.approx(0.7340, abs=0.001)
    assert saw_benefit["Cosan"] == pytest.approx(0.6900, abs=0.001)
    assert saw_benefit["Anindita"] == pytest.approx(0.6640, abs=0.001)

    # SAW Deck Asli (C1 Harga dan C3 Jarak sebagai Cost)
    saw_asli = dict(zip(df["Alternatif"], df["SAW_Deck_Asli"]))
    assert saw_asli["Kalis Donut"] == pytest.approx(0.8905, abs=0.001)
    assert saw_asli["Cosan"] == pytest.approx(0.7825, abs=0.001)
    assert saw_asli["Torte"] == pytest.approx(0.7815, abs=0.001)
    assert saw_asli["Anindita"] == pytest.approx(0.5040, abs=0.001)


def test_extreme_cases():
    """Pengujian kasus ekstrem: semua terendah (1.0) dan semua tertinggi (5.0)."""
    worst = [1.0, 1.0, 1.0, 1.0, 1.0]
    best = [5.0, 5.0, 5.0, 5.0, 5.0]

    # Kasus terburuk: Tsukamoto = 0.0, Sugeno = 25.0
    assert calculate_tsukamoto(worst)["score"] == pytest.approx(0.0, abs=0.01)
    assert calculate_sugeno(worst)["score"] == pytest.approx(25.0, abs=0.01)

    # Kasus terbaik: Tsukamoto = 100.0, Sugeno = 75.0
    assert calculate_tsukamoto(best)["score"] == pytest.approx(100.0, abs=0.01)
    assert calculate_sugeno(best)["score"] == pytest.approx(75.0, abs=0.01)

