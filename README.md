# GenAI

Kerangka kerja eksperimen machine learning yang dapat direproduksi. Notebook yang sudah ada tersedia di [quickstarts/](quickstarts/).

## Jalankan eksperimen pertama

Dari root repo, gunakan Python 3.10+ tanpa dependensi pihak ketiga.

```sh
python -m research.run --config configs/text_baseline.json --split validation --output runs/text-validation.json
```

Contoh ini melatih Naive Bayes multinomial pada data teks sintetis dan membandingkannya dengan prediksi kelas mayoritas. Keduanya dilatih pada split `train` dan dievaluasi pada `validation` yang sama. Output JSON memuat jumlah sampel, akurasi, macro-F1, prediksi per sampel, konfigurasi, hash data dan kode, versi Python, serta revisi Git jika tersedia. Data sintetis berfungsi untuk memeriksa alur eksperimen.

Setelah metode dan kriteria evaluasi dibekukan, jalankan evaluasi akhir dengan `--split test --output runs/text-test.json`. Setiap run memerlukan nama output baru.

## Mulai studi baru

1. Isi [protokol eksperimen](docs/protokol-riset.md) dengan pertanyaan, hipotesis, baseline, metrik utama, dan kriteria keberhasilan.
2. Catat sumber, versi, lisensi, dan unit pemisahan data. Lakukan preprocessing yang mempelajari statistik hanya pada data latih.
3. Jalankan baseline, pilih metode dengan split validasi, lalu evaluasi metode final pada split uji. Catat variasi antar-seed bila training bersifat stokastik.
4. Simpan konfigurasi, rujukan ke artefak, dan interpretasi hasil, termasuk hasil negatif.

| Lokasi | Isi |
| --- | --- |
| `docs/protokol-riset.md` | Template per eksperimen dan protokol evaluasi |
| `configs/text_baseline.json` | Konfigurasi contoh |
| `data/text_fixture.csv` | Dataset sintetis dengan split tetap |
| `research/run.py` | Pelatihan dan evaluasi baseline |
| `runs/` | Hasil lokal dalam JSON |
