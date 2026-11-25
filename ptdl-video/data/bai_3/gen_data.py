"""Bài 3 – Sinh dữ liệu mô phỏng cho case LUMI (chuỗi mỹ phẩm, 24 cửa hàng, Hà Nội).

Chạy:  python gen_data.py   (tạo 3 file CSV cùng thư mục)
Dữ liệu hư cấu, chỉ dùng cho giảng dạy. Seed cố định nên chạy lại cho kết quả y hệt.
"""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 2025
OUT = Path(__file__).resolve().parent
NGAY_PHAN_TICH = pd.Timestamp("2025-06-30")      # theo slide bài tập RFM
DAU_KY = pd.Timestamp("2024-07-01")              # kỳ phân tích 12 tháng


# ---------------------------------------------------------------------------
# 1. LUMI_khach_hang.csv – 3.000 dòng (2.899 khách sạch + 101 dòng lỗi)
# ---------------------------------------------------------------------------
def gen_khach_hang(rng):
    # Bốn phân khúc ẩn, quy mô theo slide "Chân dung bốn phân khúc khách hàng"
    seg = {
        #            n    R_tb  R_sd  F_tb  F_sd(log) AOV_tb   app  online  nhom_sp  tuoi
        "VIP":       (318,   9,    6,   24,  0.13,    540_000, 14, 0.45,   7.5,     33),
        "ThuongXuyen": (886, 32,    9,   11,  0.13,    436_000,  8, 0.35,   5.0,     30),
        "ThinhThoang": (1168, 95,  24,    4,  0.20,    350_000,  3, 0.25,   2.8,     28),
        "NguDong":   (527, 265,   40,    2,  0.30,    300_000, 0.8, 0.15,  1.6,     31),
    }
    rows = []
    for name, (n, r_m, r_sd, f_m, f_sd, aov, app, onl, nsp, tuoi) in seg.items():
        R = np.clip(rng.normal(r_m, r_sd, n), 0, 364).round().astype(int)
        if name == "VIP":
            R = np.clip(rng.gamma(2.0, r_m / 2.0, n), 0, 45).round().astype(int)
        F = np.maximum(1, np.round(f_m * np.exp(rng.normal(0, f_sd, n)))).astype(int)
        if name == "NguDong":
            F = rng.choice([1, 2, 3], n, p=[0.35, 0.45, 0.20])
        aov_i = aov * np.exp(rng.normal(0, 0.18, n))
        M = np.round(F * aov_i, -3)
        rows.append(pd.DataFrame({
            "_seg": name,
            "R": R, "F": F, "M": M,
            "so_phien_app_thang": rng.poisson(app, n),
            "ty_le_mua_online": np.clip(rng.beta(onl * 8, (1 - onl) * 8, n), 0, 1).round(2),
            "so_nhom_sp_da_mua": np.clip(rng.poisson(nsp, n), 1, 16),
            "so_lan_doi_tra": rng.poisson(0.04 * F),
            "tuoi": np.clip(rng.normal(tuoi, 7, n), 18, 65).round().astype(int),
        }))
    df = pd.concat(rows, ignore_index=True)
    n = len(df)
    df["gioi_tinh"] = rng.choice(["Nữ", "Nam"], n, p=[0.88, 0.12])
    df["cua_hang"] = [f"CH{k:02d}" for k in rng.integers(1, 25, n)]
    df["ngay_mua_gan_nhat"] = NGAY_PHAN_TICH - pd.to_timedelta(df["R"], unit="D")
    # ngày đăng ký thành viên: trước lần mua gần nhất, từ 2019
    lo = pd.Timestamp("2019-01-01")
    span = (df["ngay_mua_gan_nhat"] - lo).dt.days.values
    df["ngay_dang_ky"] = lo + pd.to_timedelta((rng.random(n) * span).astype(int), unit="D")
    df["so_don_12t"] = df["F"]
    df["tong_chi_tieu_12t"] = df["M"]

    # Giá trị thiếu ở biến phụ (giữ lại sau khi điền)
    df["tuoi"] = df["tuoi"].astype("float")
    df.loc[rng.choice(n, 87, replace=False), "tuoi"] = np.nan
    df["so_phien_app_thang"] = df["so_phien_app_thang"].astype("float")
    df.loc[rng.choice(n, 58, replace=False), "so_phien_app_thang"] = np.nan

    df.insert(0, "ma_kh", "")
    ids = rng.permutation(np.arange(1, 2971))           # 2.899 + 71 mã cho dòng lỗi
    df["ma_kh"] = [f"KH{i:05d}" for i in ids[:n]]

    # ---- 101 dòng lỗi -------------------------------------------------------
    extra_ids = [f"KH{i:05d}" for i in ids[n:]]          # 71 mã
    bad = []
    # (a) 26 dòng thiếu R hoặc M
    b = df.sample(26, random_state=1).copy()
    b["ma_kh"] = extra_ids[:26]
    b.iloc[:13, b.columns.get_loc("ngay_mua_gan_nhat")] = pd.NaT
    b.iloc[13:, b.columns.get_loc("tong_chi_tieu_12t")] = np.nan
    bad.append(b)
    # (b) 25 tài khoản đại lý / mua sỉ: F và M cực lớn
    b = df.sample(25, random_state=2).copy()
    b["ma_kh"] = extra_ids[26:51]
    b["so_don_12t"] = rng.integers(120, 320, 25)
    b["tong_chi_tieu_12t"] = np.round(rng.uniform(150e6, 650e6, 25), -3)
    b["ngay_mua_gan_nhat"] = NGAY_PHAN_TICH - pd.to_timedelta(rng.integers(0, 10, 25), unit="D")
    bad.append(b)
    # (c) 20 dòng sai logic: 10 ngày mua sau ngày phân tích, 10 chi tiêu âm
    b = df.sample(20, random_state=3).copy()
    b["ma_kh"] = extra_ids[51:71]
    b.iloc[:10, b.columns.get_loc("ngay_mua_gan_nhat")] = (
        NGAY_PHAN_TICH + pd.to_timedelta(rng.integers(5, 90, 10), unit="D")).values
    b.iloc[10:, b.columns.get_loc("tong_chi_tieu_12t")] = -np.round(rng.uniform(2e5, 3e6, 10), -3)
    bad.append(b)
    # (d) 30 dòng trùng lặp hoàn toàn (nhập liệu hai lần)
    bad.append(df.sample(30, random_state=4).copy())

    full = pd.concat([df] + bad, ignore_index=True)
    full = full.sample(frac=1, random_state=5).reset_index(drop=True)
    cols = ["ma_kh", "cua_hang", "gioi_tinh", "tuoi", "ngay_dang_ky", "ngay_mua_gan_nhat",
            "so_don_12t", "tong_chi_tieu_12t", "so_lan_doi_tra", "so_phien_app_thang",
            "ty_le_mua_online", "so_nhom_sp_da_mua"]
    for c in ["tuoi", "so_phien_app_thang", "tong_chi_tieu_12t"]:
        full[c] = full[c].round().astype("Int64")
    for c in ["ngay_dang_ky", "ngay_mua_gan_nhat"]:
        full[c] = pd.to_datetime(full[c]).dt.strftime("%Y-%m-%d")
    return full[cols]


# ---------------------------------------------------------------------------
# 2. LUMI_nhom_san_pham.csv – 16 nhóm sản phẩm, 4 họ ẩn
# ---------------------------------------------------------------------------
def gen_nhom_sp(rng):
    # Họ ẩn: A = chăm sóc da cơ bản (mua lặp lại), B = đặc trị/cao cấp,
    #        C = trang điểm, D = cơ thể & tóc
    nhom = [
        ("SP01", "Sữa rửa mặt", "A"), ("SP02", "Toner / nước hoa hồng", "A"),
        ("SP03", "Tẩy trang", "A"), ("SP04", "Kem chống nắng", "A"),
        ("SP05", "Mặt nạ giấy", "A"),
        ("SP06", "Serum đặc trị", "B"), ("SP07", "Kem dưỡng chống lão hoá", "B"),
        ("SP08", "Nước hoa", "B"),
        ("SP09", "Son môi", "C"), ("SP10", "Kem nền / cushion", "C"),
        ("SP11", "Phấn phủ", "C"), ("SP12", "Mascara / kẻ mắt", "C"),
        ("SP13", "Phấn má / bắt sáng", "C"),
        ("SP14", "Sữa tắm", "D"), ("SP15", "Dưỡng thể", "D"), ("SP16", "Dầu gội / xả", "D"),
    ]
    #         gia_tb(k) bien_LN  chu_ky_mua_lai  ty_le_KM  online  tuoi_KH  tang_truong  sku
    prof = {
        "A": (210,      0.42,    45,             0.30,     0.38,   26,      0.18,        60),
        "B": (780,      0.58,    120,            0.12,     0.22,   34,      0.09,        35),
        "C": (330,      0.50,    80,             0.25,     0.48,   25,      0.05,        110),
        "D": (160,      0.30,    35,             0.42,     0.30,   31,      0.02,        45),
    }
    sd = (0.12, 0.03, 0.15, 0.04, 0.04, 1.5, 0.03, 0.15)   # nhiễu (log cho giá, chu kỳ, sku)
    rec = []
    for ma, ten, h in nhom:
        g, bl, ck, km, onl, tuoi, tt, sku = prof[h]
        rec.append({
            "ma_nhom": ma, "ten_nhom": ten,
            "gia_ban_tb_nghin": round(g * np.exp(rng.normal(0, sd[0]))),
            "bien_loi_nhuan_gop": round(bl + rng.normal(0, sd[1]), 3),
            "chu_ky_mua_lai_ngay": round(ck * np.exp(rng.normal(0, sd[2]))),
            "ty_le_don_co_khuyen_mai": round(km + rng.normal(0, sd[3]), 3),
            "ty_le_mua_online": round(onl + rng.normal(0, sd[4]), 3),
            "tuoi_tb_khach": round(tuoi + rng.normal(0, sd[5]), 1),
            "tang_truong_doanh_thu_yoy": round(tt + rng.normal(0, sd[6]), 3),
            "so_sku": int(round(sku * np.exp(rng.normal(0, sd[7])))),
        })
    df = pd.DataFrame(rec)
    # doanh thu 12 tháng (tỷ đồng): thông tin mô tả, không bắt buộc đưa vào phân cụm
    df["doanh_thu_12t_ty"] = (df["gia_ban_tb_nghin"] * df["so_sku"] * 365 / df["chu_ky_mua_lai_ngay"]
                              * rng.uniform(0.8, 1.2, len(df)) / 1e4).round(2)
    return df


# ---------------------------------------------------------------------------
# 3. LUMI_diem_giao_hang.csv – 1.140 điểm giao: 6 vùng dày dọc trục đường + 141 điểm lẻ
# ---------------------------------------------------------------------------
KM_LAT = 110.57
KM_LON = 111.32 * np.cos(np.radians(21.02))


def _along_polyline(rng, pts, n, width_m):
    pts = np.array(pts)                                   # (lat, lon)
    xy = np.c_[pts[:, 1] * KM_LON, pts[:, 0] * KM_LAT]
    seg_len = np.linalg.norm(np.diff(xy, axis=0), axis=1)
    cum = np.r_[0, np.cumsum(seg_len)]
    s = rng.random(n) * cum[-1]
    k = np.searchsorted(cum, s, side="right") - 1
    k = np.clip(k, 0, len(seg_len) - 1)
    t = (s - cum[k]) / seg_len[k]
    p = xy[k] + (xy[k + 1] - xy[k]) * t[:, None]
    p += rng.normal(0, width_m / 1000, (n, 2))
    return np.c_[p[:, 1] / KM_LAT, p[:, 0] / KM_LON]


def _arc(rng, center, r_m, a0, a1, n, width_m):
    ang = np.radians(rng.uniform(a0, a1, n))
    r = r_m / 1000 + rng.normal(0, width_m / 1000, n)
    x = center[1] * KM_LON + r * np.cos(ang)
    y = center[0] * KM_LAT + r * np.sin(ang)
    return np.c_[y / KM_LAT, x / KM_LON]


def gen_diem_giao(rng):
    zones = [
        # (tên vùng ẩn, quận, n, toạ độ)
        ("V1", "Cầu Giấy", 212, _along_polyline(        # chữ L: Xuân Thủy -> Trần Duy Hưng
            rng, [(21.0372, 105.7770), (21.0362, 105.7985), (21.0090, 105.8000)], 212, 110)),
        ("V2", "Hoàn Kiếm", 159, _arc(                    # vòng cung quanh Hồ Gươm
            rng, (21.0287, 105.8524), 620, -60, 210, 159, 70)),
        ("V3", "Hai Bà Trưng", 172, _along_polyline(      # dọc Minh Khai
            rng, [(21.0005, 105.8440), (20.9985, 105.8580), (20.9955, 105.8710)], 172, 100)),
        ("V4", "Tây Hồ", 141, _along_polyline(            # cung Xuân Diệu – Quảng An
            rng, [(21.0705, 105.8235), (21.0645, 105.8290), (21.0585, 105.8322), (21.0530, 105.8338)], 141, 90)),
        ("V5", "Thanh Xuân", 196, _along_polyline(        # dọc Nguyễn Trãi
            rng, [(20.9992, 105.8235), (20.9925, 105.8100), (20.9850, 105.7955)], 196, 110)),
        ("V6", "Long Biên", 119, _along_polyline(         # dọc Nguyễn Văn Cừ
            rng, [(21.0455, 105.8695), (21.0420, 105.8855)], 119, 90)),
    ]
    dense = np.vstack([z[3] for z in zones])
    lab = np.concatenate([[z[0]] * z[2] for z in zones])
    quan = np.concatenate([[z[1]] * z[2] for z in zones])

    # 141 điểm lẻ: rải đều trong nội thành, cách mọi vùng dày ít nhất 700 m
    noise = []
    dxy = np.c_[dense[:, 1] * KM_LON, dense[:, 0] * KM_LAT]
    while len(noise) < 141:
        la, lo = rng.uniform(20.955, 21.085), rng.uniform(105.765, 105.905)
        d = np.hypot(dxy[:, 0] - lo * KM_LON, dxy[:, 1] - la * KM_LAT).min()
        if d > 0.7 and all(np.hypot((lo - b) * KM_LON, (la - a) * KM_LAT) > 0.9 for a, b in noise):
            noise.append((la, lo))
    noise = np.array(noise)
    tam_quan = {"Ba Đình": (21.0340, 105.8140), "Hoàn Kiếm": (21.0287, 105.8524),
                "Tây Hồ": (21.0680, 105.8180), "Long Biên": (21.0400, 105.8900),
                "Cầu Giấy": (21.0330, 105.7900), "Đống Đa": (21.0150, 105.8270),
                "Hai Bà Trưng": (21.0060, 105.8570), "Hoàng Mai": (20.9750, 105.8600),
                "Thanh Xuân": (20.9930, 105.8110), "Nam Từ Liêm": (21.0150, 105.7700),
                "Bắc Từ Liêm": (21.0700, 105.7750)}
    names = list(tam_quan)
    cen = np.array([tam_quan[k] for k in names])
    qn = [names[np.argmin(np.hypot((cen[:, 1] - b) * KM_LON, (cen[:, 0] - a) * KM_LAT))] for a, b in noise]

    pts = np.vstack([dense, noise])
    df = pd.DataFrame({"lat": pts[:, 0].round(6), "lon": pts[:, 1].round(6),
                       "quan": np.concatenate([quan, qn]),
                       "_vung": np.concatenate([lab, ["NHIEU"] * 141])})
    n = len(df)
    df["gia_tri_don"] = np.round(rng.lognormal(np.log(420_000), 0.45, n), -3).astype(int)
    t0 = pd.Timestamp("2025-04-01")
    df["thoi_gian_dat"] = (t0 + pd.to_timedelta(rng.integers(0, 91 * 24 * 60, n), unit="min")).strftime("%Y-%m-%d %H:%M")
    df = df.sample(frac=1, random_state=7).reset_index(drop=True)
    df.insert(0, "ma_don", [f"DH{i:05d}" for i in range(1, n + 1)])
    return df.drop(columns="_vung")


if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    kh = gen_khach_hang(rng)
    sp = gen_nhom_sp(rng)
    dg = gen_diem_giao(rng)
    kh.to_csv(OUT / "LUMI_khach_hang.csv", index=False, encoding="utf-8-sig")
    sp.to_csv(OUT / "LUMI_nhom_san_pham.csv", index=False, encoding="utf-8-sig")
    dg.to_csv(OUT / "LUMI_diem_giao_hang.csv", index=False, encoding="utf-8-sig")
    print(f"LUMI_khach_hang.csv    {len(kh):>5} dòng")
    print(f"LUMI_nhom_san_pham.csv {len(sp):>5} dòng")
    print(f"LUMI_diem_giao_hang.csv{len(dg):>5} dòng")
