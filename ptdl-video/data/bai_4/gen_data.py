"""Bài 4 – Sinh dữ liệu mô phỏng: MDS nước giải khát, hồi quy thuộc tính, Conjoint cà phê, Van Westendorp.

Chạy:  python gen_data.py   (tạo các file CSV cùng thư mục)
Dữ liệu hư cấu, chỉ dùng cho giảng dạy. Seed cố định nên chạy lại cho kết quả y hệt.
"""
from itertools import combinations
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 44
OUT = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# 4.1 MDS: 6 thương hiệu, vị trí "thật" lấy theo bản đồ trên slide 11
# ---------------------------------------------------------------------------
BRANDS = {"Coca-Cola": (3.47, 3.50), "Pepsi": (2.27, 3.05), "Sprite": (0.47, -1.60),
          "7Up": (-0.38, -1.85), "Fanta": (-2.95, -1.00), "Mirinda": (-2.85, -2.05)}


def gen_mds(rng, n=150):
    names = list(BRANDS)
    P = np.array([BRANDS[b] for b in names])
    pairs = list(combinations(range(6), 2))
    d = np.array([np.linalg.norm(P[i] - P[j]) for i, j in pairs])
    dmax = d.max()
    bias = rng.normal(0, 0.45, len(pairs))            # lệch nhận thức chung theo cặp (không Euclid)
    rows = []
    for r in range(1, n + 1):
        scale = rng.normal(1, 0.12)                   # mỗi người dùng thang hơi khác
        for k, (i, j) in enumerate(pairs):
            s = 9 - 8 * d[k] / dmax * scale + bias[k] + rng.normal(0, 1.0)
            rows.append((f"DV{r:03d}", names[i], names[j], int(np.clip(np.round(s), 1, 9))))
    sim = pd.DataFrame(rows, columns=["dap_vien", "thuong_hieu_1", "thuong_hieu_2", "muc_giong_nhau"])

    # Bản đồ theo thuộc tính: chấm 1–7 trên hai thuộc tính chọn sẵn
    attr_true = {"Coca-Cola": (6.4, 5.6), "Pepsi": (6.0, 5.0), "Sprite": (2.0, 4.2),
                 "7Up": (1.8, 3.6), "Fanta": (1.6, 3.4), "Mirinda": (1.7, 3.0)}
    rows = []
    for r in range(1, n + 1):
        for b in names:
            a, c = attr_true[b]
            rows.append((f"DV{r:03d}", b,
                         int(np.clip(np.round(a + rng.normal(0, 0.9)), 1, 7)),
                         int(np.clip(np.round(c + rng.normal(0, 1.1)), 1, 7))))
    att = pd.DataFrame(rows, columns=["dap_vien", "thuong_hieu", "vi_cola_dam", "cao_cap"])
    return sim, att


# ---------------------------------------------------------------------------
# 4.1.2 Hồi quy thuộc tính – ý định mua nước giải khát có ga (slide 13)
# ---------------------------------------------------------------------------
def gen_hoiquy(rng, n=400):
    cols = ["hinh_anh_thuong_hieu", "vi_va_do_ga", "san_co_tai_diem_ban",
            "cam_nhan_gia_cao", "thiet_ke_bao_bi", "khuyen_mai_diem_ban"]
    beta = np.array([0.44, 0.29, 0.26, -0.21, 0.12, 0.04]) * 1.06   # bù phần suy giảm do làm tròn thang 1–7
    S = np.full((6, 6), 0.20)
    np.fill_diagonal(S, 1.0)
    S[0, 4] = S[4, 0] = 0.35          # hình ảnh thương hiệu – bao bì
    S[3, 5] = S[5, 3] = -0.10
    X = rng.multivariate_normal(np.zeros(6), S, n)
    sig = np.sqrt(1 - beta @ S @ beta)
    y = X @ beta + rng.normal(0, sig, n)

    def likert7(z, mu=4.6, sd=1.25):
        return np.clip(np.round(mu + sd * z), 1, 7).astype(int)

    df = pd.DataFrame({c: likert7(X[:, k], mu=4.4 if c != "cam_nhan_gia_cao" else 3.9) for k, c in enumerate(cols)})
    df["y_dinh_mua"] = likert7(y, mu=4.5, sd=1.35)
    df.insert(0, "dap_vien", [f"R{i:03d}" for i in range(1, n + 1)])
    df["tuoi"] = np.clip(rng.normal(27, 7, n), 16, 60).round().astype(int)
    df["gioi_tinh"] = rng.choice(["Nữ", "Nam"], n)
    return df


# ---------------------------------------------------------------------------
# 4.2 Conjoint chuỗi cà phê: 3 thuộc tính x 3 mức, thiết kế trực giao L9, 200 đáp viên
# ---------------------------------------------------------------------------
LEVELS = {"nguon_goc": ["Ethiopia", "Colombia", "Việt Nam"],
          "bao_bi": ["Hộp cao cấp", "Túi giấy", "Hộp nhựa"],
          "gia": [45000, 60000, 75000]}
L9 = [(1, 1, 1), (1, 2, 2), (1, 3, 3), (2, 1, 2), (2, 2, 3), (2, 3, 1), (3, 1, 3), (3, 2, 1), (3, 3, 2)]
# part-worth gộp (mức thấp nhất = 0) theo slide 23
PW = {"nguon_goc": [1.39, 0.66, 0.0], "bao_bi": [1.53, 0.72, 0.0], "gia": [2.30, 1.18, 0.0]}


def gen_conjoint(rng, n=200):
    prof = pd.DataFrame([{"to_hop": k + 1,
                          "nguon_goc": LEVELS["nguon_goc"][a - 1],
                          "bao_bi": LEVELS["bao_bi"][b - 1],
                          "gia": LEVELS["gia"][c - 1]} for k, (a, b, c) in enumerate(L9)])
    rows = []
    for r in range(1, n + 1):
        a0 = rng.normal(2.35, 0.45)                         # mức "dễ tính" riêng của người chấm
        w = np.clip(1 + rng.normal(0, 0.22, 3), 0.3, None)  # khác biệt sở thích giữa người
        for k, (a, b, c) in enumerate(L9):
            u = (a0 + w[0] * PW["nguon_goc"][a - 1] + w[1] * PW["bao_bi"][b - 1]
                 + w[2] * PW["gia"][c - 1] + rng.normal(0, 0.55))
            rows.append((r, k + 1, int(np.clip(np.round(u), 1, 9))))
    df = pd.DataFrame(rows, columns=["dap_vien", "to_hop", "diem"]).merge(prof, on="to_hop")
    df = df.sort_values(["dap_vien", "to_hop"]).reset_index(drop=True)
    return prof, df[["dap_vien", "to_hop", "nguon_goc", "bao_bi", "gia", "diem"]]


# ---------------------------------------------------------------------------
# 4.3.2 Van Westendorp – giá một ly cà phê, n = 320
# ---------------------------------------------------------------------------
def gen_vw(rng, n=320):
    mu = np.array([32000, 42500, 61000, 78000])
    sd = np.array([5000, 6000, 7000, 9000])
    rho = 0.6
    C = np.full((4, 4), rho)
    np.fill_diagonal(C, 1)
    Z = rng.multivariate_normal(np.zeros(4), C, n)
    V = np.sort(mu + Z * sd, axis=1)                      # bảo đảm quá rẻ < rẻ < đắt < quá đắt
    V = (np.round(V / 1000) * 1000).astype(int)
    df = pd.DataFrame(V, columns=["qua_re", "re", "dat", "qua_dat"])
    df.insert(0, "dap_vien", [f"VW{i:03d}" for i in range(1, n + 1)])
    df["thu_nhap_trieu_thang"] = np.clip(rng.lognormal(np.log(14), 0.45, n), 4, 80).round(1)
    df["tan_suat_uong_tuan"] = rng.choice([1, 2, 3, 5, 7, 10], n, p=[.15, .2, .2, .2, .15, .1])
    return df


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    sim, att = gen_mds(rng)
    hq = gen_hoiquy(rng)
    prof, cj = gen_conjoint(rng)
    vw = gen_vw(rng)
    files = {"b4_mds_khaosat.csv": sim, "b4_danhgia_thuonghieu.csv": att, "b4_hoiquy_nuocngot.csv": hq,
             "b4_conjoint_profiles.csv": prof, "b4_conjoint_khaosat.csv": cj, "b4_vanwestendorp.csv": vw}
    for f, d in files.items():
        d.to_csv(OUT / f, index=False, encoding="utf-8-sig")
        print(f"{f:28s}{len(d):>6} dòng")
