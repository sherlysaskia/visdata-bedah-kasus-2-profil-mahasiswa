"""Analisis detail dataset profil mahasiswa."""
import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv("data_mahasiswa_sintesis.csv")
def judul(t): print("\n" + "="*70 + f"\n{t}\n" + "="*70)
def iqr_bounds(s):
    q1, q3 = s.quantile([.25, .75]); i = q3 - q1; return q1 - 1.5*i, q3 + 1.5*i

judul("1. KUALITAS DATA")
print(df.dtypes, "\nMissing:\n", df.isna().sum(), "\nDuplikat:", df.duplicated().sum())
print("IPK di luar 0-4:", ((df.IPK < 0) | (df.IPK > 4)).sum(), "| Semester di luar 1-8:", (~df.Semester.between(1, 8)).sum())

judul("2. NOMINAL: Jurusan")
f = df.Jurusan.value_counts(); print(pd.DataFrame({"n": f, "%": (f/len(df)*100).round(1)}))

judul("3. ORDINAL: Semester (urut)")
s = df.Semester.value_counts().sort_index()
print(pd.DataFrame({"n": s, "%": (s/len(df)*100).round(1), "kumulatif_%": (s.cumsum()/len(df)*100).round(1)}))
print("Median semester:", df.Semester.median(), "| Modus:", df.Semester.mode()[0], "(ordinal: pakai median/modus, bukan mean)")

judul("4. KONTINU: IPK & Usia")
d = df[["IPK", "Usia"]].describe().T
d["skewness"] = df[["IPK", "Usia"]].skew(); d["kurtosis"] = df[["IPK", "Usia"]].kurt()
print(d.round(2))
for c in ["IPK", "Usia"]:
    lo, hi = iqr_bounds(df[c]); o = df[(df[c] < lo) | (df[c] > hi)]
    print(f"\nOutlier {c}: batas [{lo:.2f}, {hi:.2f}] -> {len(o)} data ({len(o)/len(df)*100:.1f}%)")
    print("  nilai terekstrem:", sorted(o[c].tolist())[:3], "...", sorted(o[c].tolist())[-3:])
    p = stats.shapiro(df[c].sample(500, random_state=1))[1]
    print(f"  Shapiro p={p:.3g} -> {'normal' if p > .05 else 'tidak normal'}")

judul("5. IPK PER JURUSAN")
g = df.groupby("Jurusan").IPK.agg(["count", "mean", "median", "std", "min", "max"]).round(2)
print(g.sort_values("mean", ascending=False))
h, p = stats.kruskal(*[x.IPK.values for _, x in df.groupby("Jurusan")])
print(f"\nKruskal-Wallis IPK ~ Jurusan: H={h:.1f}, p={p:.3g} -> {'ada perbedaan signifikan' if p < .05 else 'tidak ada perbedaan signifikan'}")

judul("6. IPK & USIA PER SEMESTER (ordinal)")
print(df.groupby("Semester").agg(n=("IPK", "size"), IPK_mean=("IPK", "mean"), IPK_median=("IPK", "median"), Usia_median=("Usia", "median")).round(2))

judul("7. KORELASI (Spearman, cocok untuk ordinal)")
for a, b in [("Semester", "IPK"), ("Semester", "Usia"), ("Usia", "IPK")]:
    r, p = stats.spearmanr(df[a], df[b]); print(f"{a:9s} vs {b:5s}: rho={r:+.2f}, p={p:.3g}")

judul("8. KATEGORI PRESTASI (berdasar IPK)")
kat = pd.cut(df.IPK, [0, 2.75, 3.0, 3.5, 3.75, 4.0], labels=["<2.75 (perlu perhatian)", "2.75-3.00", "3.01-3.50 (sangat memuaskan)", "3.51-3.75", "3.76-4.00 (cum laude)"], include_lowest=True)
print(kat.value_counts().sort_index())

judul("9. SILANG JURUSAN x SEMESTER (jumlah)")
print(pd.crosstab(df.Jurusan, df.Semester, margins=True))

judul("10. INSIGHT OTOMATIS")
print(f"- Jurusan terbanyak: {f.idxmax()} ({f.max()} mhs). IPK rata-rata tertinggi: {g['mean'].idxmax()} ({g['mean'].max():.2f}).")
print(f"- IPK rata-rata {df.IPK.mean():.2f}, median {df.IPK.median():.2f}; skew {df.IPK.skew():.2f} (miring kiri karena ada IPK rendah dan batas atas 4.0).")
print(f"- Usia median {df.Usia.median():.0f} tahun; {(df.Usia > 25).sum()} mahasiswa berusia di atas 25.")
print(f"- {(df.IPK >= 3.76).sum()} mahasiswa ({(df.IPK >= 3.76).mean()*100:.1f}%) berpotensi cum laude (IPK >= 3.76).")
