#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Push specific files to the GitHub Pages repo via gh api (REST rebuild).

Used when `git push` is blocked. Reconstructs blobs -> tree -> commit ->
PATCH refs/heads/master. All other repo files are preserved.

Usage:
    python gh_push.py <file1> [file2 ...] ["message"]
"""
import sys
import os
import json
import base64
import subprocess

REPO = "chenyang0301/huitexun-website"


def gh_api(method, path, body=None):
    cmd = ["gh", "api", "/repos/" + REPO + path, "-X", method]
    inp = None
    if body is not None:
        cmd += ["--input", "-"]
        inp = json.dumps(body).encode("utf-8")
    r = subprocess.run(cmd, input=inp, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("gh api %s failed: %s" % (path, r.stderr.decode("utf-8", "replace")))
    if not r.stdout:
        return {}
    return json.loads(r.stdout)


def main():
    args = sys.argv[1:]
    if not args:
        print("usage: python gh_push.py <file> ... [message]")
        return
    # last arg is an optional message if it doesn't look like a file
    files, msg = [], "chore: sync IoT card data from Tencent Docs"
    for a in args:
        if os.path.exists(a):
            files.append(a)
        else:
            msg = a
    if not files:
        print("no valid files given")
        return

    # 1. current master ref + tree
    ref = gh_api("GET", "/git/refs/heads/master")
    commit_sha = ref["object"]["sha"]
    tree = gh_api("GET", "/git/trees/" + commit_sha + "?recursive=1")
    old = {e["path"]: e for e in tree["tree"] if e["type"] == "blob"}

    # 2. create blobs for changed/new files
    shas = {}
    for f in files:
        data = open(f, "rb").read()
        b64 = base64.b64encode(data).decode("ascii")
        r = gh_api("POST", "/git/blobs", {"content": b64, "encoding": "base64"})
        shas[f] = r["sha"]
        print("blob  %-32s %d KB -> %s" % (f, len(data) // 1024, r["sha"][:8]))

    # 3. build new tree (keep all old blobs, override changed, add new)
    entries = []
    for path, e in old.items():
        sha = shas.get(path, e["sha"])
        entries.append({"path": path, "mode": e["mode"], "type": "blob", "sha": sha})
    for f in files:
        if f not in old:
            entries.append({"path": f, "mode": "100644", "type": "blob", "sha": shas[f]})

    new_tree = gh_api("POST", "/git/trees", {"tree": entries})
    print("tree  ->", new_tree["sha"][:8])

    # 4. commit
    commit = gh_api("POST", "/git/commits",
                    {"message": msg, "tree": new_tree["sha"], "parents": [commit_sha]})
    print("commit ->", commit["sha"][:8])

    # 5. point master at new commit
    gh_api("PATCH", "/git/refs/heads/master", {"sha": commit["sha"]})
    print("PUSHED master ->", commit["sha"][:8])


if __name__ == "__main__":
    main()
