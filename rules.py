"""
rules.py
Pembangkitan otomatis 32 aturan fuzzy (2^5 kombinasi) berbasis bobot kriteria SAW.
"""
from typing import List, Tuple, Dict, Any
import itertools
from membership import mu_rendah, mu_tinggi

CRITERIA_NAMES = [
    "C1 Harga",
    "C2 Fasilitas",
    "C3 Jarak",
    "C4 Kenyamanan",
    "C5 Jam Operasional"
]

DEFAULT_WEIGHTS = [0.25, 0.30, 0.15, 0.18, 0.12]


def generate_rules(weights: List[float] = None) -> List[Dict[str, Any]]:
    """
    Membangkitkan 32 rule dari kombinasi (Rendah, Tinggi) untuk 5 kriteria.
    Konsekuen = 'Layak' jika total bobot kriteria yang 'Tinggi' > 0.5, selain itu 'Tidak Layak'.
    Menghasilkan tepat 16 rule Layak dan 16 rule Tidak Layak.
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS

    rules = []
    # Urutkan kombinasi agar deterministik: Rendah duluan, Tinggi kemudian
    combinations = list(itertools.product(["Rendah", "Tinggi"], repeat=len(weights)))

    for idx, combo in enumerate(combinations, start=1):
        total_weight_tinggi = sum(
            w for level, w in zip(combo, weights) if level == "Tinggi"
        )
        consequent = "Layak" if total_weight_tinggi > 0.5 else "Tidak Layak"

        rules.append({
            "rule_id": idx,
            "antecedents": combo,
            "weight_tinggi": round(total_weight_tinggi, 4),
            "consequent": consequent
        })

    return rules


def evaluate_rules(
    scores: List[float],
    rules: List[Dict[str, Any]] = None,
    weights: List[float] = None,
    a: float = 1.0,
    b: float = 5.0
) -> List[Dict[str, Any]]:
    """
    Mengevaluasi firing strength (alpha-predikat) untuk setiap rule dengan input skor tertentu.
    alpha_i = min(mu_1, mu_2, ..., mu_5)
    """
    if rules is None:
        rules = generate_rules(weights)

    # Hitung mu_rendah dan mu_tinggi untuk tiap kriteria input
    memberships = []
    for score in scores:
        memberships.append({
            "Rendah": mu_rendah(score, a=a, b=b),
            "Tinggi": mu_tinggi(score, a=a, b=b)
        })

    evaluated = []
    for r in rules:
        antecedents = r["antecedents"]
        mu_values = [memberships[i][level] for i, level in enumerate(antecedents)]
        alpha = min(mu_values)

        evaluated.append({
            "rule_id": r["rule_id"],
            "antecedents": antecedents,
            "weight_tinggi": r["weight_tinggi"],
            "consequent": r["consequent"],
            "mu_values": mu_values,
            "alpha": round(alpha, 6),
            "is_active": alpha > 0.0
        })

    return evaluated

