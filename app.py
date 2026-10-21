import pandas as pd, numpy as np, plotly.express as px, plotly.graph_objects as go
import streamlit as st
from scipy import stats

st.set_page_config(page_title="Dashboard Profil Mahasiswa", page_icon="🎓", layout="wide")
TIPE = pd.DataFrame({"Kolom": ["Jurusan", "Semester", "IPK", "Usia"],
                     "Skala": ["Nominal", "Ordinal", "Rasio (Kontinu)", "Rasio (Kontinu)"],
                     "Visualisasi yang tepat": ["Bar / Pie Chart", "Bar Chart berurutan", "Histogram / Box Plot", "Histogram / Box Plot"]})
URUT = list(range(1, 9))

@st.cache_data
def load():
    d = pd.read_csv("data_mahasiswa_sintesis.csv")
    d["Semester"] = pd.Categorical(d.Semester, categories=URUT, ordered=True)
    d["Prestasi"] = pd.cut(d.IPK, [0, 2.75, 3.0, 3.5, 3.75, 4.0], include_lowest=True,
                           labels=["<2.75", "2.75-3.00", "3.01-3.50", "3.51-3.75", "3.76-4.00"])
    return d
df = load()

st.sidebar.header("🔎 Filter")
jur = st.sidebar.multiselect("Jurusan", sorted(df.Jurusan.unique()), default=sorted(df.Jurusan.unique()))
sem = st.sidebar.slider("Rentang semester", 1, 8, (1, 8))
ipk = st.sidebar.slider("Rentang IPK", 0.0, 4.0, (float(df.IPK.min()), 4.0), step=0.05)
f = df[df.Jurusan.isin(jur) & df.Semester.astype(int).between(*sem) & df.IPK.between(*ipk)]
if f.empty:
    st.warning("Tidak ada data untuk filter ini."); st.stop()

st.title("🎓 Dashboard Profil Mahasiswa-Sherly Saskia Rani-241051002")
st.caption("Bedah Kasus 2 · Data sintesis 1.000 mahasiswa (dikembangkan dari 2 baris seed: Sistem Informasi & Manajemen)")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Jumlah Mahasiswa", f"{len(f):,}".replace(",", "."))
c2.metric("Rata² IPK", f"{f.IPK.mean():.2f}")
c3.metric("Median IPK", f"{f.IPK.median():.2f}")
c4.metric("Median Usia", f"{f.Usia.median():.0f} th")
c5.metric("Potensi Cum Laude", f"{(f.IPK >= 3.76).mean()*100:.1f}%")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏷️ Nominal (Jurusan)", "📶 Ordinal (Semester)", "📊 Kontinu (IPK & Usia)",
                                         "🔗 Korelasi & Uji", "🗂️ Data"])

with tab1:
    a, b = st.columns(2)
    j = f.Jurusan.value_counts().reset_index(); j.columns = ["Jurusan", "Jumlah"]
    a.plotly_chart(px.pie(j, names="Jurusan", values="Jumlah", hole=.45, title="Proporsi Mahasiswa per Jurusan"), width="stretch")
    b.plotly_chart(px.bar(j.sort_values("Jumlah"), x="Jumlah", y="Jurusan", orientation="h", color="Jumlah",
                          color_continuous_scale="Blues", title="Jumlah Mahasiswa per Jurusan"), width="stretch")
    m = f.groupby("Jurusan").IPK.mean().sort_values().reset_index()
    st.plotly_chart(px.bar(m, x="IPK", y="Jurusan", orientation="h", range_x=[2.5, 4], text=m.IPK.round(2),
                           title="Rata² IPK per Jurusan"), width="stretch")

with tab2:
    st.info("Semester bersifat **ordinal**: ada urutan 1 → 8, tapi jarak antar tingkat tidak bisa dianggap sama. "
            "Karena itu dipakai **bar chart berurutan** (bukan pie), dan ringkasan memakai median/modus.")
    a, b = st.columns(2)
    s = f.Semester.value_counts().reindex(URUT).fillna(0).reset_index(); s.columns = ["Semester", "Jumlah"]
    a.plotly_chart(px.bar(s, x="Semester", y="Jumlah", title="Jumlah Mahasiswa per Semester (berurutan)",
                          color_discrete_sequence=["#2a9df4"]).update_xaxes(type="category"), width="stretch")
    sj = f.groupby(["Semester", "Jurusan"], observed=True).size().reset_index(name="Jumlah")
    b.plotly_chart(px.bar(sj, x="Semester", y="Jumlah", color="Jurusan", title="Komposisi Jurusan per Semester").update_xaxes(type="category"),
                   width="stretch")
    ts = f.groupby("Semester", observed=True).agg(IPK=("IPK", "mean"), Usia=("Usia", "median")).reset_index()
    fig = go.Figure()
    fig.add_scatter(x=ts.Semester.astype(int), y=ts.IPK, name="Rata² IPK", mode="lines+markers")
    fig.add_scatter(x=ts.Semester.astype(int), y=ts.Usia, name="Median Usia", yaxis="y2", mode="lines+markers", line=dict(color="#f39c12"))
    fig.update_layout(title="IPK dan Usia per Semester", xaxis=dict(dtick=1, title="Semester"),
                      yaxis=dict(title="IPK"), yaxis2=dict(title="Usia", overlaying="y", side="right"), legend=dict(orientation="h"))
    st.plotly_chart(fig, width="stretch")

with tab3:
    a, b = st.columns(2)
    nb = st.slider("Jumlah bin histogram", 10, 50, 25)
    a.plotly_chart(px.histogram(f, x="IPK", nbins=nb, marginal="box", color_discrete_sequence=["#f39c12"],
                                title="Distribusi IPK (histogram + box plot)"), width="stretch")
    b.plotly_chart(px.histogram(f, x="Usia", nbins=nb, marginal="box", color_discrete_sequence=["#e67e22"],
                                title="Distribusi Usia (histogram + box plot)"), width="stretch")
    c, d = st.columns(2)
    c.plotly_chart(px.box(f, x="Jurusan", y="IPK", color="Jurusan", points="outliers",
                          title="Sebaran & Outlier IPK per Jurusan").update_layout(showlegend=False), width="stretch")
    d.plotly_chart(px.box(f, x="Semester", y="Usia", points="outliers", title="Sebaran & Outlier Usia per Semester")
                   .update_xaxes(type="category"), width="stretch")
    def outl(s):
        q1, q3 = s.quantile([.25, .75]); i = q3 - q1; return (s < q1 - 1.5*i) | (s > q3 + 1.5*i)
    o = f[outl(f.IPK) | outl(f.Usia)]
    st.subheader(f"Deteksi outlier (IQR): {len(o)} mahasiswa")
    st.dataframe(o.sort_values("Usia", ascending=False), width="stretch", height=220)
    dd = f[["IPK", "Usia"]].describe().T; dd["skewness"] = f[["IPK", "Usia"]].skew()
    st.dataframe(dd.round(2), width="stretch")

with tab4:
    a, b = st.columns(2)
    a.plotly_chart(px.scatter(f, x="Usia", y="IPK", color="Jurusan", opacity=.6, title="Usia vs IPK"), width="stretch")
    nf = f.assign(Semester=f.Semester.astype(int))
    cm = nf[["Semester", "IPK", "Usia"]].corr(method="spearman")
    b.plotly_chart(px.imshow(cm.round(2), text_auto=True, zmin=-1, zmax=1, color_continuous_scale="RdBu_r",
                             title="Korelasi Spearman"), width="stretch")
    r, p = stats.spearmanr(nf.Semester, nf.IPK)
    st.info(f"**Spearman Semester vs IPK:** ρ = {r:.2f} (p = {p:.3g}). Spearman dipakai karena semester ordinal.")
    if f.Jurusan.nunique() > 1:
        h, p = stats.kruskal(*[g.IPK.values for _, g in f.groupby("Jurusan")])
        st.info(f"**Kruskal-Wallis IPK antar jurusan:** H = {h:.1f}, p = {p:.3g} → "
                f"{'ada perbedaan signifikan' if p < .05 else 'tidak ada perbedaan signifikan'} (α = 0,05).")
    pr = pd.crosstab(f.Jurusan, f.Prestasi, normalize="index").mul(100).round(1)
    st.plotly_chart(px.imshow(pr, text_auto=True, aspect="auto", color_continuous_scale="Greens",
                              title="Sebaran kategori IPK per jurusan (%)"), width="stretch")

with tab5:
    st.markdown("**Tipe data tiap kolom**")
    st.table(TIPE)
    st.dataframe(f.drop(columns="Prestasi"), width="stretch", height=350)
    st.download_button("⬇️ Unduh CSV (terfilter)", f.to_csv(index=False).encode(), "mahasiswa_filtered.csv", "text/csv")
