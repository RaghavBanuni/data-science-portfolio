"""The index and the registry cannot drift apart.

These tests are offline on purpose: they check internal consistency, which is the failure that
actually happens (a project renamed in one place and not the other). Reachability is a separate,
network-dependent concern and lives in ``scripts/check_links.py``.

Run with ``pytest`` from the repository root.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = json.loads((ROOT / "projects.json").read_text(encoding="utf-8"))
README = (ROOT / "README.md").read_text(encoding="utf-8")
PROJECTS = REGISTRY["projects"]
REQUIRED_KEYS = {"slug", "title", "category", "stack", "decision", "hard_part"}


def test_the_registry_holds_seventeen_projects():
    assert len(PROJECTS) == 17


def test_every_entry_is_complete():
    for project in PROJECTS:
        assert REQUIRED_KEYS <= set(project), f"{project.get('slug')} is missing keys"
        assert project["stack"], f"{project['slug']} declares no stack"
        assert project["hard_part"].strip().endswith("."), project["slug"]


def test_slugs_are_unique_and_url_safe():
    slugs = [project["slug"] for project in PROJECTS]
    assert len(set(slugs)) == len(slugs)
    for slug in slugs:
        assert re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug), slug


def test_every_declared_category_is_used():
    declared = set(REGISTRY["categories"])
    used = {project["category"] for project in PROJECTS}
    assert used <= declared, f"undeclared categories: {used - declared}"
    assert declared == used, f"unused categories: {declared - used}"


def test_the_readme_links_every_project():
    """The failure this catches: a project renamed in the registry and not in the index.

    A project may legitimately be linked more than once -- the reading-order section links a few of
    them a second time -- so this asserts presence, not an exact count.
    """
    owner = REGISTRY["owner"]
    missing = [
        project["slug"]
        for project in PROJECTS
        if f"https://github.com/{owner}/{project['slug']}" not in README
    ]
    assert missing == [], f"not linked from the index: {missing}"


def test_the_readme_links_nothing_that_is_not_in_the_registry():
    """A link to a repository that was renamed or never existed is the other half of the drift."""
    owner = REGISTRY["owner"]
    linked = set(re.findall(rf"https://github\.com/{owner}/([a-z0-9-]+)", README))
    known = {project["slug"] for project in PROJECTS} | {"data-science-portfolio"}
    assert linked <= known, f"unknown links: {sorted(linked - known)}"


def test_every_category_heading_appears_in_the_readme():
    for category in REGISTRY["categories"]:
        assert category in README, category


def test_the_link_checker_reads_the_same_registry():
    """Two sources of truth would defeat the point of having a registry."""
    script = (ROOT / "scripts" / "check_links.py").read_text(encoding="utf-8")
    assert 'REGISTRY = ROOT / "projects.json"' in script
