#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


DOMAIN_RULES = {
    "automation": [
        "automate",
        "automation",
        "workflow",
        "composio",
        "integration",
        "api",
    ],
    "engineering": [
        "code",
        "refactor",
        "testing",
        "deploy",
        "ci/cd",
        "docker",
        "fullstack",
        "backend",
        "frontend",
    ],
    "research-science": [
        "research",
        "scientific",
        "biology",
        "genomics",
        "clinical",
        "paper",
        "literature",
    ],
    "content-writing": [
        "writing",
        "copy",
        "report",
        "documentation",
        "summary",
        "draft",
    ],
    "design-visual": [
        "design",
        "ui",
        "ux",
        "image",
        "infographic",
        "slides",
        "poster",
    ],
    "business-marketing": [
        "marketing",
        "seo",
        "growth",
        "ads",
        "sales",
        "pricing",
        "brand",
    ],
    "productivity-ops": [
        "planning",
        "schedule",
        "weekly",
        "status",
        "sop",
        "decision",
        "review",
    ],
}


ROLE_RULES = {
    "developer": ["dev", "code", "refactor", "test", "debug", "mcp", "plugin"],
    "researcher": ["research", "scientific", "paper", "literature", "clinical"],
    "operator": ["ops", "sre", "deploy", "release", "incident", "workflow"],
    "marketer": ["marketing", "seo", "ads", "content", "campaign"],
    "designer": ["design", "ui", "ux", "image", "visual", "slide"],
    "manager": ["plan", "roadmap", "review", "priority", "report", "strategy"],
}


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
YAML_LINE_RE = re.compile(r"^([a-zA-Z0-9_-]+):\s*(.*)$")


@dataclass
class SkillEntry:
    key: str
    path: str
    folder: str
    name: str
    description: str
    domain_category: str
    role_category: str
    fingerprint: str
    tags: List[str]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(content: str) -> Dict[str, str]:
    normalized = content.replace("\r\n", "\n")
    lines = normalized.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}
    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx < 0:
        return {}
    block = "\n".join(lines[1:end_idx])
    result: Dict[str, str] = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = YAML_LINE_RE.match(line)
        if not m:
            continue
        k = m.group(1).strip()
        v = m.group(2).strip().strip("\"'")
        result[k] = v
    return result


def classify(text: str, rules: Dict[str, List[str]], default_label: str) -> str:
    lowered = text.lower()
    best_label = default_label
    best_score = 0
    for label, keywords in rules.items():
        score = sum(1 for kw in keywords if kw in lowered)
        if score > best_score:
            best_score = score
            best_label = label
    return best_label


def make_fingerprint(path: Path, rel_path: str, content: str) -> str:
    stat = path.stat()
    payload = (
        f"{rel_path}\n{stat.st_size}\n{int(stat.st_mtime)}\n"
        + hashlib.sha1(content.encode("utf-8", errors="replace")).hexdigest()
    )
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def collect_skills(repo_root: Path, skills_root: Path) -> List[SkillEntry]:
    entries: List[SkillEntry] = []
    for skill_file in sorted(skills_root.rglob("SKILL.md")):
        rel_path = skill_file.relative_to(repo_root).as_posix()
        content = read_text(skill_file)
        fm = parse_frontmatter(content)
        skill_name = fm.get("name", "").strip()
        description = fm.get("description", "").strip()
        folder = skill_file.parent.relative_to(skills_root).as_posix()
        fallback_name = skill_file.parent.name.strip()
        display_name = skill_name if skill_name else fallback_name
        key = rel_path
        joined = f"{display_name} {description} {folder}"
        domain = classify(joined, DOMAIN_RULES, "uncategorized")
        role = classify(joined, ROLE_RULES, "general")
        fingerprint = make_fingerprint(skill_file, rel_path, content)
        tags: List[str] = []
        if not skill_name:
            tags.append("name-fallback")
        if not description:
            tags.append("no-description")
        if "skills/skills/skills/" in rel_path:
            tags.append("mirrored-path")
        entries.append(
            SkillEntry(
                key=key,
                path=rel_path,
                folder=folder,
                name=display_name,
                description=description,
                domain_category=domain,
                role_category=role,
                fingerprint=fingerprint,
                tags=tags,
            )
        )
    return entries


def load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(read_text(path))


def delta_and_merge(
    current: List[SkillEntry], previous_data: List[Dict], previous_manifest: Dict
) -> Tuple[List[Dict], Dict]:
    current_by_key = {e.key: e for e in current}
    prev_by_key = {d["key"]: d for d in previous_data} if previous_data else {}
    prev_fp = previous_manifest.get("fingerprints", {}) if previous_manifest else {}

    merged: Dict[str, Dict] = dict(prev_by_key)
    added: List[str] = []
    updated: List[str] = []
    unchanged: List[str] = []

    for key, entry in current_by_key.items():
        old_fp = prev_fp.get(key)
        if old_fp is None:
            added.append(key)
            merged[key] = asdict(entry)
        elif old_fp != entry.fingerprint:
            updated.append(key)
            merged[key] = asdict(entry)
        else:
            unchanged.append(key)
            if key not in merged:
                merged[key] = asdict(entry)

    removed = [k for k in merged.keys() if k not in current_by_key]
    for k in removed:
        del merged[k]

    merged_list = sorted(merged.values(), key=lambda x: x["path"])
    manifest = {
        "updated_at": now_iso(),
        "counts": {
            "total": len(merged_list),
            "added": len(added),
            "updated": len(updated),
            "removed": len(removed),
            "unchanged": len(unchanged),
        },
        "delta": {
            "added": sorted(added),
            "updated": sorted(updated),
            "removed": sorted(removed),
        },
        "fingerprints": {e.key: e.fingerprint for e in current},
    }
    return merged_list, manifest


def build_html(data: List[Dict], manifest: Dict) -> str:
    data_json = json.dumps(data, ensure_ascii=True)
    manifest_json = json.dumps(manifest, ensure_ascii=True)
    counts = manifest.get("counts", {})
    total = counts.get("total", 0)
    added = counts.get("added", 0)
    updated = counts.get("updated", 0)
    removed = counts.get("removed", 0)
    unchanged = counts.get("unchanged", 0)
    updated_at = manifest.get("updated_at", "")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Skills Inventory Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; background: #0b1020; color: #e8ecf1; }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 24px; }}
    .card {{ background: #121a31; border: 1px solid #293352; border-radius: 10px; padding: 16px; margin-bottom: 16px; }}
    .grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }}
    .metric {{ background: #10172b; border: 1px solid #2a3454; border-radius: 8px; padding: 10px; }}
    input, select {{ background: #0f1528; color: #e8ecf1; border: 1px solid #324168; border-radius: 8px; padding: 8px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th, td {{ border-bottom: 1px solid #24304d; padding: 8px; text-align: left; vertical-align: top; }}
    th {{ cursor: pointer; user-select: none; }}
    .muted {{ color: #9fb0d1; }}
    .pill {{ display: inline-block; font-size: 11px; padding: 2px 8px; border: 1px solid #3b4b76; border-radius: 999px; margin-right: 6px; }}
    .pill.good {{ border-color: #1f8f5d; color: #84f1be; }}
    .pill.warn {{ border-color: #a2721f; color: #ffd58a; }}
    .pill.info {{ border-color: #2e5ea7; color: #a7cbff; }}
    .pill.bad {{ border-color: #8f2f2f; color: #ffabab; }}
    .tree {{ font-family: Consolas, monospace; font-size: 12px; line-height: 1.6; }}
    .split {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
    ul.flat {{ margin: 8px 0 0 18px; padding: 0; }}
    ul.flat li {{ margin: 3px 0; }}
    code.path {{ color: #b9d2ff; }}
    .toolbar {{ display:flex; gap:8px; flex-wrap:wrap; align-items:center; }}
    .stats {{ font-size: 12px; color: #9fb0d1; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <h2 style="margin-top:0;">Skills Inventory Report</h2>
      <div class="muted">Updated: {updated_at}</div>
      <div class="grid" style="margin-top:12px;">
        <div class="metric"><b>Total</b><br>{total}</div>
        <div class="metric"><b>Added</b><br>{added}</div>
        <div class="metric"><b>Updated</b><br>{updated}</div>
        <div class="metric"><b>Removed</b><br>{removed}</div>
        <div class="metric"><b>Unchanged</b><br>{unchanged}</div>
      </div>
    </div>

    <div class="card">
      <div class="toolbar">
        <label>Search</label>
        <input id="q" placeholder="Search name/description/path" style="flex: 1; min-width: 260px;" />
        <label>Domain</label>
        <select id="domain"></select>
        <label>Role</label>
        <select id="role"></select>
        <label>Per page</label>
        <select id="pageSize">
          <option value="50">50</option>
          <option value="100" selected>100</option>
          <option value="200">200</option>
          <option value="all">All</option>
        </select>
      </div>
      <div class="stats" style="margin-top:8px;">
        Conditions = Search + Domain + Role. Sort = click column title.
      </div>
      <div id="resultStats" class="stats" style="margin-top:4px;"></div>
      <div class="toolbar" style="margin-top:8px;">
        <button id="prevBtn">Prev</button>
        <button id="nextBtn">Next</button>
        <span id="pageInfo" class="stats"></span>
      </div>
    </div>

    <div class="card split">
      <div>
        <h3 style="margin:0 0 8px 0;">Delta Details</h3>
        <details open>
          <summary>Added (<span id="addedCount">0</span>)</summary>
          <ul id="addedList" class="flat"></ul>
        </details>
        <details>
          <summary>Updated (<span id="updatedCount">0</span>)</summary>
          <ul id="updatedList" class="flat"></ul>
        </details>
        <details>
          <summary>Removed (<span id="removedCount">0</span>)</summary>
          <ul id="removedList" class="flat"></ul>
        </details>
      </div>
      <div>
        <h3 style="margin:0 0 8px 0;">Folder Tree (filtered)</h3>
        <div id="treeRoot" class="tree"></div>
      </div>
    </div>

    <div class="card">
      <table id="tbl">
        <thead>
          <tr>
            <th data-k="name">Name</th>
            <th data-k="domain_category">Domain</th>
            <th data-k="role_category">Role</th>
            <th>Status</th>
            <th>Tags</th>
            <th data-k="folder">Folder</th>
            <th data-k="path">Path</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>
  </div>
  <script>
    const DATA = {data_json};
    const MANIFEST = {manifest_json};
    let sortKey = "path";
    let sortAsc = true;

    const qEl = document.getElementById("q");
    const dEl = document.getElementById("domain");
    const rEl = document.getElementById("role");
    const pageSizeEl = document.getElementById("pageSize");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const pageInfo = document.getElementById("pageInfo");
    const resultStats = document.getElementById("resultStats");
    const tbody = document.querySelector("#tbl tbody");
    const treeRoot = document.getElementById("treeRoot");
    const TOTAL_COUNT = DATA.length;
    let currentPage = 1;

    function uniqueValues(k) {{
      return ["all", ...new Set(DATA.map(x => x[k] || "unknown"))].sort();
    }}

    function fillSelect(el, vals) {{
      el.innerHTML = vals.map(v => `<option value="${{v}}">${{v}}</option>`).join("");
    }}

    fillSelect(dEl, uniqueValues("domain_category"));
    fillSelect(rEl, uniqueValues("role_category"));

    function renderDeltaList(id, arr) {{
      const el = document.getElementById(id);
      if (!arr || arr.length === 0) {{
        el.innerHTML = "<li class='muted'>none</li>";
        return;
      }}
      el.innerHTML = arr.map(p => `<li><code class="path">${{p}}</code></li>`).join("");
    }}

    function renderDeltaPanel() {{
      const delta = MANIFEST.delta || {{}};
      const added = delta.added || [];
      const updated = delta.updated || [];
      const removed = delta.removed || [];
      document.getElementById("addedCount").textContent = String(added.length);
      document.getElementById("updatedCount").textContent = String(updated.length);
      document.getElementById("removedCount").textContent = String(removed.length);
      renderDeltaList("addedList", added);
      renderDeltaList("updatedList", updated);
      renderDeltaList("removedList", removed);
    }}

    function insertTree(node, parts, fullPath) {{
      let cur = node;
      for (const part of parts) {{
        if (!cur.children[part]) {{
          cur.children[part] = {{ name: part, children: {{}}, files: [] }};
        }}
        cur = cur.children[part];
      }}
      cur.files.push(fullPath);
    }}

    function treeToHtml(node) {{
      const childNames = Object.keys(node.children).sort();
      const fileItems = (node.files || []).sort().map(
        p => `<li><code class="path">${{p}}</code></li>`
      ).join("");
      const childItems = childNames.map(name => {{
        const child = node.children[name];
        return `<li><details open><summary>${{name}}</summary><ul>${{treeToHtml(child)}}</ul></details></li>`;
      }}).join("");
      return `${{childItems}}${{fileItems}}`;
    }}

    function renderTree(rows) {{
      const root = {{ children: {{}}, files: [] }};
      for (const row of rows) {{
        const parts = (row.folder || "").split("/").filter(Boolean);
        insertTree(root, parts, row.path);
      }}
      const hasAny = Object.keys(root.children).length > 0 || root.files.length > 0;
      treeRoot.innerHTML = hasAny ? `<ul>${{treeToHtml(root)}}</ul>` : "<span class='muted'>no results</span>";
    }}

    function getFilteredRows() {{
      const q = (qEl.value || "").toLowerCase().trim();
      const d = dEl.value;
      const r = rEl.value;

      return DATA.filter(x => {{
        const s = `${{x.name}} ${{x.description}} ${{x.path}}`.toLowerCase();
        const okQ = !q || s.includes(q);
        const okD = d === "all" || (x.domain_category || "unknown") === d;
        const okR = r === "all" || (x.role_category || "unknown") === r;
        return okQ && okD && okR;
      }});
    }}

    function render() {{
      let rows = getFilteredRows();
      const filteredCount = rows.length;
      const pageSizeRaw = pageSizeEl.value;
      const pageSize = pageSizeRaw === "all" ? filteredCount || 1 : Number(pageSizeRaw);

      rows.sort((a, b) => {{
        const va = (a[sortKey] || "").toLowerCase();
        const vb = (b[sortKey] || "").toLowerCase();
        if (va < vb) return sortAsc ? -1 : 1;
        if (va > vb) return sortAsc ? 1 : -1;
        return 0;
      }});

      const totalPages = Math.max(1, Math.ceil((filteredCount || 1) / pageSize));
      if (currentPage > totalPages) {{
        currentPage = totalPages;
      }}
      const start = pageSizeRaw === "all" ? 0 : (currentPage - 1) * pageSize;
      const end = pageSizeRaw === "all" ? rows.length : Math.min(start + pageSize, rows.length);
      const viewRows = rows.slice(start, end);

      const delta = MANIFEST.delta || {{}};
      const addedSet = new Set(delta.added || []);
      const updatedSet = new Set(delta.updated || []);

      tbody.innerHTML = viewRows.map(x => {{
        let st = "<span class='pill good'>unchanged</span>";
        if (addedSet.has(x.key)) {{
          st = "<span class='pill info'>added</span>";
        }} else if (updatedSet.has(x.key)) {{
          st = "<span class='pill warn'>updated</span>";
        }}
        const tags = (x.tags || []).map(t => `<span class="pill bad">${{t}}</span>`).join("");
        return `
        <tr>
          <td>${{x.name || "<span class='muted'>unknown</span>"}}</td>
          <td><span class="pill">${{x.domain_category}}</span></td>
          <td><span class="pill">${{x.role_category}}</span></td>
          <td>${{st}}</td>
          <td>${{tags || "<span class='muted'>none</span>"}}</td>
          <td>${{x.folder}}</td>
          <td><code>${{x.path}}</code></td>
          <td>${{x.description || "<span class='muted'>no description</span>"}}</td>
        </tr>
      `;
      }}).join("");
      resultStats.textContent = `Total: ${{TOTAL_COUNT}} | Matched: ${{filteredCount}} | Showing: ${{viewRows.length}}`;
      pageInfo.textContent = `Page ${{currentPage}} / ${{totalPages}}`;
      prevBtn.disabled = currentPage <= 1 || pageSizeRaw === "all";
      nextBtn.disabled = currentPage >= totalPages || pageSizeRaw === "all";
      renderTree(rows);
    }}

    function resetAndRender() {{
      currentPage = 1;
      render();
    }}

    qEl.addEventListener("input", resetAndRender);
    dEl.addEventListener("change", resetAndRender);
    rEl.addEventListener("change", resetAndRender);
    pageSizeEl.addEventListener("change", resetAndRender);
    prevBtn.addEventListener("click", () => {{
      currentPage = Math.max(1, currentPage - 1);
      render();
    }});
    nextBtn.addEventListener("click", () => {{
      currentPage += 1;
      render();
    }});

    document.querySelectorAll("th[data-k]").forEach(th => {{
      th.addEventListener("click", () => {{
        const k = th.getAttribute("data-k");
        if (sortKey === k) {{
          sortAsc = !sortAsc;
        }} else {{
          sortKey = k;
          sortAsc = true;
        }}
        render();
      }});
    }});

    renderDeltaPanel();
    render();
  </script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Build incremental skills HTML report.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--skills-root", default=".agents/skills")
    parser.add_argument("--out-html", default="reports/skills-report.html")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    skills_root = (repo_root / args.skills_root).resolve()
    out_html = (repo_root / args.out_html).resolve()
    out_dir = out_html.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    data_path = out_dir / "skills-report.data.json"
    manifest_path = out_dir / "skills-report.manifest.json"

    current = collect_skills(repo_root, skills_root)
    previous_data = load_json(data_path) or []
    previous_manifest = load_json(manifest_path) or {}
    merged_data, manifest = delta_and_merge(current, previous_data, previous_manifest)

    out_html.write_text(build_html(merged_data, manifest), encoding="utf-8")
    data_path.write_text(json.dumps(merged_data, ensure_ascii=True, indent=2), encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=True, indent=2), encoding="utf-8")

    c = manifest["counts"]
    print(
        "done: total={total} added={added} updated={updated} removed={removed} unchanged={unchanged}".format(
            **c
        )
    )
    print(f"html: {out_html}")


if __name__ == "__main__":
    main()
