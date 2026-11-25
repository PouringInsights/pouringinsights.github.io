"""Bài 5 – Sinh dữ liệu mô phỏng case NAVIO (hộp thực phẩm tươi, thu phí hằng tháng) và bài tập slide 10.

Chạy:  python gen_data.py   (tạo các file CSV cùng thư mục)
Dữ liệu hư cấu, chỉ dùng cho giảng dạy. Seed cố định nên chạy lại cho kết quả y hệt.

Cơ chế sinh dữ liệu bám đúng "dữ liệu cohort thực tế" trong slide:
  tỷ lệ rời bỏ 25% (tháng 1), 12% (tháng 2–3), 7% (tháng 4–6), 4% (từ tháng 7)
  ARPU 450.000 đ (tháng 1–3), 560.000 đ (tháng 4–6), 680.000 đ (từ tháng 7)
Rời bỏ được nhân thêm hệ số theo kênh thu hút; cohort từ 01/2025 có onboarding mới
nên rời bỏ tháng 1–3 thấp hơn.
"""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 55
OUT = Path(__file__).resolve().parent
THANG_DAU = pd.Period("2022-07", "M")
THANG_CUOI = pd.Period("2025-06", "M")        # ngày phân tích 30/06/2025

KENH = {  # tỷ trọng khách mới, CAC mục tiêu (đ), hệ số rời bỏ
    "Giới thiệu bạn bè": (0.20, 400_000, 0.70),
    "Google Search":     (0.20, 900_000, 0.90),
    "Facebook/TikTok Ads": (0.45, 1_000_000, 1.10),
    "KOL/Influencer":    (0.15, 1_200_000, 1.30),
}


def hazard(t, cohort):
    if t == 1:
        h = 0.25
    elif t <= 3:
        h = 0.12
    elif t <= 6:
        h = 0.07
    else:
        h = 0.04
    if cohort >= pd.Period("2025-01", "M") and t <= 3:   # onboarding mới
        h *= 0.72
    return h


def arpu(t):
    return 450_000 if t <= 3 else (560_000 if t <= 6 else 680_000)


def main():
    rng = np.random.default_rng(SEED)
    kenh_names = list(KENH)
    p_kenh = [KENH[k][0] for k in kenh_names]
    cohorts = pd.period_range(THANG_DAU, THANG_CUOI, freq="M")
    kh_rows, gd_rows = [], []
    idx = 0
    for i, c in enumerate(cohorts):
        n = int(rng.normal(190 + 4 * i, 18))
        for _ in range(n):
            idx += 1
            ma = f"NV{idx:05d}"
            kenh = rng.choice(kenh_names, p=p_kenh)
            mult = KENH[kenh][2]
            ho = rng.choice(["1-2 người", "3-4 người", "5+ người"], p=[0.35, 0.50, 0.15])
            hs_ho = {"1-2 người": 0.85, "3-4 người": 1.05, "5+ người": 1.25}[ho]
            ca_nhan = np.exp(rng.normal(0, 0.10)) / np.exp(0.005)
            kh_rows.append((ma, str(c), kenh, rng.choice(["Hà Nội", "TP.HCM"], p=[0.45, 0.55]), ho))
            t, m = 1, c
            while m <= THANG_CUOI:
                # doanh thu tháng: ARPU theo tuổi đời × quy mô hộ (chuẩn hoá về trung bình 1) × nhiễu
                dt = arpu(t) * hs_ho / 1.01 * ca_nhan * np.exp(rng.normal(0, 0.08) - 0.0032)
                gd_rows.append((ma, str(m), int(round(dt, -3))))
                if rng.random() < min(0.95, hazard(t, c) * mult):
                    break
                t += 1
                m += 1
    kh = pd.DataFrame(kh_rows, columns=["ma_kh", "thang_gia_nhap", "kenh_thu_hut", "thanh_pho", "quy_mo_ho"])
    gd = pd.DataFrame(gd_rows, columns=["ma_kh", "thang", "doanh_thu"])

    # Chi phí thu hút theo kênh (tổng 36 tháng) – CAC = chi phí / số khách mới
    cp = kh.groupby("kenh_thu_hut").size().rename("so_kh_moi").reset_index()
    cp["chi_phi_thu_hut"] = [int(round(KENH[k][1] * n * rng.uniform(0.97, 1.03), -6))
                             for k, n in zip(cp["kenh_thu_hut"], cp["so_kh_moi"])]
    cp = cp[["kenh_thu_hut", "chi_phi_thu_hut", "so_kh_moi"]]

    # Bài tập slide 10: ứng dụng học tiếng Anh (số liệu lấy nguyên từ slide)
    bt = pd.DataFrame({
        "phan_khuc": ["Champions", "Loyal", "Potential", "At Risk", "Hibernating"],
        "so_kh": [180, 340, 520, 410, 630],
        "doanh_thu_kh_6_thang": [2_760_000, 1_620_000, 780_000, 1_140_000, 300_000],
        "ty_le_roi_bo_thang": [0.020, 0.035, 0.060, 0.110, 0.170],
    })

    kh.to_csv(OUT / "NAVIO_khach_hang.csv", index=False, encoding="utf-8-sig")
    gd.to_csv(OUT / "NAVIO_giao_dich.csv", index=False, encoding="utf-8-sig")
    cp.to_csv(OUT / "NAVIO_chi_phi_kenh.csv", index=False, encoding="utf-8-sig")
    bt.to_csv(OUT / "bai_tap_app_tieng_anh.csv", index=False, encoding="utf-8-sig")
    for f, d in [("NAVIO_khach_hang.csv", kh), ("NAVIO_giao_dich.csv", gd),
                 ("NAVIO_chi_phi_kenh.csv", cp), ("bai_tap_app_tieng_anh.csv", bt)]:
        print(f"{f:28s}{len(d):>7} dòng")


if __name__ == "__main__":
    main()
