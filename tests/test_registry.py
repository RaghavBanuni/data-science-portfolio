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

# The index opens with the count spelled out in words, which is exactly the kind of detail that goes
# stale when a project is added. Mapping only the range this repository could plausibly occupy keeps
# the check honest: an unmapped count fails loudly rather than silently passing.
NUMBER_WORDS = {
    17: "Seventeen",
    18: "Eighteen",
    19: "Nineteen",
    20: "Twenty",
    21: "Twenty-one",
    22: "Twenty-two",
    23: "Twenty-three",
    24: "Twenty-four",
    25: "Twenty-five",
    26: "Twenty-six",
    27: "Twenty-seven",
    28: "Twenty-eight",
    29: "Twenty-nine",
    30: "Thirty",
}


def test_the_registry_holds_twenty_seven_projects():
    assert len(PROJECTS) == 27


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


def test_the_readme_states_the_current_project_count():
    """The opening sentence spells the count out, and nothing else keeps it in step with the registry."""
    count = len(PROJECTS)
    assert count in NUMBER_WORDS, f"extend NUMBER_WORDS to cover {count}"
    expected = f"{NUMBER_WORDS[count]} end-to-end projects"
    assert expected in README, f"the index does not say {expected!r}"


def test_every_project_appears_in_a_table_row_under_its_own_category():
    """A project linked only from the reading order would be invisible in the category tables.

    Checked structurally: the link has to appear somewhere after its category heading and before the
    next one, which is what makes the index navigable rather than merely complete.
    """
    owner = REGISTRY["owner"]
    positions = {
        category: README.index(f"## {category}")
        for category in REGISTRY["categories"]
        if f"## {category}" in README
    }
    assert len(positions) == len(REGISTRY["categories"]), "a category has no `## ` heading"
    ordered = sorted(positions.items(), key=lambda item: item[1])
    bounds = {}
    for index, (category, start) in enumerate(ordered):
        end = ordered[index + 1][1] if index + 1 < len(ordered) else len(README)
        bounds[category] = (start, end)

    for project in PROJECTS:
        start, end = bounds[project["category"]]
        section = README[start:end]
        link = f"https://github.com/{owner}/{project['slug']}"
        assert link in section, f"{project['slug']} is not listed under {project['category']}"


def test_the_link_checker_reads_the_same_registry():
    """Two sources of truth would defeat the point of having a registry."""
    script = (ROOT / "scripts" / "check_links.py").read_text(encoding="utf-8")
    assert 'REGISTRY = ROOT / "projects.json"' in script
