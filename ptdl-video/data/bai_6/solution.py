"""Bài 6 – Lời giải tham khảo case MỘC AN: EFA 6 bước, Cronbach's Alpha, phân khúc theo tâm lý học
bằng K-means trên điểm nhân tố, đối chiếu nhân khẩu học.

Chạy sau gen_data.py:  python solution.py
Cần: pandas, numpy, factor_analyzer, scikit-learn, statsmodels.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Tương thích: factor_analyzer 0.5.1 gọi check_array(force_all_finite=...), tham số này đã bị
# scikit-learn >= 1.8 đổi tên thành ensure_all_finite. Bọc lại để chạy được với cả hai phiên bản.
import factor_analyzer.factor_analyzer as _fa_mod
_check_array_goc = _fa_mod.check_array


def _check_array(*a, **kw):
    try:
        return _check_array_goc(*a, **kw)
    except TypeError:
        if "force_all_finite" in kw:
            kw["ensure_all_finite"] = kw.pop("force_all_finite")
        return _check_array_goc(*a, **kw)


_fa_mod.check_array = _check_array

D = Path(__file__).resolve().parent
pd.set_option("display.width", 160, "display.max_columns", 30)


def tieu_de(s):
    print("\n" + "=" * 78 + f"\n{s}\n" + "=" * 78)


def cronbach(x):
    k = x.shape[1]
    return k / (k - 1) * (1 - x.var(ddof=1).sum() / x.sum(axis=1).var(ddof=1))


df = pd.read_csv(D / "MOCAN_khaosat.csv")
dic = pd.read_csv(D / "MOCAN_bien_quan_sat.csv")
items = dic.loc[dic.vai_tro == "EFA", "ma_bien"].tolist()
X = df[items]
print(f"n = {len(df)} đáp viên, {len(items)} biến quan sát đưa vào EFA")


def chay_efa(X, k, in_bang=True):
    fa = FactorAnalyzer(n_factors=k, rotation="varimax", method="principal")
    fa.fit(X)
    L = pd.DataFrame(fa.loadings_, index=X.columns, columns=[f"NT{i + 1}" for i in range(k)])
    L["communality"] = fa.get_communalities()
    var = fa.get_factor_variance()
    if in_bang:
        show = L.copy()
        for c in show.columns[:-1]:
            show[c] = show[c].where(show[c].abs() >= 0.30)       # ẩn hệ số tải < 0,30
        print(show.round(2).fillna("").to_string())
        print("Phương sai giải thích (%):", np.round(var[1] * 100, 1),
              f"| tích luỹ {var[2][-1] * 100:.1f}%")
    return fa, L


# ---------------------------------------------------------------------------
tieu_de("BƯỚC 1. KIỂM TRA ĐIỀU KIỆN: KMO VÀ BARTLETT")
kmo_item, kmo = calculate_kmo(X)
chi2, p = calculate_bartlett_sphericity(X)
print(f"KMO = {kmo:.3f} (ngưỡng ≥ 0,6; lý tưởng > 0,8)")
print(f"Bartlett: Chi² = {chi2:,.1f}, p {'< 0,001' if p < 0.001 else '= ' + format(p, '.3f')}")
print("KMO từng biến thấp nhất:", pd.Series(kmo_item, index=items).nsmallest(3).round(3).to_dict())

tieu_de("BƯỚC 2–3. TRÍCH NHÂN TỐ (PCA) VÀ CHỌN SỐ NHÂN TỐ")
fa0 = FactorAnalyzer(n_factors=len(items), rotation=None, method="principal").fit(X)
ev, _ = fa0.get_eigenvalues()
print("Eigenvalue 8 giá trị đầu:", np.round(ev[:8], 2))
k = int((ev > 1).sum())
print(f"Số nhân tố có eigenvalue > 1 (tiêu chuẩn Kaiser): {k}")

tieu_de(f"BƯỚC 4–5. XOAY VARIMAX VỚI {k} NHÂN TỐ, LỌC BIẾN ({len(items)} biến)")
fa, L = chay_efa(X, k)
nt = L.columns[:-1]
loai = []
for v, r in L.iterrows():
    a = r[nt].abs().sort_values(ascending=False)
    ly_do = []
    if r["communality"] < 0.5:
        ly_do.append(f"communality {r['communality']:.2f} < 0,5")
    if a.iloc[0] < 0.5:
        ly_do.append(f"hệ số tải lớn nhất {a.iloc[0]:.2f} < 0,5")
    if a.iloc[1] > 0.4:
        ly_do.append(f"tải chéo {a.iloc[0]:.2f} / {a.iloc[1]:.2f}")
    if ly_do:
        loai.append(v)
        print(f"Loại {v} ({dic.set_index('ma_bien').loc[v, 'noi_dung']}): {'; '.join(ly_do)}")

tieu_de(f"CHẠY LẠI EFA SAU KHI LOẠI {', '.join(loai)} ({len(items) - len(loai)} biến)")
items2 = [i for i in items if i not in loai]
X2 = df[items2]
print(f"KMO = {calculate_kmo(X2)[1]:.3f}")
fa2, L2 = chay_efa(X2, k)

tieu_de("BƯỚC 6. ĐẶT TÊN VÀ KIỂM TRA ĐỘ TIN CẬY (Cronbach's Alpha > 0,7)")
nhom = {c: [] for c in L2.columns[:-1]}
for v, r in L2.iterrows():
    nhom[r[L2.columns[:-1]].abs().idxmax()].append(v)
TEN = {"CL": "Độ bền sản phẩm", "GT": "Giá trị kinh tế", "TN": "Trải nghiệm cửa hàng",
       "TH": "Hình ảnh thương hiệu", "PC": "Phong cách thiết kế"}
ten_nt = {}
for c, vs in nhom.items():
    ten = TEN[pd.Series([v[:2] for v in vs]).mode()[0]]
    ten_nt[c] = ten
    print(f"{c} = {ten:22s} biến {', '.join(vs):26s} alpha = {cronbach(df[vs]):.3f}")

# ---------------------------------------------------------------------------
tieu_de("PHÂN KHÚC THEO TÂM LÝ HỌC: K-MEANS TRÊN ĐIỂM NHÂN TỐ")
sc = pd.DataFrame(fa2.transform(X2), columns=[ten_nt[c] for c in L2.columns[:-1]])
kq = []
for kk in range(2, 9):
    km = KMeans(n_clusters=kk, n_init=20, random_state=42).fit(sc)
    kq.append((kk, km.inertia_, silhouette_score(sc, km.labels_)))
print(pd.DataFrame(kq, columns=["K", "inertia", "silhouette"]).round(3).to_string(index=False))
km = KMeans(n_clusters=4, n_init=20, random_state=42).fit(sc)
df["phan_khuc"] = km.labels_
prof = sc.groupby(df["phan_khuc"]).mean()
prof["so_dv"] = df["phan_khuc"].value_counts().sort_index()
print("\nĐiểm nhân tố trung bình theo phân khúc (K = 4):")
print(prof.round(2).to_string())


def dat_ten(r):
    top = r.drop("so_dv").idxmax()
    return {"Giá trị kinh tế": "Săn ưu đãi", "Độ bền sản phẩm": "Thực dụng, chuộng độ bền",
            "Hình ảnh thương hiệu": "Ưa thương hiệu & phong cách", "Phong cách thiết kế": "Ưa thương hiệu & phong cách",
            "Trải nghiệm cửa hàng": "Cần trải nghiệm tại cửa hàng"}[top]


df["ten_phan_khuc"] = df["phan_khuc"].map(prof.apply(dat_ten, axis=1))
print("\nĐối chiếu với nhân khẩu học và hành vi (tỷ lệ % theo hàng):")
for c in ["nhom_tuoi", "thu_nhap", "kenh_mua_chinh"]:
    ct = pd.crosstab(df["ten_phan_khuc"], df[c], normalize="index") * 100
    thu_tu = {"thu_nhap": ["Dưới 10 triệu", "10-20 triệu", "20-35 triệu", "Trên 35 triệu"]}
    if c in thu_tu:
        ct = ct[thu_tu[c]]
    print(ct.round(0).to_string(), "\n")
print(df.groupby("ten_phan_khuc")[["so_lan_mua_12t", "chi_tieu_12t_nghin"]].mean().round(1).to_string())

# ---------------------------------------------------------------------------
tieu_de("NỐI SANG BÀI 7: HỒI QUY Ý ĐỊNH MUA LẠI LÊN ĐIỂM NHÂN TỐ")
df["YD"] = df[["YD1", "YD2", "YD3"]].mean(axis=1)
print(f"Cronbach's Alpha thang YD = {cronbach(df[['YD1', 'YD2', 'YD3']]):.3f}")
ols = sm.OLS((df["YD"] - df["YD"].mean()) / df["YD"].std(), sm.add_constant(sc)).fit()
print(pd.DataFrame({"beta": ols.params.drop("const"), "p": ols.pvalues.drop("const")}).round(3).to_string())
print(f"R² = {ols.rsquared:.3f}. Giá trị kinh tế không phải đòn bẩy mạnh nhất của ý định mua lại.")

# Đối chiếu với nhãn ẩn (chỉ khi có file đáp án của giảng viên)
f = D / "_dap_an_phan_khuc_an.csv"
if f.exists():
    from sklearn.metrics import adjusted_rand_score
    an = pd.read_csv(f)
    print(f"\n[GV] Adjusted Rand Index so với phân khúc ẩn: {adjusted_rand_score(an['phan_khuc_an'], df['phan_khuc']):.3f}")
