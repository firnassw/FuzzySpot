"""
mamdani.py
Mesin inferensi fuzzy metode Mamdani dengan rumus centroid analitik eksak
(Piecewise Trapezoid Area & Moment) untuk selisih 0.0000 terhadap hitungan manual.
"""
from typing import List, Dict, Any
from rules import evaluate_rules


def calculate_mamdani(
    scores: List[float],
    rules: List[Dict[str, Any]] = None,
    weights: List[float] = None,
    a: float = 1.0,
    b: float = 5.0,
    mid: float = 50.0
) -> Dict[str, Any]:
    """
    Menghitung skor kelayakan menggunakan metode Mamdani secara analitik eksak.
    """
    evaluated = evaluate_rules(scores, rules=rules, weights=weights, a=a, b=b)

    alphas_tidak_layak = [
        item["alpha"] for item in evaluated if item["consequent"] == "Tidak Layak" and item["is_active"]
    ]
    alphas_layak = [
        item["alpha"] for item in evaluated if item["consequent"] == "Layak" and item["is_active"]
    ]

    alpha_1 = max(alphas_tidak_layak) if alphas_tidak_layak else 0.0
    alpha_2 = max(alphas_layak) if alphas_layak else 0.0

    # Luas trapesium terpotong
    A1 = 25.0 * alpha_1 * (2.0 - alpha_1)
    A2 = 25.0 * alpha_2 * (2.0 - alpha_2)

    # Momen luasan terhadap titik 0
    M1 = (2500.0 / 6.0) * alpha_1 * (3.0 - 3.0 * alpha_1 + alpha_1**2)
    M2 = (2500.0 / 6.0) * alpha_2 * (9.0 - 3.0 * alpha_2 - alpha_2**2)

    total_area = A1 + A2
    total_moment = M1 + M2

    if total_area > 0.0:
        score = total_moment / total_area
    else:
        score = mid

    active_rules = [r for r in evaluated if r["is_active"]]

    return {
        "score": round(score, 4),
        "alpha_1": round(alpha_1, 4),
        "alpha_2": round(alpha_2, 4),
        "A1": round(A1, 4),
        "A2": round(A2, 4),
        "M1": round(M1, 4),
        "M2": round(M2, 4),
        "total_area": round(total_area, 4),
        "total_moment": round(total_moment, 4),
        "detailed_rules": evaluated,
        "active_rules": active_rules,
        "total_rules": len(evaluated),
        "active_count": len(active_rules)
    }

