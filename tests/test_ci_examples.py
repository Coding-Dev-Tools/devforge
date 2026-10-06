"""Exercise the rendered CI examples with disposable, non-secret fixtures."""

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from test_install_copy import code_blocks


def workflow(page):
    block = next(block for block in code_blocks(page) if ".github/workflows/" in block)
    return yaml.safe_load(block)


@pytest.mark.parametrize("page", ["docs.html", "quickstart.html"])
def test_rendered_ci_uses_file_based_contract_check(page):
    jobs = workflow(page)["jobs"]
    steps = next(iter(jobs.values()))["steps"]
    checkout = next(step for step in steps if step.get("uses", "").startswith("actions/checkout@"))
    assert checkout["with"]["fetch-depth"] == 0
    runs = "\n".join(step.get("run", "") for step in steps)
    assert 'git show "origin/$BASE_REF:openapi.yaml"' in runs
    assert next(step for step in steps if "git show" in step.get("run", ""))["env"]["BASE_REF"] == "${{ github.base_ref }}"
    assert 'api-contract-guardian check "$baseline" openapi.yaml' in runs
    assert "--base " not in runs and "--head " not in runs
    assert "acg validate" not in runs


@pytest.mark.parametrize("page", ["docs.html", "quickstart.html"])
def test_python_is_selected_before_rendered_install_steps(page):
    steps = next(iter(workflow(page)["jobs"].values()))["steps"]
    setup = next(i for i, step in enumerate(steps) if step.get("uses", "").startswith("actions/setup-python@"))
    install = [i for i, step in enumerate(steps) if "pip install" in step.get("run", "")]
    assert install and all(setup < i for i in install), f"{page}: install before setup-python"


@pytest.mark.skipif(os.environ.get("DEVFORGE_UPSTREAM_SMOKE") != "1", reason="run in the CLI Example Smoke job")
@pytest.mark.parametrize("page", ["docs.html", "quickstart.html"])
@pytest.mark.parametrize("breaking", [False, True])
def test_rendered_ci_commands_run_and_gate_breaking_changes(tmp_path, page, breaking):
    # All remotes below are local disposable fixtures. Nothing contacts a live
    # API, cloud provider, credentials store or production repository.
    required = ["api-contract-guardian"]
    if page == "docs.html":
        required += ["json2sql", "deploydiff", "configdrift"]
    for command in required:
        assert shutil.which(command), f"Smoke job must install {command}"

    def git(*args):
        return subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True, text=True)

    git("init", "-b", "main")
    spec = {"openapi": "3.0.0", "info": {"title": "Dummy", "version": "1"}, "paths": {"/ping": {"get": {"responses": {"200": {"description": "OK"}}}}}}
    (tmp_path / "openapi.yaml").write_text(yaml.safe_dump(spec))
    git("add", "openapi.yaml")
    git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", "Fixture baseline")
    git("remote", "add", "origin", str(tmp_path))
    git("checkout", "-b", "feature")
    if breaking:
        spec["paths"] = {}
        (tmp_path / "openapi.yaml").write_text(yaml.safe_dump(spec))
    (tmp_path / "data").mkdir()
    (tmp_path / "data/seed.json").write_text(json.dumps([{"id": 1, "name": "dummy"}]))
    (tmp_path / "plan.json").write_text(json.dumps({"format_version": "1.2", "resource_changes": []}))
    for filename in ["dev.yaml", "prod.yaml"]:
        (tmp_path / filename).write_text("APP_MODE: dummy\n")

    steps = next(iter(workflow(page)["jobs"].values()))["steps"]
    for step in steps:
        run = step.get("run")
        if not run or run.strip().startswith("pip install"):
            continue  # Installation is verified separately by the smoke job.
        env = dict(os.environ)
        env.update({key: value.replace("${{ github.base_ref }}", "main") for key, value in step.get("env", {}).items()})
        result = subprocess.run(["bash", "-e", "-c", run], cwd=tmp_path, env=env, capture_output=True, text=True)
        if "api-contract-guardian check" in run and breaking:
            assert result.returncode == 1, result.stdout + result.stderr
            break  # GitHub stops later steps when this gate fails.
        assert result.returncode == 0, result.stdout + result.stderr


def test_deploy_requires_all_validation_jobs():
    root = Path(__file__).resolve().parents[1]
    ci = yaml.safe_load((root / ".github/workflows/ci.yml").read_text())
    assert {"test", "linkcheck", "html-validate", "pages-artifact", "cli-example-smoke"} <= set(ci["jobs"]["deploy"]["needs"])


@pytest.mark.skipif(os.environ.get("DEVFORGE_UPSTREAM_SMOKE") != "1", reason="run in the CLI Example Smoke job")
def test_rendered_deadcode_quickstart_scans_a_dummy_project(tmp_path):
    import shlex

    assert shutil.which("deadcode"), "Smoke job must install DeadCode"
    project = tmp_path / "typescript-project"
    project.mkdir()
    (project / "index.ts").write_text("export const unusedDummy = 1;\n")
    block = next(block for block in code_blocks("quickstart.html") if "deadcode " in block and "pip install" not in block)
    line = next(line.strip() for line in block.splitlines() if line.strip().startswith("deadcode "))
    args = [str(project) if arg == "/path/to/ts-project" else arg for arg in shlex.split(line)]
    result = subprocess.run(args, cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "No such option" not in result.stderr
