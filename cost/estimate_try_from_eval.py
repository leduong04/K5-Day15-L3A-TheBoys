"""Project a 10-session simulate --try using measured per-case usage from an eval run.

This is a calibrated estimate, not a new API run. For measured simulation use
`python run.py simulate --try` with a real model configured in the ignored .env.
"""
import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "cost"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import run_eval as ev  # noqa: E402
import simulate  # noqa: E402


def main(path):
    path = path if os.path.isabs(path) else os.path.join(ROOT, path)
    with open(path, encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))
    if not rows:
        raise SystemExit("Run eval rỗng: %s" % ev.rel(path))
    run_ids = {r.get("run_id", "") for r in rows}
    if len(run_ids) != 1 or "" in run_ids:
        raise SystemExit("Run eval phải có đúng một Run ID.")
    if any(r.get("error", "").strip() for r in rows):
        raise SystemExit("Run eval có lỗi; không dùng làm mốc trung bình.")
    models = {r.get("model", "").strip() for r in rows} - {""}
    if len(models) != 1:
        raise SystemExit("Run eval cần đúng một model thật; đang có: %s" % ", ".join(sorted(models)))
    model = next(iter(models))
    def total(column):
        try:
            return sum(int(r.get(column) or 0) for r in rows)
        except ValueError:
            raise SystemExit("Cột %s không phải số nguyên." % column)

    calls = total("model_calls")
    tokens_in = total("tokens_in")
    tokens_out = total("tokens_out")
    if not calls or not tokens_in or not tokens_out:
        raise SystemExit("Run cần có số lần gọi và token > 0.")
    avg = {"calls": calls / len(rows), "in": tokens_in / len(rows), "out": tokens_out / len(rows)}

    cfg, warnings = simulate.load_config()
    bench = ev.load_items()
    plan = simulate.plan_sessions(cfg, bench, 10)
    interactions = sum(len(inputs) for _, _, inputs in plan)
    persona_counts = {}
    for _, persona, inputs in plan:
        stat = persona_counts.setdefault(persona["name"], {"sessions": 0, "turns": 0})
        stat["sessions"] += 1
        stat["turns"] += len(inputs)

    est = {key: value * interactions for key, value in avg.items()}
    prices = {p["model"].lower(): p for p in cfg["prices"]}
    observed_price = prices.get(model.lower())
    if not observed_price:
        raise SystemExit("Chưa có giá cho model đo được: %s" % model)

    lines = [
        "# Ước tính simulate --try từ lượt eval thật", "",
        "> Đây là phép chiếu theo token trung bình đo ở run eval, không phải lượt mô phỏng mới gọi API. "
        "Chạy `python run.py simulate --try` để đo thực tế từng phiên khi có API key.", "",
        "- Run nguồn: `%s` · Run ID: `%s` · model: `%s` · %d câu, không lỗi." %
        (ev.rel(path), next(iter(run_ids)), model, len(rows)),
        "- Số đo nguồn: %d token vào · %d token ra · %d lần gọi; trung bình %.1f token vào / %.1f token ra / %.3f lần gọi mỗi câu (≈ %.1f)." %
        (tokens_in, tokens_out, calls, avg["in"], avg["out"], avg["calls"], avg["calls"]),
        "- Kịch bản thử: 10 phiên theo `cost/personas.yaml`, seed %s; %d lượt hỏi tổng cộng." %
        (cfg["seed"], interactions),
        "- Phân bổ persona: " + ", ".join("%s %d phiên / %d lượt" % (name, stat["sessions"], stat["turns"])
                                          for name, stat in persona_counts.items()) + ".",
        "- Token dự phóng từ trung bình run nguồn: khoảng %.0f vào · %.0f ra · %.1f lần gọi." %
        (est["in"], est["out"], est["calls"]), "",
        "## Chi phí dự phóng cho 10 phiên", "",
        "| Model dùng để tính giá | Giá vào / ra (USD / 1M token) | Chi phí ước tính |",
        "|---|---:|---:|",
    ]
    for p in cfg["prices"]:
        usd = est["in"] * p["input"] / 1_000_000 + est["out"] * p["output"] / 1_000_000
        lines.append("| %s%s | $%s / $%s | $%.6f |" %
                     (p["model"], " (model đo token)" if p["model"].lower() == model.lower() else " (giá tham chiếu)" ,
                      p["input"], p["output"], usd))
    lines += ["", "## Giới hạn", "",
              "Run nguồn gồm đủ 24 câu benchmark, còn mô phỏng chọn ngẫu nhiên loại `thuong` và `kho`; "
              "dùng trung bình chung là ước tính gần đúng, không thay thế token đo riêng trên các đầu vào mô phỏng. "
              "Chi phí mỗi model dùng tokenization của model đo được và giá trong `cost/personas.yaml`."]
    out = os.path.join(ROOT, "cost", "run1-usage-projection.md")
    with open(out, "w", encoding="utf-8") as destination:
        destination.write("\n".join(lines) + "\n")
    print("Đã tạo %s" % ev.rel(out))
    print("%d phiên · %d lượt hỏi · %.0f token vào / %.0f ra · %.1f lần gọi dự phóng" %
          (len(plan), interactions, est["in"], est["out"], est["calls"]))
    print("Mốc: %s (%d câu)" % (next(iter(run_ids)), len(rows)))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "eval/run-1.csv")
