# FuzzySpot - SPK Fuzzy Inference Dashboard

Aplikasi Fuzzy Inference untuk Pemilihan Tempat Nongkrong. Mengimplementasikan dan membandingkan 3 metode (Tsukamoto, Sugeno Orde-0, dan Mamdani Centroid) berbasis Python dan Streamlit dengan antarmuka interaktif, transparan, dan bertema Apple iPadOS Split-View & Google Stitch Design System.

---

## Fitur Utama

- **Multi-Model Inference**:
  - **Tsukamoto**: Monotonik linear dengan defuzzifikasi rata-rata terbobot (*weighted average*).
  - **Sugeno Orde-0**: Singleton output berbobot konstan (`z_Tidak Layak = 25`, `z_Layak = 75`).
  - **Mamdani Centroid**: Agregasi max-min analitik dengan defuzzifikasi titik berat (*Center of Gravity*).
- **5 Kriteria Keputusan**:
  - C1: Harga (skor 1-5, benefit)
  - C2: Fasilitas (skor 1-5, benefit)
  - C3: Jarak (skor 1-5, benefit)
  - C4: Kenyamanan (skor 1-5, benefit)
  - C5: Jam Operasional (skor 1-5, benefit)
- **Visualisasi Kurva Keanggotaan Reaktif**:
  - Kurva fungsi keanggotaan input dan output interaktif menggunakan Plotly.
  - Parameter kurva dapat disesuaikan secara dinamis (*live update*).
- **Desain Modern**:
  - Tipografi Plus Jakarta Sans dan JetBrains Mono.
  - Navigasi tablet iPadOS Split-View tanpa emoji, berbasis SVG dan Unicode glyphs.

---

## Struktur Repositori

```text
├── assets/
│   └── logo/             # Brand kit vektor & raster FuzzySpot
├── tests/
│   └── test_fuzzy.py     # Unit tests untuk ketiga model inferensi
├── .streamlit/
│   └── config.toml       # Konfigurasi server & tema Streamlit
├── app.py                # Aplikasi dashboard utama
├── membership.py         # Fungsi keanggotaan fuzzy
├── tsukamoto.py          # Logika inferensi Tsukamoto
├── sugeno.py             # Logika inferensi Sugeno Orde-0
├── mamdani.py            # Logika inferensi Mamdani Centroid
├── rules.py              # Basis aturan fuzzy (32 rules)
├── compare.py            # Modul perbandingan model
├── style.css             # Desain custom CSS iPadOS / Stitch
├── requirements.txt      # Dependensi Python
└── README.md
```

---

## Cara Menjalankan

### 1. Kloning Repositori
```bash
git clone https://github.com/firnassw/FuzzySpot.git
cd FuzzySpot
```

### 2. Instal Dependensi
```bash
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi
```bash
streamlit run app.py
```

Buka peramban pada tautan lokal `http://localhost:8501`.

---

## Pengujian Unit

Jalankan test suite menggunakan pytest:
```bash
pytest tests/test_fuzzy.py
```
Semua unit test memvalidasi batas kurva, akurasi derajat keanggotaan, evaluasi aturan inferensi, dan nilai defuzzifikasi ketiga model.
