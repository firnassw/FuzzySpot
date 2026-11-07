"""
sugeno.py
Mesin inferensi fuzzy metode Sugeno Orde-0 (Zero-Order).
Konstanta output default: Layak = 75.0, Tidak Layak = 25.0
Defuzzifikasi: z* = sum(alpha_i * k_i) / sum(alpha_i)
"""
from typing import List, Dict, Any
from rules import evaluate_rules


def calculate_sugeno(
    scores: List[float],
    rules: List[Dict[str, Any]] = None,
    weights: List[float] = None,
    a: float = 1.0,
    b: float = 5.0,
    k_layak: float = 75.0,
    k_tidak_layak: float = 25.0,
    mid: float = 50.0
) -> Dict[str, Any]:
    """
    Menghitung skor kelayakan menggunakan metode Sugeno Orde-0.
    """
    evaluated = evaluate_rules(scores, rules=rules, weights=weights, a=a, b=b)

    sum_alpha_k = 0.0
    sum_alpha = 0.0
    detailed_rules = []

    for item in evaluated:
        alpha = item["alpha"]
        consequent = item["consequent"]

        k_i = k_layak if consequent == "Layak" else k_tidak_layak
        alpha_k = alpha * k_i

        sum_alpha_k += alpha_k
        sum_alpha += alpha

        rule_detail = dict(item)
        rule_detail["k_i"] = round(k_i, 4)
        rule_detail["alpha_k"] = round(alpha_k, 6)
        detailed_rules.append(rule_detail)

    if sum_alpha > 0.0:
        score = sum_alpha_k / sum_alpha
    else:
        score = mid

    active_rules = [r for r in detailed_rules if r["is_active"]]

    return {
        "score": round(score, 4),
        "sum_alpha": round(sum_alpha, 4),
        "sum_alpha_k": round(sum_alpha_k, 4),
        "detailed_rules": detailed_rules,
        "active_rules": active_rules,
        "total_rules": len(detailed_rules),
        "active_count": len(active_rules)
    }

