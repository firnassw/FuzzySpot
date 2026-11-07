"""
tsukamoto.py
Mesin inferensi fuzzy metode Tsukamoto.
Layak: z_i = 50 + 50*alpha_i
Tidak Layak: z_i = 50 - 50*alpha_i
Defuzzifikasi: z* = sum(alpha_i * z_i) / sum(alpha_i)
"""
from typing import List, Dict, Any, Tuple
from rules import evaluate_rules, generate_rules
from membership import z_layak_tsukamoto, z_tidak_layak_tsukamoto


def calculate_tsukamoto(
    scores: List[float],
    rules: List[Dict[str, Any]] = None,
    weights: List[float] = None,
    a: float = 1.0,
    b: float = 5.0,
    min_val: float = 0.0,
    mid: float = 50.0,
    max_val: float = 100.0
) -> Dict[str, Any]:
    """
    Menghitung skor kelayakan menggunakan metode Tsukamoto.
    """
    evaluated = evaluate_rules(scores, rules=rules, weights=weights, a=a, b=b)

    sum_alpha_z = 0.0
    sum_alpha = 0.0
    detailed_rules = []

    for item in evaluated:
        alpha = item["alpha"]
        consequent = item["consequent"]

        if consequent == "Layak":
            z_i = z_layak_tsukamoto(alpha, mid=mid, max_val=max_val)
        else:
            z_i = z_tidak_layak_tsukamoto(alpha, min_val=min_val, mid=mid)

        alpha_z = alpha * z_i
        sum_alpha_z += alpha_z
        sum_alpha += alpha

        rule_detail = dict(item)
        rule_detail["z_i"] = round(z_i, 4)
        rule_detail["alpha_z"] = round(alpha_z, 6)
        detailed_rules.append(rule_detail)

    if sum_alpha > 0.0:
        score = sum_alpha_z / sum_alpha
    else:
        score = mid

    active_rules = [r for r in detailed_rules if r["is_active"]]

    return {
        "score": round(score, 4),
        "sum_alpha": round(sum_alpha, 4),
        "sum_alpha_z": round(sum_alpha_z, 4),
        "detailed_rules": detailed_rules,
        "active_rules": active_rules,
        "total_rules": len(detailed_rules),
        "active_count": len(active_rules)
    }

