# FuzzySpot — Panduan Logo Ringkas

## 1. Logo
- **Ide**: dua fungsi keanggotaan fuzzy linear-halus (Low turun, High naik) saling menyilang. Titik silangnya (node) adalah "spot": nilai di mana dua himpunan fuzzy bertemu dan keputusan ditentukan. Garis tebal berujung bulat menjaga karakter modern seperti dashboard SaaS.
- **Versi**: horizontal (utama) · stacked · simbol saja · monokrom hitam · latar gelap (reversed) · app badge 64×64
- **File**: `*.svg` untuk web dan cetak (master vektor) · `png/` untuk dokumen dan slide · `web/` untuk favicon dan ikon aplikasi

## 2. Ruang bebas
Sisakan ruang kosong **¼ tinggi simbol** di keempat sisi logo. Jangan menaruh teks atau tepi gambar di dalam zona ini.

## 3. Ukuran minimum
| Versi | Layar | Cetak |
|---|---|---|
| Horizontal | 160 px lebar | 30 mm lebar |
| Stacked | 120 px lebar | 25 mm lebar |
| Simbol penuh | 32 px | 8 mm |
| Simbol kecil (`fuzzyspot-symbol-small.svg`, garis lebih tebal, node disederhanakan) | 16 px | 5 mm |

Di bawah 32 px selalu pakai `fuzzyspot-symbol-small.svg` (favicon, tab browser).

## 4. Warna
| Nama | HEX | RGB | CMYK (perkiraan) |
|---|---|---|---|
| Royal Indigo (primer) | #3B28CC | 59, 40, 204 | 71, 80, 0, 20 |
| Warm Coral (aksen) | #E07A5F | 224, 122, 95 | 0, 46, 58, 12 |
| Deep Indigo Black (teks) | #1E1B2E | 30, 27, 46 | 35, 41, 0, 82 |
| Warm Pastel Peach (latar UI) | #FFE8DC | 255, 232, 220 | 0, 9, 14, 0 |
| Border Peach | #F3D5C5 | 243, 213, 197 | 0, 12, 19, 5 |
| Pure White | #FFFFFF | 255, 255, 255 | 0, 0, 0, 0 |

CMYK dihitung otomatis dari RGB; cek ulang dengan profil printer sebelum cetak massal. Pantone belum ditetapkan.

**Pasangan latar yang disetujui**
- Warna penuh di atas putih, `#F5F6F8`, atau Warm Pastel Peach `#FFE8DC` (latar Navigation Rail)
- Versi reversed (`*-reversed.svg`) di atas `#1E1B2E`
- Versi hitam (`*-black.svg`) untuk printer hitam-putih, fotokopi, stempel
- App badge (`fuzzyspot-badge-64.svg`) untuk pojok sidebar atau avatar; di atas foto atau latar ramai, taruh logo di dalam kotak putih atau gelap polos

## 5. Tipografi
- Wordmark: **Plus Jakarta Sans Bold (700)**, sudah dikonversi menjadi path (SIL Open Font License)
- Teks antarmuka aplikasi: Plus Jakarta Sans atau Inter, tidak dipakai di dalam logo
- Jangan mengetik ulang wordmark; selalu pakai file logo

## 6. Jangan
- Jangan meregangkan, memiringkan, atau memutar logo
- Jangan mengubah warna di luar palet atau menukar warna kedua kurva (indigo = turun, koral = naik)
- Jangan menambah gradien, glow, bayangan, atau efek 3D
- Jangan memakai simbol penuh di bawah 32 px
- Jangan memindah atau mengubah ukuran bagian lockup (simbol dan teks)
- Jangan menaruh versi warna penuh di atas latar `#1E1B2E`; pakai versi reversed

## 7. Catatan teknis
- Semua SVG berisi path murni (tanpa teks hidup, gambar raster, filter, atau mask). Kurva sudah dikonversi menjadi outline, bukan stroke.
- Versi hitam memakai lubang asli di node dan celah di sekeliling node, jadi aman untuk stiker potong dan cetak satu warna; kedua kurva menjadi satu bentuk.
- Versi reversed memakai kurva putih (menggantikan indigo) dan garis sedikit lebih tipis (22 vs 24 satuan) untuk mengimbangi efek irradiasi di latar gelap.
- Favicon dan ikon PWA memakai ubin Warm Pastel Peach supaya tetap terbaca di tab gelap. `apple-touch-icon.png` memakai latar putih.
- `theme-color` di `web/head-snippet.html` diset ke Royal Indigo `#3B28CC`.
- Pencarian merek dagang dan pemeriksaan kemiripan belum dilakukan.
