# Protokol eksperimen ML

Salin tabel ini untuk setiap eksperimen dan isi desain sebelum membuka hasil uji.

| Bagian | Yang dicatat |
| --- | --- |
| Pertanyaan dan hipotesis | Satu kondisi yang diubah, efek yang diprediksi, dan batas klaim |
| Data | Sumber, lisensi, versi atau hash, unit pemisahan, dan distribusi per split |
| Baseline | Baseline naif dan metode pembanding yang relevan dengan literatur atau praktik |
| Metode | Komponen yang diuji, prapemrosesan, ruang pencarian, budget komputasi, dan seed |
| Evaluasi | Metrik utama, arah perbaikan, ambang efek yang berarti, metrik sekunder, dan metode estimasi ketidakpastian |
| Reproduksi | Revisi kode, versi paket dan data, konfigurasi, perintah, perangkat keras, dan lokasi artefak |
| Hasil dan keputusan | Nilai per metode dan per seed jika relevan, selisih terhadap baseline, analisis kegagalan, dan kesimpulan |

## Aturan perbandingan

- Tentukan unit split sesuai klaim generalisasi. Pisahkan berdasarkan dokumen asal, subjek, atau kasus simulasi jika satu unit menghasilkan banyak sampel. Pakai urutan waktu bila klaimnya prediksi periode berikutnya.
- Bekukan split dan fit seluruh transformasi berbasis data pada train. Gunakan validation untuk pemilihan fitur, threshold, dan hiperparameter. Buka hasil test setelah metode dan kriteria dikunci.
- Bandingkan metode pada split, metrik, dan kondisi evaluasi yang sama. Catat budget pencarian dan laporkan waktu atau komputasi jika itu bagian dari klaim.
- Untuk training stokastik, tentukan daftar seed di awal dan laporkan hasil per seed beserta ringkasannya. Untuk ketidakpastian akibat sampling, gunakan unit evaluasi independen yang sesuai dengan desain studi.
- Jika ada klaim tentang kontribusi suatu komponen, uji ablation dengan mengubah komponen itu saja sejauh desain memungkinkan. Nyatakan batas klaim jika hasil masih belum bisa membedakan hipotesis dari penjelasan lain.

## Contoh yang tersedia

Pertanyaan awal adalah apakah frekuensi kata mengungguli prediksi kelas mayoritas pada klasifikasi teks sintetis bertopik aliran dan struktur. Metrik utama adalah macro-F1. Akurasi dicatat sebagai metrik sekunder. Split sudah ditetapkan dan kedua baseline deterministik, sehingga eksperimen contoh tidak memerlukan pengulangan seed. Ukuran fixture hanya cukup untuk memeriksa alur I/O, pelatihan, dan evaluasi.
