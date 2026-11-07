"""
membership.py
Fungsi keanggotaan fuzzy linear monoton untuk input kriteria dan himpunan output kelayakan.
"""

def mu_rendah(x: float, a: float = 1.0, b: float = 5.0) -> float:
    """
    Fungsi keanggotaan linear turun untuk kriteria input.
    mu_rendah = (b - x) / (b - a), diclamp pada [0.0, 1.0].
    """
    if b == a:
        return 1.0 if x <= a else 0.0
    val = (b - x) / (b - a)
    return min(1.0, max(0.0, float(val)))


def mu_tinggi(x: float, a: float = 1.0, b: float = 5.0) -> float:
    """
    Fungsi keanggotaan linear naik untuk kriteria input.
    mu_tinggi = (x - a) / (b - a), diclamp pada [0.0, 1.0].
    """
    if b == a:
        return 1.0 if x >= a else 0.0
    val = (x - a) / (b - a)
    return min(1.0, max(0.0, float(val)))


def mu_output_tidak_layak(z: float, min_val: float = 0.0, mid: float = 50.0) -> float:
    """
    Fungsi keanggotaan output 'Tidak Layak' (turun dari 1.0 di 0.0 ke 0.0 di 50.0).
    """
    if mid == min_val:
        return 1.0 if z <= min_val else 0.0
    val = (mid - z) / (mid - min_val)
    return min(1.0, max(0.0, float(val)))


def mu_output_layak(z: float, mid: float = 50.0, max_val: float = 100.0) -> float:
    """
    Fungsi keanggotaan output 'Layak' (naik dari 0.0 di 50.0 ke 1.0 di 100.0).
    """
    if max_val == mid:
        return 1.0 if z >= max_val else 0.0
    val = (z - mid) / (max_val - mid)
    return min(1.0, max(0.0, float(val)))


def z_layak_tsukamoto(alpha: float, mid: float = 50.0, max_val: float = 100.0) -> float:
    """
    Invers fungsi keanggotaan Layak untuk metode Tsukamoto:
    alpha = (z - mid) / (max_val - mid) => z = mid + alpha * (max_val - mid)
    Default: z = 50.0 + 50.0 * alpha
    """
    return mid + (max_val - mid) * alpha


def z_tidak_layak_tsukamoto(alpha: float, min_val: float = 0.0, mid: float = 50.0) -> float:
    """
    Invers fungsi keanggotaan Tidak Layak untuk metode Tsukamoto:
    alpha = (mid - z) / (mid - min_val) => z = mid - alpha * (mid - min_val)
    Default: z = 50.0 - 50.0 * alpha
    """
    return mid - (mid - min_val) * alpha

