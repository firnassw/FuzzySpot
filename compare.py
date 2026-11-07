"""
compare.py
Penyatuan hasil 3 metode Fuzzy (Tsukamoto, Sugeno, Mamdani)
serta komparasi terhadap 2 versi SAW (Deck Asli vs Terkoreksi).
"""
from typing import Dict, List, Any
import numpy as np
import pandas as pd

from tsukamoto import calculate_tsukamoto
from sugeno import calculate_sugeno
from mamdani import calculate_mamdani
from rules import CRITERIA_NAMES, DEFAULT_WEIGHTS

DEFAULT_DATASET: Dict[str, List[float]] = {
    "Anindita": [5.0, 2.0, 5.0, 2.0, 3.0],
    "Cosan": [3.0, 3.0, 4.0, 4.0, 4.0],
    "Kalis Donut": [3.0, 5.0, 4.0, 5.0, 2.0],
    "Torte": [4.0, 3.0, 3.0, 4.0, 5.0]
}


def calculate_saw(
    matrix: np.ndarray,
    weights: np.ndarray,
    cost_indices: List[int] = None
) -> np.ndarray:
    """
    Menghitung skor Simple Additive Weighting (SAW).
    - Jika index ada di cost_indices: r_ij = min(x_j) / x_ij
    - Jika Benefit: r_ij = x_ij / max(x_j)
    """
    if cost_indices is None:
        cost_indices = []

    m, n = matrix.shape
    norm_matrix = np.zeros_like(matrix, dtype=float)

    max_vals = matrix.max(axis=0)
    min_vals = matrix.min(axis=0)

    for j in range(n):
        if j in cost_indices:
            # Cost: min / x
            norm_matrix[:, j] = np.where(matrix[:, j] > 0, min_vals[j] / matrix[:, j], 0.0)
        else:
            # Benefit: x / max
            norm_matrix[:, j] = np.where(max_vals[j] > 0, matrix[:, j] / max_vals[j], 0.0)

    scores = norm_matrix.dot(weights)
    return scores


def evaluate_all(
    dataset: Dict[str, List[float]] = None,
    weights: List[float] = None,
    a: float = 1.0,
    b: float = 5.0
) -> pd.DataFrame:
    """
    Mengevaluasi seluruh alternatif untuk seluruh metode:
    - Tsukamoto (0-100)
    - Sugeno (0-100)
    - Mamdani (0-100)
    - SAW Terkoreksi (Semua Benefit, skala 0-1 dan skala 0-100)
    - SAW Deck Asli (C1 Harga & C3 Jarak Cost, skala 0-1 dan skala 0-100)
    """
    if dataset is None:
        dataset = DEFAULT_DATASET
    if weights is None:
        weights = DEFAULT_WEIGHTS

    names = list(dataset.keys())
    matrix = np.array([dataset[name] for name in names], dtype=float)
    w_arr = np.array(weights, dtype=float)

    # 1. Fuzzy Methods
    tsuk_scores = []
    sug_scores = []
    mam_scores = []

    for name in names:
        sc = dataset[name]
        t_res = calculate_tsukamoto(sc, weights=weights, a=a, b=b)
        s_res = calculate_sugeno(sc, weights=weights, a=a, b=b)
        m_res = calculate_mamdani(sc, weights=weights, a=a, b=b)

        tsuk_scores.append(t_res["score"])
        sug_scores.append(s_res["score"])
        mam_scores.append(m_res["score"])

    # 2. SAW Terkoreksi (All Benefit)
    saw_benefit = calculate_saw(matrix, w_arr, cost_indices=[])

    # 3. SAW Deck Asli (C1 Harga idx 0, C3 Jarak idx 2 sebagai Cost)
    saw_asli = calculate_saw(matrix, w_arr, cost_indices=[0, 2])

    df = pd.DataFrame({
        "Alternatif": names,
        "Tsukamoto": tsuk_scores,
        "Sugeno": sug_scores,
        "Mamdani": mam_scores,
        "SAW_Terkoreksi": saw_benefit,
        "SAW_Deck_Asli": saw_asli
    })

    # Ranking untuk tiap metode (1 = tertinggi)
    df["Rank_Tsukamoto"] = df["Tsukamoto"].rank(ascending=False, method="min").astype(int)
    df["Rank_Sugeno"] = df["Sugeno"].rank(ascending=False, method="min").astype(int)
    df["Rank_Mamdani"] = df["Mamdani"].rank(ascending=False, method="min").astype(int)
    df["Rank_SAW_Terkoreksi"] = df["SAW_Terkoreksi"].rank(ascending=False, method="min").astype(int)
    df["Rank_SAW_Deck_Asli"] = df["SAW_Deck_Asli"].rank(ascending=False, method="min").astype(int)

    return df


def calculate_sensitivity(
    dataset: Dict[str, List[float]] = None,
    criterion_idx: int = 1, # default C2 Fasilitas
    weights: List[float] = None,
    steps: int = 41
) -> pd.DataFrame:
    """
    Analisis sensitivitas: menghitung variasi skor tiap alternatif saat satu kriteria diubah dari 1.0 ke 5.0.
    """
    if dataset is None:
        dataset = DEFAULT_DATASET
    if weights is None:
        weights = DEFAULT_WEIGHTS

    names = list(dataset.keys())
    val_range = np.linspace(1.0, 5.0, steps)

    records = []
    for val in val_range:
        for name in names:
            sc = list(dataset[name])
            sc[criterion_idx] = float(val)

            t_score = calculate_tsukamoto(sc, weights=weights)["score"]
            s_score = calculate_sugeno(sc, weights=weights)["score"]
            m_score = calculate_mamdani(sc, weights=weights)["score"]

            records.append({
                "Nilai_Kriteria": round(val, 2),
                "Alternatif": name,
                "Tsukamoto": t_score,
                "Sugeno": s_score,
                "Mamdani": m_score
            })

    return pd.DataFrame(records)

