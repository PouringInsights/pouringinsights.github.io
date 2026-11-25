"""Bài 4 – Lời giải tham khảo: MDS, hồi quy thuộc tính, Conjoint (part-worth, tầm quan trọng, WTP,
mô phỏng thị phần), Van Westendorp.

Chạy sau gen_data.py:  python solution.py
Cần: pandas, numpy, scikit-learn, scipy, statsmodels.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.spatial import procrustes
from sklearn.manifold import MDS

D = Path(__file__).resolve().parent
pd.set_option("display.width", 140, "display.max_columns", 20)


def tieu_de(s):
    print("\n" + "=" * 78 + f"\n{s}\n" + "=" * 78)


# ===========================================================================
# 1. MDS – bản đồ nhận thức 6 thương hiệu nước giải khát
# ===========================================================================
tieu_de("1. MDS – BẢN ĐỒ NHẬN THỨC (b4_mds_khaosat.csv)")
sim = pd.read_csv(D / "b4_mds_khaosat.csv")
names = ["Coca-Cola", "Pepsi", "Sprite", "7Up", "Fanta", "Mirinda"]
m = sim.groupby(["thuong_hieu_1", "thuong_hieu_2"])["muc_giong_nhau"].mean()
S = pd.DataFrame(9.0, index=names, columns=names)
for (a, b), v in m.items():
    S.loc[a, b] = S.loc[b, a] = v
Dis = 9 - S                                   # độ khác biệt: 0 = giống hệt
print("Ma trận độ khác biệt trung bình (9 − mức giống nhau):")
print(Dis.round(2).to_string())

try:
    mds = MDS(n_components=2, metric_mds=True, metric="precomputed", n_init=8, init="random",
              random_state=0, normalized_stress=False)
except TypeError:                              # scikit-learn < 1.8
    mds = MDS(n_components=2, dissimilarity="precomputed", metric=True, n_init=8,
              random_state=0, normalized_stress=False)
X = mds.fit_transform(Dis.values)
iu = np.triu_indices(6, 1)
delta = Dis.values[iu]
dist = np.linalg.norm(X[:, None] - X[None], axis=2)[iu]
b = (delta @ dist) / (delta @ delta)           # hệ số co giãn tối ưu
stress1 = np.sqrt(((b * delta - dist) ** 2).sum() / (dist ** 2).sum())
print("\nToạ độ MDS 2 chiều:")
print(pd.DataFrame(X, index=names, columns=["Chieu_1", "Chieu_2"]).round(2).to_string())
print(f"Kruskal Stress-1 = {stress1:.3f}  (Kruskal 1964: <0,05 tốt; 0,05–0,10 khá; >0,20 kém)")
print("Cặp gần nhau nhất:", Dis.where(np.triu(np.ones((6, 6)), 1).astype(bool)).stack().idxmin())

att = pd.read_csv(D / "b4_danhgia_thuonghieu.csv")
A = att.groupby("thuong_hieu")[["vi_cola_dam", "cao_cap"]].mean().loc[names]
print("\nBản đồ theo thuộc tính (điểm trung bình 1–7):")
print(A.round(2).to_string())
_, _, disparity = procrustes(A.values, X)
print(f"Procrustes giữa bản đồ MDS và bản đồ thuộc tính: sai lệch = {disparity:.3f} "
      "(càng gần 0 càng giống cấu trúc)")

# ===========================================================================
# 2. Hồi quy thuộc tính lên ý định mua
# ===========================================================================
tieu_de("2. HỒI QUY THUỘC TÍNH (b4_hoiquy_nuocngot.csv)")
hq = pd.read_csv(D / "b4_hoiquy_nuocngot.csv")
xs = ["hinh_anh_thuong_hieu", "vi_va_do_ga", "san_co_tai_diem_ban", "cam_nhan_gia_cao",
      "thiet_ke_bao_bi", "khuyen_mai_diem_ban"]
z = hq[xs + ["y_dinh_mua"]].apply(lambda s: (s - s.mean()) / s.std())
ols = smf.ols("y_dinh_mua ~ " + " + ".join(xs), data=z).fit()
out = pd.DataFrame({"beta_chuan_hoa": ols.params[xs], "p_value": ols.pvalues[xs]})
print(out.sort_values("beta_chuan_hoa", ascending=False).round(3).to_string())
print(f"R² = {ols.rsquared:.3f}; n = {int(ols.nobs)}")
print(f"Hình ảnh thương hiệu / Vị: {ols.params['hinh_anh_thuong_hieu'] / ols.params['vi_va_do_ga']:.2f} lần")

# ===========================================================================
# 3. Conjoint – part-worth bằng hồi quy bội với biến giả
# ===========================================================================
tieu_de("3. CONJOINT CÀ PHÊ (b4_conjoint_khaosat.csv)")
cj = pd.read_csv(D / "b4_conjoint_khaosat.csv")
print(f"{cj.dap_vien.nunique()} đáp viên × {cj.to_hop.nunique()} tổ hợp = {len(cj)} lượt đánh giá")
prof = pd.read_csv(D / "b4_conjoint_profiles.csv")
d = pd.get_dummies(prof.drop(columns="to_hop").astype(str)).astype(int)
print("Kiểm tra trực giao: tương quan lớn nhất giữa hai biến giả khác thuộc tính =",
      round(max(abs(d[a].corr(d[b])) for a in d for b in d if a.split('_')[0] != b.split('_')[0]), 3))

f = ("diem ~ C(nguon_goc, Treatment('Việt Nam')) + C(bao_bi, Treatment('Hộp nhựa'))"
     " + C(gia, Treatment(75000))")
mod = smf.ols(f, data=cj).fit()
print(f"R² = {mod.rsquared:.3f}")
levels = {"nguon_goc": ["Ethiopia", "Colombia", "Việt Nam"],
          "bao_bi": ["Hộp cao cấp", "Túi giấy", "Hộp nhựa"],
          "gia": [45000, 60000, 75000]}
ref = {"nguon_goc": "Việt Nam", "bao_bi": "Hộp nhựa", "gia": 75000}
pw = {}
for a, lv in levels.items():
    vals = []
    for l in lv:
        if l == ref[a]:
            vals.append(0.0)
        else:
            key = [k for k in mod.params.index if k.startswith(f"C({a}") and k.endswith(f"[T.{l}]")][0]
            vals.append(mod.params[key])
    pw[a] = pd.Series(vals, index=[str(x) for x in lv])

rows = []
for a, s in pw.items():
    for l, v in s.items():
        rows.append((a, l, v - s.min(), v - s.mean()))
tab = pd.DataFrame(rows, columns=["thuoc_tinh", "muc", "pw_min0", "pw_tru_trung_binh"])
print(tab.round(2).to_string(index=False))

rng_ = {a: s.max() - s.min() for a, s in pw.items()}
tot = sum(rng_.values())
print("\nTầm quan trọng tương đối (từ khoảng dao động):")
for a, r in rng_.items():
    print(f"  {a:10s} khoảng dao động {r:.2f}  ->  {r / tot * 100:.1f}%")

# WTP
vnd_per_util = (75000 - 45000) / rng_["gia"]
print(f"\n1 đơn vị utility = 30.000 / {rng_['gia']:.2f} = {vnd_per_util:,.0f} đồng")
wtp_eth = (pw["nguon_goc"]["Ethiopia"] - pw["nguon_goc"]["Việt Nam"]) * vnd_per_util
wtp_box = (pw["bao_bi"]["Hộp cao cấp"] - pw["bao_bi"]["Hộp nhựa"]) * vnd_per_util
wtp_paper = (pw["bao_bi"]["Túi giấy"] - pw["bao_bi"]["Hộp nhựa"]) * vnd_per_util
print(f"WTP thêm cho hạt Ethiopia so với Việt Nam: {wtp_eth:,.0f} đ")
print(f"WTP thêm cho hộp cao cấp so với hộp nhựa:  {wtp_box:,.0f} đ")
print(f"WTP thêm cho túi giấy so với hộp nhựa:     {wtp_paper:,.0f} đ")
print(f"Nâng cả hai (Ethiopia + hộp cao cấp): {wtp_eth + wtp_box:,.0f} đ -> vượt khoảng 30.000 đ đã khảo sát, "
      "không được ngoại suy")

# Mô phỏng thị phần logit (cấu hình đối thủ là giả định minh hoạ)
def U(o, p, g):
    return pw["nguon_goc"][o] + pw["bao_bi"][p] + pw["gia"][str(g)]


tieu_de("3b. MÔ PHỎNG THỊ PHẦN LOGIT (cấu hình đối thủ giả định)")
GIA_VON = 30000          # giả định giá vốn một ly (biên gộp 50% ở mức 60.000 đ), để tính lợi nhuận gộp
QUY_MO = 50000           # giả định số ly/tháng toàn thị trường
thi_truong = {"Ta": ("Colombia", "Túi giấy", 60000), "Đối thủ A": ("Việt Nam", "Hộp nhựa", 45000),
              "Đối thủ B": ("Ethiopia", "Hộp cao cấp", 75000), "Đối thủ C": ("Việt Nam", "Túi giấy", 60000)}
for kb, gia_ta in [("Giữ giá 60.000", 60000), ("Hạ giá 45.000", 45000)]:
    mk = dict(thi_truong)
    mk["Ta"] = ("Colombia", "Túi giấy", gia_ta)
    u = pd.Series({k: U(*v) for k, v in mk.items()})
    share = np.exp(u) / np.exp(u).sum()
    ln = share["Ta"] * QUY_MO * (gia_ta - GIA_VON) / 1e6
    print(f"{kb}: " + " | ".join(f"{k} {v * 100:.1f}%" for k, v in share.items())
          + f"  -> lợi nhuận gộp của ta ≈ {ln:,.0f} triệu đ/tháng")

# ===========================================================================
# 4. Van Westendorp
# ===========================================================================
tieu_de("4. VAN WESTENDORP (b4_vanwestendorp.csv)")
vw = pd.read_csv(D / "b4_vanwestendorp.csv")
print(f"n = {len(vw)}; vi phạm thứ tự quá rẻ<rẻ<đắt<quá đắt: "
      f"{(~((vw.qua_re <= vw.re) & (vw.re <= vw.dat) & (vw.dat <= vw.qua_dat))).sum()} dòng")
p = np.arange(15000, 110001, 50)
too_cheap = np.array([(vw.qua_re >= x).mean() for x in p])   # đường giảm
cheap = np.array([(vw.re >= x).mean() for x in p])           # đường giảm
expensive = np.array([(vw.dat <= x).mean() for x in p])      # đường tăng
too_exp = np.array([(vw.qua_dat <= x).mean() for x in p])    # đường tăng


def giao(a, b):
    diff = a - b
    i = np.where(np.sign(diff[:-1]) != np.sign(diff[1:]))[0][0]
    t = diff[i] / (diff[i] - diff[i + 1])
    return p[i] + t * (p[i + 1] - p[i])


PMC = giao(too_cheap, expensive)
PME = giao(cheap, too_exp)
OPP = giao(too_cheap, too_exp)
IPP = giao(cheap, expensive)
print(f"PMC (quá rẻ ∩ đắt)        = {PMC:,.0f} đ")
print(f"OPP (quá rẻ ∩ quá đắt)    = {OPP:,.0f} đ")
print(f"IPP (rẻ ∩ đắt)            = {IPP:,.0f} đ")
print(f"PME (rẻ ∩ quá đắt)        = {PME:,.0f} đ")
print(f"Vùng giá chấp nhận được: {PMC:,.0f} – {PME:,.0f} đ")
# Biến thể thường gặp (SurveyMonkey, nhiều phần mềm): dùng đường 'không rẻ' = 1 − rẻ, 'không đắt' = 1 − đắt
PMC2 = giao(too_cheap, 1 - cheap)
PME2 = giao(too_exp, 1 - expensive)
print(f"Biến thể 'không rẻ / không đắt': PMC = {PMC2:,.0f} đ, PME = {PME2:,.0f} đ")

print("\nTham chiếu với Conjoint: mức 60.000 đ nằm",
      "TRONG" if PMC <= 60000 <= PME else "NGOÀI", "vùng giá chấp nhận được.")
