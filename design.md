# Dokumen Desain UI/UX (`design.md`)

**Proyek:** Aplikasi Fuzzy Inference untuk Pemilihan Tempat Nongkrong (Project 2 SCPK 2026)

**Target Platform:** Web Lokal (Streamlit + Custom CSS / Component Styling)

**Versi Desain:** 2.0 (Gaya *Apple iPadOS Split-View & Pastel Cards* Berdasarkan Referensi)

---

## 1. Referensi Gaya Visual & Inspirasi UI/UX (iPadOS Style)

Berdasarkan referensi antarmuka aplikasi medis iPadOS yang bersih dan modern, gaya visual aplikasi ini mengadopsi **"Soft Pastel Split-View Dashboard"**. Karakteristik utamanya meliputi:

1. **Multi-Column Navigation (Split-View):**
   * **Kolom Kiri (Sidebar/Navigation Pane):** Berwarna latar pastel lembut (`#FDF4F2` atau `#FAF0EE`) dengan sudut melengkung halus (*rounded container*), memuat daftar alternatif tempat nongkrong layaknya daftar pasien (*Patients list* di referensi).
   * **Kolom Tengah/Utama (Main Content Pane):** Berwarna latar putih bersih (`#FFFFFF`) dengan *border-radius* besar (khas jendela aplikasi iPadOS), tempat tabel interaktif, grafik, dan rincian langkah perhitungan ditampilkan.

2. **Skema Warna Lembut & Elegan (Soft Pastel Palette):**
   * Menggantikan warna primer yang terlalu mencolok dengan palet warna pastel yang menenangkan mata, sangat ideal untuk presentasi di depan dosen tanpa membuat silau.
   * Aksen kartu menggunakan efek *soft shadow* dan *subtle borders* (`1px solid rgba(0,0,0,0.06)`).

3. **Kartu List & Badge Status Interaktif:**
   * Setiap item alternatif atau rule memiliki *card container* terpisah dengan ikon status kecil (misal: badge hijau untuk "Layak", merah untuk "Tidak Layak", dan indikator metode).
   * Kolom pencarian (*Search bar*) dan filter cepat di bagian atas untuk memudahkan navigasi instan saat demo.

---

## 2. Sistem Desain (Design System)

### 2.1 Palet Warna & Variabel Visual (iPadOS Theme)

| Kategori Elemen | Nama Warna / Tema | Kode Hex | Penggunaan Utama di UI / Plotly |
| :--- | :--- | :--- | :--- |
| **Background Aplikasi** | *Soft Lavender / Slate* | `#EEEDF2` | Latar belakang global layar (luar jendela aplikasi) |
| **Background Sidebar** | *Warm Rose Pastel* | `#F7EBE8` | Panel navigasi kiri (daftar alternatif & pemilih metode) |
| **Background Konten Utama** | *Pure White Card* | `#FFFFFF` | Area jendela utama di sebelah kanan |
| **Aksen Utama (Tsukamoto)**| *Indigo Modern* | `#4F46E5` | Tombol utama, bar chart Tsukamoto, badge aktif |
| **Aksen Sugeno** | *Teal Emerald* | `#0D9488` | Bar chart dan badge metode Sugeno |
| **Aksen Mamdani** | *Amber Warm* | `#D97706` | Bar chart dan badge metode Mamdani |
| **Status Layak (Positif)** | *Soft Emerald Green* | `#10B981` | Badge skor tinggi / rule Layak |
| **Status Tidak Layak** | *Soft Coral Red* | `#EF4444` | Badge skor rendah / rule Tidak Layak |

### 2.2 Tipografi & Format Angka

* **Font Antarmuka:** `SF Pro Display`, `Inter`, atau `Plus Jakarta Sans` (mengikuti standar antarmuka Apple).
* **Font Angka & Tabel:** `JetBrains Mono` agar angka desimal $\mu$, $\alpha$, dan skor $z^*$ lurus sejajar.
* **Format Pembulatan Layar:**
  * Skor Akhir ($z^*$): **2 desimal** (contoh: `65,00`, `58,99`).
  * Derajat Keanggotaan ($\mu$ & $\alpha$): **3 desimal** (contoh: `0,250`, `0,500`).

---

## 3. Arsitektur Tata Letak Aplikasi (Split-View Layout)

Layout utama dibagi menjadi dua panel utama yang menyerupai antarmuka aplikasi tablet profesional:

```
+-----------------------------------------------------------------------------------+
| [PANEL KIRI: Sidebar Navigasi & Alternatif (#F7EBE8)]                             |
|                                                                                   |
|   [Cari Tempat Nongkrong...        ]                                            |
|                                                                                   |
|   PILIH METODE INFERENSI                                                        |
|     (•) Tsukamoto (Utama)                                                         |
|     ( ) Sugeno Orde-0                                                             |
|     ( ) Mamdani Centroid                                                          |
|                                                                                   |
|   DAFTAR ALTERNATIF (Klik untuk Sorot Detail)                                   |
|     +-----------------------------------------+                                   |
|     | ☕ Kalis Donut               [#1]       |                                   |
|     |    Fasilitas: 5.0 | Kenyamanan: 5.0     |                                   |
|     +-----------------------------------------+                                   |
|     |  Torte                     [#2]       |                                   |
|     |    Jam Buka: 5.0  | Harga: 4.0          |                                   |
|     +-----------------------------------------+                                   |
|     |  Anindita                  [#3]       |                                   |
|     | ☕ Cosan                     [#4]       |                                   |
|                                                                                   |
|  ⚙️ [x] Mode Presentasi Tablet   [ Reset]                                       |
+-----------------------------------------------------------------------------------+
| [PANEL KANAN: Area Konten Utama Tabbed View (#FFFFFF)]                            |
|                                                                                   |
|   [ Tab 1: Data & Bobot ] [ Tab 2: Kurva Fuzzy ] [ Tab 3: Proses Hitung ] ...     |
|   -----------------------------------------------------------------------------   |
|                                                                                   |
|   [ Konten Dinamis Tab Aktif Berbentuk Kotak Kartu Ber-shadow Halus ]             |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 4. Rincian Tampilan per Tab (iPadOS Card Style)

### Tab 1: Data & Bobot (` Data Alternatif & Bobot Kriteria`)
* **Desain Kartu:** Tabel input dibungkus dalam kontainer kartu putih dengan sudut melengkung (`border-radius: 12px`).
* **Komponen:** Di sebelah kanan tabel data, terdapat ringkasan bobot kriteria berbentuk *progress bar* melengkung horizontal (menyerupai *Activity Rings* Apple) untuk menampilkan persentase C1 sampai C5.

### Tab 2: Fungsi Keanggotaan (` Kurva Fuzzy & Parameter`)
* **Desain Kartu:** Menampilkan dua kartu grafik berdampingan (Input di kiri, Output terbelah di kanan).
* **Kontrol Interaktif:** Panel pengatur batas input $[a, b]$ disembunyikan di dalam *collapsible card* minimalis agar layar tidak penuh, lengkap dengan tombol geser nilai tengah output.

### Tab 3: Proses Hitung Langkah demi Langkah (` Rincian Step-by-Step`)
* **Desain Kartu:** Dibagi menjadi 3 tahapan akordeon (*Fuzzifikasi* $\rightarrow$ *Evaluasi 32 Rule* $\rightarrow$ *Defuzzifikasi*).
* **Kotak Rumus:** Menggunakan kotak latar belakang abu-abu terang (`#F9F9FB`) dengan border tipis untuk merender persamaan LaTeX (`st.latex`) secara elegan.

### Tab 4: Hasil & Simulasi What-If (` Peringkat & Playground What-If`)
* **Kartu Pemenang (Hero Card):** Di bagian atas, sebuah kartu pastel hijau lembut menampilkan rekomendasi tempat terbaik beserta alasan singkatnya (misal: *"Kalis Donut unggul di Fasilitas dan Kenyamanan"*).
* **Kolom What-If:** Slider interaktif untuk menggeser nilai kriteria secara *real-time* diletakkan di panel samping kartu hasil.

### Tab 5: Perbandingan Metode (`⚖️ Komparasi Lintas Metode`)
* **Desain Kartu:** Grafik *Grouped Bar Chart* dengan warna pastel kontras untuk Tsukamoto, Sugeno, dan Mamdani, diikuti tabel komparasi terhadap metode SAW (Asli vs Terkoreksi).

### Tab 6: Analisis Lanjut & Validasi (` Sensitivitas & Validasi Manual`)
* **Desain Kartu:** Menampilkan panel validasi otomatis dengan ikon centang hijau (`✅`) yang membuktikan selisih hitungan kode dan manual di bawah $0,001$, serta tombol unduh CSV berukuran besar yang estetis.

---

## 5. Pedoman Implementasi CSS Kustom di Streamlit

Untuk menduplikasi gaya iPadOS ini ke dalam Streamlit (`app.py`), gunakan injeksi CSS global berikut:

```python
st.markdown("""
<style>
    /* Mengubah background utama aplikasi */
    .stApp {
        background-color: #EEEDF2;
    }
    /* Styling kontainer kartu putih ala iPadOS */
    div.st-emotion-cache-1r6slb0, div[data-testid="stVerticalBlock"] > div {
        border-radius: 12px;
    }
    /* Warna latar sidebar pastel */
    section[data-testid="stSidebar"] {
        background-color: #F7EBE8;
    }
    /* Styling tombol */
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)
```