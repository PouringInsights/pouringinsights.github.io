"""Bài 3 – Lời giải tham khảo case LUMI (RFM, K-means, Hierarchical/Ward, DBSCAN).

Chạy sau gen_data.py:  python solution.py
Cần: pandas, numpy, scikit-learn, scipy.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster, cophenet
from scipy.spatial.distance import pdist
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

D = Path(__file__).resolve().parent
NGAY_PHAN_TICH = pd.Timestamp("2025-06-30")
pd.set_option("display.width", 140, "display.max_columns", 20)


def tieu_de(s):
    print("\n" + "=" * 78 + f"\n{s}\n" + "=" * 78)


# ===========================================================================
# YÊU CẦU 1. Làm sạch dữ liệu khách hàng
# ===========================================================================
tieu_de("YÊU CẦU 1. LÀM SẠCH LUMI_khach_hang.csv")
kh = pd.read_csv(D / "LUMI_khach_hang.csv", parse_dates=["ngay_dang_ky", "ngay_mua_gan_nhat"])
print("Số dòng ban đầu:", len(kh))
print("Giá trị thiếu theo cột:\n", kh.isna().sum()[kh.isna().sum() > 0].to_string())

n0 = len(kh)
kh = kh.drop_duplicates()
print(f"(a) Bỏ dòng trùng lặp hoàn toàn: -{n0 - len(kh)}")
n0 = len(kh)
kh = kh.dropna(subset=["ngay_mua_gan_nhat", "tong_chi_tieu_12t"])
print(f"(b) Bỏ dòng thiếu ngày mua gần nhất hoặc tổng chi tiêu (không tính được R/M): -{n0 - len(kh)}")
n0 = len(kh)
kh = kh[(kh["ngay_mua_gan_nhat"] <= NGAY_PHAN_TICH) & (kh["tong_chi_tieu_12t"] > 0)]
print(f"(c) Bỏ dòng sai logic (ngày mua sau ngày phân tích, chi tiêu âm): -{n0 - len(kh)}")

# (d) Ngoại lệ: quy tắc IQR trên thang log (phân phối F, M lệch phải mạnh)
n0 = len(kh)
mask = pd.Series(True, index=kh.index)
for c in ["so_don_12t", "tong_chi_tieu_12t"]:
    x = np.log(kh[c])
    q1, q3 = x.quantile([0.25, 0.75])
    up = q3 + 1.5 * (q3 - q1)
    mask &= x <= up
    print(f"    ngưỡng trên {c}: {np.exp(up):,.0f}")
kh = kh[mask].copy()
print(f"(d) Bỏ ngoại lệ (tài khoản mua sỉ) theo IQR trên log(F), log(M): -{n0 - len(kh)}")

# (e) Điền giá trị thiếu ở biến phụ bằng trung vị
for c in ["tuoi", "so_phien_app_thang"]:
    print(f"(e) Điền {kh[c].isna().sum()} giá trị thiếu ở '{c}' bằng trung vị = {kh[c].median():.0f}")
    kh[c] = kh[c].fillna(kh[c].median())
print("Số khách hàng sau làm sạch:", len(kh))

# ===========================================================================
# YÊU CẦU 2a. RFM theo ngũ phân vị
# ===========================================================================
tieu_de("YÊU CẦU 2a. CHẤM ĐIỂM RFM (ngày phân tích 30/06/2025, kỳ 12 tháng)")
kh["R"] = (NGAY_PHAN_TICH - kh["ngay_mua_gan_nhat"]).dt.days
kh["F"] = kh["so_don_12t"]
kh["M"] = kh["tong_chi_tieu_12t"]
# rank(method="first") để tránh lỗi trùng ngưỡng khi F có nhiều giá trị giống nhau
kh["R_diem"] = pd.qcut(kh["R"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1]).astype(int)
kh["F_diem"] = pd.qcut(kh["F"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
kh["M_diem"] = pd.qcut(kh["M"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
kh["ma_RFM"] = kh["R_diem"].astype(str) + kh["F_diem"].astype(str) + kh["M_diem"].astype(str)


def nhan_rfm(r, f, m):
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    if r >= 3 and f >= 4 and m >= 4:
        return "Trung thành"
    if r >= 4 and f <= 2:
        return "Khách mới / Tiềm năng"
    if r <= 2 and f >= 3 and m >= 3:
        return "At Risk"
    if r <= 2 and f <= 2:
        return "Hibernating / Lost"
    return "Cần theo dõi"


kh["phan_khuc_RFM"] = [nhan_rfm(*v) for v in kh[["R_diem", "F_diem", "M_diem"]].values]
tb = kh.groupby("phan_khuc_RFM").agg(so_KH=("ma_kh", "size"), R_tb=("R", "mean"),
                                      F_tb=("F", "mean"), M_tb_trieu=("M", lambda s: s.mean() / 1e6))
tb["ty_trong_DT_%"] = kh.groupby("phan_khuc_RFM")["M"].sum() / kh["M"].sum() * 100
print(tb.round(1).sort_values("M_tb_trieu", ascending=False).to_string())

# Bài tập slide 12: chấm 5 khách theo ngưỡng ngũ phân vị của toàn bộ tệp LUMI
print("\nBài tập slide 12 (chấm theo ngưỡng ngũ phân vị của tệp LUMI):")
bt = pd.DataFrame({"ma": ["KH01", "KH02", "KH03", "KH04", "KH05"],
                   "ngay": pd.to_datetime(["2025-06-25", "2025-06-02", "2025-01-18", "2025-06-28", "2024-12-03"]),
                   "F": [14, 9, 6, 2, 4], "M": [12.4e6, 7.8e6, 5.1e6, 0.9e6, 3.2e6]})
bt["R"] = (NGAY_PHAN_TICH - bt["ngay"]).dt.days
qR = kh["R"].quantile([.2, .4, .6, .8]).values
qF = kh["F"].quantile([.2, .4, .6, .8]).values
qM = kh["M"].quantile([.2, .4, .6, .8]).values
bt["R_diem"] = 5 - np.searchsorted(qR, bt["R"], side="left")
bt["F_diem"] = 1 + np.searchsorted(qF, bt["F"], side="left")
bt["M_diem"] = 1 + np.searchsorted(qM, bt["M"], side="left")
bt["phan_khuc"] = [nhan_rfm(*v) for v in bt[["R_diem", "F_diem", "M_diem"]].values]
print(bt[["ma", "R", "F", "M", "R_diem", "F_diem", "M_diem", "phan_khuc"]].to_string(index=False))

# ===========================================================================
# YÊU CẦU 2b. K-means trên R, log F, log M đã chuẩn hoá
# ===========================================================================
tieu_de("YÊU CẦU 2b. K-MEANS: CHỌN K BẰNG ELBOW + SILHOUETTE")
X = np.c_[kh["R"], np.log1p(kh["F"]), np.log1p(kh["M"])]
Xs = StandardScaler().fit_transform(X)
kq = []
for k in range(2, 9):
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(Xs)
    kq.append((k, km.inertia_, silhouette_score(Xs, km.labels_)))
kq = pd.DataFrame(kq, columns=["K", "inertia", "silhouette"])
print(kq.round(3).to_string(index=False))
k_best = int(kq.loc[kq["silhouette"].idxmax(), "K"])
print("K có Silhouette cao nhất:", k_best)

km = KMeans(n_clusters=4, n_init=10, random_state=42).fit(Xs)
kh["cum"] = km.labels_
prof = kh.groupby("cum").agg(so_KH=("ma_kh", "size"), R_tb=("R", "mean"), F_tb=("F", "mean"),
                             M_tb_trieu=("M", lambda s: s.mean() / 1e6),
                             app_tb=("so_phien_app_thang", "mean"),
                             online_tb=("ty_le_mua_online", "mean"),
                             nhom_sp_tb=("so_nhom_sp_da_mua", "mean"),
                             tuoi_tb=("tuoi", "mean"))
prof["ty_trong_DT_%"] = kh.groupby("cum")["M"].sum() / kh["M"].sum() * 100
prof = prof.sort_values("M_tb_trieu", ascending=False)
prof.insert(0, "ten_cum", ["VIP", "Thường xuyên", "Thỉnh thoảng", "Ngủ đông"])
print("\nChân dung 4 cụm (K = 4):")
print(prof.round(2).to_string())
print(f"Silhouette K = 4: {silhouette_score(Xs, km.labels_):.3f}")

# ===========================================================================
# YÊU CẦU 3. Hierarchical (Ward) cho 16 nhóm sản phẩm
# ===========================================================================
tieu_de("YÊU CẦU 3. HIERARCHICAL CLUSTERING (WARD) – 16 NHÓM SẢN PHẨM")
sp = pd.read_csv(D / "LUMI_nhom_san_pham.csv")
feat = ["gia_ban_tb_nghin", "bien_loi_nhuan_gop", "chu_ky_mua_lai_ngay", "ty_le_don_co_khuyen_mai",
        "ty_le_mua_online", "tuoi_tb_khach", "tang_truong_doanh_thu_yoy", "so_sku"]
Z = StandardScaler().fit_transform(sp[feat])
L = linkage(Z, method="ward")
c, _ = cophenet(L, pdist(Z))
print(f"Hệ số tương quan cophenetic: {c:.3f}")
print("Chiều cao 5 lần hợp nhất cuối (khoảng nhảy lớn = chỗ cắt):", np.round(L[-5:, 2], 2))
for k in range(2, 7):
    print(f"  {k} họ: silhouette = {silhouette_score(Z, fcluster(L, k, 'maxclust')):.3f}")
sp["ho"] = fcluster(L, 4, "maxclust")
for h, g in sp.groupby("ho"):
    print(f"Họ {h}: {', '.join(g['ten_nhom'])}")
print(sp.groupby("ho")[feat].mean().round(2).to_string())

# ===========================================================================
# YÊU CẦU 4. DBSCAN trên toạ độ giao hàng
# ===========================================================================
tieu_de("YÊU CẦU 4. DBSCAN – ĐIỂM GIAO HÀNG")
dg = pd.read_csv(D / "LUMI_diem_giao_hang.csv")
coords = np.radians(dg[["lat", "lon"]].values)
R_TD = 6371.0088
# k-distance (k = MinPts) để chọn eps
from sklearn.neighbors import NearestNeighbors
nn = NearestNeighbors(n_neighbors=12, metric="haversine").fit(coords)
kd = np.sort(nn.kneighbors(coords)[0][:, -1] * R_TD * 1000)
print("k-distance (k=12), phân vị 50/80/88/90/95 (m):", np.percentile(kd, [50, 80, 88, 90, 95]).round(0))
db = DBSCAN(eps=0.5 / R_TD, min_samples=12, metric="haversine", algorithm="ball_tree").fit(coords)
dg["vung"] = db.labels_
n_vung = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
print(f"eps = 500 m, MinPts = 12 -> {n_vung} vùng, {np.sum(db.labels_ == -1)} điểm nhiễu "
      f"({np.mean(db.labels_ == -1) * 100:.1f}%)")
print(dg[dg.vung >= 0].groupby("vung").agg(so_don=("ma_don", "size"),
      quan=("quan", lambda s: s.mode()[0])).to_string())

# So sánh với K-means K = 6 trên toạ độ phẳng (km)
xy = np.c_[dg["lon"] * 111.32 * np.cos(np.radians(21.02)), dg["lat"] * 110.57]
kmg = KMeans(n_clusters=6, n_init=10, random_state=42).fit(xy)
s_km = silhouette_score(xy, kmg.labels_)
core = dg.vung.values >= 0
s_db = silhouette_score(xy[core], dg.vung.values[core])
s_db_all = silhouette_score(xy, dg.vung.values)
print(f"Silhouette K-means (K=6, mọi điểm): {s_km:.3f}")
print(f"Silhouette DBSCAN, coi nhóm nhiễu là một nhãn (mọi điểm): {s_db_all:.3f}")
print(f"Silhouette DBSCAN, chỉ tính điểm thuộc vùng (bỏ nhiễu): {s_db:.3f}")


def km_xa_nhat(labels, mask=None):
    out = []
    for l in np.unique(labels):
        if l == -1:
            continue
        p = xy[labels == l]
        out.append(pdist(p).max())
    return np.round(out, 1)


print("Khoảng cách xa nhất giữa 2 đơn trong cùng một vùng (km):")
print("  K-means:", km_xa_nhat(kmg.labels_))
print("  DBSCAN :", km_xa_nhat(dg.vung.values))

# ===========================================================================
# YÊU CẦU 5. Gợi ý số liệu cho khuyến nghị
# ===========================================================================
tieu_de("YÊU CẦU 5. MỘT VÀI CON SỐ DÙNG CHO KHUYẾN NGHỊ")
vip = prof.iloc[0]
print(f"Cụm VIP: {vip['so_KH']:.0f} KH ({vip['so_KH'] / len(kh) * 100:.1f}% số khách) "
      f"tạo {vip['ty_trong_DT_%']:.1f}% doanh thu 12 tháng.")
ar = kh[kh.phan_khuc_RFM == "At Risk"]
print(f"At Risk (RFM): {len(ar)} KH, doanh thu 12 tháng {ar['M'].sum() / 1e9:.2f} tỷ đồng. "
      f"Kéo lại 20% nhóm này giữ được khoảng {0.2 * ar['M'].sum() / 1e9:.2f} tỷ đồng/năm.")
print(f"Đơn nhiễu (giao lẻ): {np.sum(db.labels_ == -1)} đơn, nên giao qua đối tác vận chuyển ngoài.")
