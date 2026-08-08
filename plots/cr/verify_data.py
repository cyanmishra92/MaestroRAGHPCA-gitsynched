#!/usr/bin/env python3
"""
verify_data.py -- Task 7 Part B: prove the regenerated panels plot the original values.

regen_figures.py writes plotted_values.json, a record of every number it handed to a
plotting call, per panel. This script re-loads the ORIGINAL scripts in a fresh process,
rebuilds the expected values independently of regen_figures, and diffs the two.

A panel passes only if every value matches exactly. Any difference at all is a failure,
however much better the panel looks.

Usage:  python3 plots/cr/verify_data.py        (exit 0 = all panels pass)
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _origdata as O  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "plotted_values.json")


def col(df, name):
    return [float(v) for v in df[name]]


def by(recs, xkey, huekey, vkey):
    xs, hues = [], []
    for r in recs:
        if r[xkey] not in xs:
            xs.append(r[xkey])
        if r[huekey] not in hues:
            hues.append(r[huekey])
    out = {}
    for h in hues:
        out[str(h)] = [next((r[vkey] for r in recs if r[xkey] == x and r[huekey] == h), None)
                       for x in xs]
    return xs, [str(h) for h in hues], out


def expected():
    e = {}
    ns = O.load("pieChart.py")
    e["stacked_graph"] = {"stages": ns["stages"], "startup": list(ns["startup"]),
                          "execution": list(ns["execution"]), "grand_total": ns["grand_total"]}
    d = O.load("FwdPassBS.py")["df_8cores"]
    e["forwardpass_8cores"] = {"x": col(d, "Batch Size"), "y": col(d, "Latency (s)")}
    d = O.load("FwdPass.py")["df_bs16"]
    e["forwardpass_bs16_range_discrete"] = {"x": col(d, "# Cores"),
                                            "min": col(d, "Min Latency (s)"),
                                            "max": col(d, "Max Latency (s)")}
    d = O.load("stackedLatencyMotivation.py")["df_batch"]
    e["batchsize_stacked_linear_labeled"] = {"x": col(d, "Batch Size"),
                                             "index_fetch": col(d, "Index Fetch (s)"),
                                             "similarity_search": col(d, "Similarity Search (s)"),
                                             "ylim": 15}
    c = O.load("CharacterizationPlot1.py")
    e["latency_cores"] = {"x": col(c["df_cores"], "# Cores"), "y": col(c["df_cores"], "Latency(s)")}
    e["latency_dbsize"] = {"x": col(c["df_dbsize"], "DB Size (M)"),
                           "y": col(c["df_dbsize"], "Latency(s)")}

    s9 = O.load("SpeedUpPlot4090.py")
    for key, name in (("data_ours", "4090LatencyOurs"), ("data_edge", "4090speedupEdgeRAG"),
                      ("data_flash", "4090speedupFlashRAG"), ("data_pipe", "4090speedupPipeRAG")):
        xs, hues, table = by(s9[key], "Batch Size", "DB Size", "Latency")
        e[name] = {"batch_sizes": xs, "db_sizes": hues, "values": table}
    s8 = O.load("AllSpeedup4080.py")
    xs, hues, table = by(s8["data_ours_4080"], "Batch Size", "DB Size", "Latency")
    e["4080Latency_MaestroRAG"] = {"batch_sizes": xs, "db_sizes": hues, "values": table}
    xs, hues, table = by(s8["data_speedup_merged"], "Batch Size", "Implementation", "Speedup")
    e["4080Speedup_Merged"] = {"batch_sizes": xs, "baselines": hues, "values": table}

    d = O.load("JetsonThemVsUs.py")["df"]
    e["JetsonThemVsUs"] = {"batch_sizes": col(d, "Batch Size"), "EdgeRAG": col(d, "EdgeRAG"),
                           "MaestroRAG": col(d, "MaestroRAG"), "Speedup": col(d, "Speedup")}

    recs = O.load("mapping.py")["data"]
    e["cores_allocation_stacked"] = {
        f"{r['DB Size']}/{r['Method']}": {"Batch Size": r["Batch Size"], "Encode": r["Encode"],
                                          "Retrieve": r["Retrieve"],
                                          "Total": r["Encode"] + r["Retrieve"]}
        for r in recs}

    recs = O.load("mainLatencyResult2.py")["data_main"]
    e["MainLatencyResults2"] = {f"{r['Device']}/{r['Implementation']}": r["Latency"]
                                for r in recs
                                if r["Implementation"] != "MaestroRAG w/ Cache"
                                or r["Device"] == "4090"}
    recs = O.load("goodput.py")["data_main"]
    e["ThroughputResults"] = {f"{r['Device']}/{r['Implementation']}": r["Throughput"]
                              for r in recs}
    return e


def norm(v):
    if isinstance(v, dict):
        return {str(k): norm(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [norm(x) for x in v]
    if isinstance(v, bool) or v is None:
        return v
    if isinstance(v, (int, float)):
        return None if v != v else round(float(v), 10)  # NaN -> None
    return str(v)


def main():
    if not os.path.exists(MANIFEST):
        print("plotted_values.json missing; run regen_figures.py first", file=sys.stderr)
        return 2
    got = json.load(open(MANIFEST, encoding="utf-8"))
    exp = expected()
    fails = 0
    print(f"{'panel':<36} {'result':<8} detail")
    for name in sorted(exp):
        if name not in got:
            print(f"{name:<36} {'FAIL':<8} not present in the manifest")
            fails += 1
            continue
        a, b = norm(got[name]), norm(exp[name])
        if a == b:
            n = sum(1 for _ in json.dumps(b).split(",")) if isinstance(b, dict) else len(b)
            print(f"{name:<36} {'PASS':<8} identical to the original script's arrays")
        else:
            print(f"{name:<36} {'FAIL':<8} regenerated {a}")
            print(f"{'':<36} {'':<8} original    {b}")
            fails += 1
    extra = [k for k in got if k not in exp]
    if extra:
        print(f"\npanels in the manifest with no expectation: {extra}")
        fails += len(extra)
    print(f"\n{len(exp) - fails}/{len(exp)} panels match the original data exactly")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
