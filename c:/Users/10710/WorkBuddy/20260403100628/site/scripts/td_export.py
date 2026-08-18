#!/usr/bin/env python3
"""Export a Tencent Docs sheet to a local file via the MCP helper.

Usage:
    python td_export.py <file_id> <output_path>

Polls manage.export_progress until done, then downloads the signed file_url.
"""
import sys
import time
import json
import urllib.request
import subprocess
import os

TENCENTDOCS_PY = (os.environ.get("TENCENTDOCS_PY")
                   or r"C:\Users\10710\AppData\Local\Programs\WorkBuddy\resources\app.asar.unpacked\resources\builtin-plugins\tencent-docs-plugin\skills\tencent-docs\tencentdocs.py")
PY = r"C:\Users\10710\.workbuddy\binaries\python\versions\3.13.12\python.exe"


def tdoc_call(service, tool, args):
    out = subprocess.check_output([PY, TENCENTDOCS_PY, "tdoc_call", service, tool, json.dumps(args)],
                                  stderr=subprocess.DEVNULL)
    data = json.loads(out)
    # result may be nested under content[0].text
    res = data.get("result", {})
    if "content" in res:
        return json.loads(res["content"][0]["text"])
    return res.get("structuredContent", res)


def export(file_id, out_path):
    r = tdoc_call("tencent-docs", "manage.export_file", {"file_id": file_id})
    task_id = r["task_id"]
    print(f"  export task_id={task_id}")
    file_url = None
    for _ in range(60):  # up to 5 min
        p = tdoc_call("tencent-docs", "manage.export_progress", {"task_id": task_id})
        prog = p.get("progress", 0)
        print(f"  progress={prog}")
        if prog == 100:
            file_url = p.get("file_url")
            break
        time.sleep(5)
    if not file_url:
        raise RuntimeError("export did not complete")
    print(f"  downloading {file_url[:60]}...")
    req = urllib.request.Request(file_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp, open(out_path, "wb") as f:
        f.write(resp.read())
    print(f"  saved -> {out_path} ({os.path.getsize(out_path)} bytes)")


if __name__ == "__main__":
    export(sys.argv[1], sys.argv[2])
