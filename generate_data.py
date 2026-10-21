"""Membangkitkan 1000 data sintesis profil mahasiswa dari 2 baris seed Bedah Kasus 2."""
import numpy as np, pandas as pd
rng = np.random.default_rng(7)

# (jurusan, bobot populasi, rata2 IPK, sebaran IPK)
JURUSAN = [
    ("Sistem Informasi",       .20, 3.35, .30),   # seed
    ("Manajemen",              .20, 3.25, .32),   # seed
    ("Teknik Informatika",     .16, 3.20, .35),
    ("Akuntansi",              .14, 3.30, .30),
    ("Psikologi",              .10, 3.45, .25),
    ("Hukum",                  .08, 3.15, .33),
    ("Desain Komunikasi Visual", .07, 3.40, .28),
    ("Teknik Sipil",           .05, 3.05, .38),
]
names = [j[0] for j in JURUSAN]
w = np.array([j[1] for j in JURUSAN]); w = w / w.sum()
# semester 1..8 (ordinal): mahasiswa semester awal lebih banyak
sem_w = np.array([.19, .17, .16, .14, .12, .10, .07, .05]); sem_w /= sem_w.sum()

N = 1000
ji = rng.choice(len(JURUSAN), N, p=w)
sem = rng.choice(np.arange(1, 9), N, p=sem_w)

# Usia (tahun): ~18 + (semester-1)/2 + noise, sebagian kecil mahasiswa lebih tua (outlier alami)
usia = 18 + (sem - 1) / 2 + rng.normal(0.6, 0.8, N)
tua = rng.random(N) < 0.025
usia[tua] += rng.integers(4, 15, tua.sum())
usia = np.clip(np.round(usia), 17, 45).astype(int)

# IPK 0-4: rata2 per jurusan + naik tipis seiring semester, batas atas 4.00
mu = np.array([JURUSAN[i][2] for i in ji]) + 0.025 * (sem - 4)
sd = np.array([JURUSAN[i][3] for i in ji])
ipk = np.clip(rng.normal(mu, sd * .75), 1.5, 4.0)
rendah = rng.random(N) < 0.02                     # sebagian kecil IPK rendah (outlier bawah)
ipk[rendah] = rng.uniform(1.5, 2.2, rendah.sum())
ipk = np.round(ipk, 2)

df = pd.DataFrame({"Jurusan": [names[i] for i in ji], "Semester": sem, "IPK": ipk, "Usia": usia})
df.loc[0] = ["Sistem Informasi", 3, 3.85, 20]     # seed 1 (asli)
df.loc[1] = ["Manajemen", 1, 3.50, 19]            # seed 2 (asli)
df.to_csv("data_mahasiswa_sintesis.csv", index=False)
print(df.head(), "\nBaris:", len(df))
