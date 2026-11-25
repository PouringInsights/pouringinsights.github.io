"""Finalize MCQ JSON: reshuffle options (seeded) so answer letters are balanced and unpredictable,
keep numeric options ascending, keep questions whose options cite other letters, remap renumbered sections.
usage: mcq_finalize.py <scripts_dir>   -> writes bN_mcq_final.json
"""
import json, random, re, sys
D = sys.argv[1]
REMAP = {3: {"3.3.2": "3.1.2"}}          # Bài 3: RFM renumbered on the slides
L = "ABCD"
num = lambda s: re.fullmatch(r"[\s≈~−\-+]*[\d.,]+\s*(%|đ|đồng|triệu|lần|ngày|tháng)?[\s.]*", s.strip()) is not None

def balanced(rng, n):
    while True:
        base = list(L) * (n // 4) + rng.sample(L, n % 4)
        rng.shuffle(base)
        if all(not (base[i] == base[i+1] == base[i+2]) for i in range(n - 2)): return base

for n in [1, 3, 4, 5, 6, 7, 8]:
    rng = random.Random(1000 + n)
    qs = json.load(open(f"{D}/b{n}_mcq.json", encoding="utf-8"))
    for _ in range(500):
        target = balanced(rng, len(qs)); out = []
        for q, t in zip(qs, target):
            q = dict(q); opts = [q[k] for k in L]; correct = q[q["dap_an"]]
            locked = re.search(r"\b(phương án|đáp án) [ABCD]\b|\b[ABCD] và [ABCD]\b", " ".join(opts))
            if locked:
                pass
            elif all(num(o) for o in opts):
                def key(o):
                    v = re.sub(r"[^\d,.\-−]", "", o).replace(".", "").replace(",", ".").replace("−", "-")
                    try: return float(v)
                    except ValueError: return 0
                opts = sorted(opts, key=key)
            else:
                others = [o for o in opts if o != correct]; rng.shuffle(others)
                i = L.index(t); opts = others[:i] + [correct] + others[i:]
            for k, o in zip(L, opts): q[k] = o
            q["dap_an"] = L[opts.index(correct)]
            q["muc"] = REMAP.get(n, {}).get(q["muc"], q["muc"])
            out.append(q)
        seq = "".join(q["dap_an"] for q in out); cnt = {c: seq.count(c) for c in L}
        if min(cnt.values()) >= 4 and max(cnt.values()) <= 7 and not re.search(r"(.)\1\1", seq): break
    json.dump(out, open(f"{D}/b{n}_mcq_final.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(n, seq, cnt)
