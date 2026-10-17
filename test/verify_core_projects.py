"""Verify self-contained core packs, intentional starters and native windows.

No student program is changed by the observer. The only completed-starter
replacement is its declared task module. Wrong-reference cases are disposable.
Every child has a timeout, a process-group cleanup path and persistent logs.
"""

import argparse
import ast
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
PACKS = {
    "setup": ("PG-CORE-Workspace-and-Assets", "workspace_config.py", 5),
    "sprites": ("PG-CORE-Image-Anchors", "geometry.py", 9),
    "master": ("PG-CORE-Arena-Capstone", "game_logic.py", 16),
}
ASSET_SHA = "a435b65656cdecdebd8b2c5510092217995b4754d1afd4bc2fdbd583040c8263"
VERSIONS = {"pgzero": "1.2.1", "pygame": "2.6.1", "numpy": "2.5.4"}


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    return {str(path.relative_to(root)): sha(path) for path in sorted(root.rglob("*")) if path.is_file() and "__pycache__" not in path.parts}


def run(args, cwd, output, expected=0, env=None, timeout=20):
    output.mkdir(parents=True, exist_ok=True)
    record = {"parentTask": "pygames-core-native-contracts", "parentPid": os.getpid(),
              "cwd": str(cwd), "command": args, "startTime": now(), "timeoutSeconds": timeout}
    child = subprocess.Popen(args, cwd=cwd, env=env, start_new_session=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    record.update(pid=child.pid, event="start")
    with (output / "processes.jsonl").open("a") as log:
        log.write(json.dumps(record) + "\n")
    cleanup = "not needed"
    stdout = stderr = b""
    try:
        stdout, stderr = child.communicate(timeout=timeout)
    except BaseException:
        cleanup = "owned process group terminated after timeout or cancellation"
        os.killpg(child.pid, signal.SIGTERM)
        try:
            stdout, stderr = child.communicate(timeout=3)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            stdout, stderr = child.communicate()
        raise
    finally:
        (output / "stdout.log").write_bytes(stdout)
        (output / "stderr.log").write_bytes(stderr)
        record.update(event="end", endTime=now(), exitCode=child.returncode,
                      childProcessGroupCleanup=cleanup)
        with (output / "processes.jsonl").open("a") as log:
            log.write(json.dumps(record) + "\n")
    assert child.returncode == expected, (args, child.returncode, expected, stderr.decode(), stdout.decode())
    return stdout.decode()


def wrong_task(kind, text):
    if kind == "setup":
        before, after = "WIDTH = 640", "WIDTH = 320"
    elif kind == "sprites":
        before = "return (\n        min(max(x, sprite_width / 2), width - sprite_width / 2),\n        min(max(y, sprite_height / 2), height - sprite_height / 2),\n    )"
        after = "return x, y"
    else:
        before = 'self.bullets.append({"x": self.x + 34, "y": self.y, "vx": 360.0})'
        after = "pass  # Disposable regression: no projectile was created."
    assert text.count(before) == 1, (kind, before)
    return text.replace(before, after)


def verify_native(kind, profile, native):
    assert native["finished"] is True and native["versions"] == VERSIONS
    assert native["pythonVersion"][:2] == [3, 12]
    captures = {capture["name"]: capture for capture in native["captures"]}
    for capture in captures.values():
        assert capture["displayDriver"] == "dummy"
        assert capture["assetSha256"] == ASSET_SHA
        assert capture["assetSize"] == [66, 92]
        assert len(capture["renderedOpaquePixels"]) == 3, (kind, profile, capture["name"])
    complete = profile in ("completed-starter", "reference")
    if kind == "setup":
        first = captures["startup"]
        dimensions = [640, 480] if complete else [320, 240] if profile == "starter" else [320, 480]
        assert first["window"] == dimensions
        assert first["actorCenter"] == [dimensions[0] / 2, dimensions[1] / 2]
        assert first["caption"] == "Workspace Check"
    elif kind == "sprites":
        assert captures["startup"]["actorCenter"] == [320, 240]
        assert captures["top_left"]["actorCenter"] == ([33, 46] if complete else [0, 0])
        assert captures["bottom_right"]["actorCenter"] == ([607, 434] if complete else [640, 480])
        assert captures["right_click_ignored"]["actorCenter"] == captures["bottom_right"]["actorCenter"]
        assert captures["center"]["actorCenter"] == [320, 240]
        assert len(native["eventsPosted"]) == 4
        if complete:
            assert captures["top_left"]["actorBounds"] == [0, 0, 66, 92]
            assert captures["bottom_right"]["actorBounds"] == [574, 388, 640, 480]
    else:
        model = {name: capture["model"] for name, capture in captures.items()}
        assert model["ready"]["mode"] == "ready"
        assert model["playing"]["mode"] == "playing"
        assert model["paused"]["mode"] == "paused"
        assert model["paused"] == model["paused_again"] == model["paused_shot_refused"]
        assert model["resumed"]["mode"] == "playing"
        assert (model["held_right"]["x"] > 96) is (profile != "starter")
        assert len(model["fired"]["bullets"]) == (1 if complete else 0)
        assert model["controlled_win"]["mode"] == ("playing" if profile == "starter" else "won")
        for name in ("controlled_timeout", "controlled_tie"):
            assert model[name]["mode"] == ("playing" if profile == "starter" else "lost")
        reset = model["controlled_reset"]
        assert reset["mode"] == "playing" and reset["score"] == 0 and reset["lives"] == 3
        assert reset["remaining"] == 30 and reset["bullets"] == []
        assert reset["x"] == 96 and reset["y"] == 240 and reset["vx"] == reset["vy"] == 0
        assert reset["shot_cooldown"] == reset["hit_cooldown"] == 0
        assert reset["enemies"] == [{"x": 500, "y": 120}, {"x": 540, "y": 360}]
        assert reset["beacon_index"] == 0 and reset["beacon"] == [520, 240]
        for name in ("restart", "restart_after_fire"):
            assert model[name]["mode"] == "playing" and model[name]["bullets"] == []
            assert model[name]["score"] == 0 and model[name]["lives"] == 3
            assert captures[name]["actorCenter"] == [96, 240]
        assert len(native["eventsPosted"]) == 9
        for capture in captures.values():
            assert capture["window"] == [640, 480] and capture["hudSize"] == [640, 40]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--contracts-only", action="store_true")
    args = parser.parse_args()
    output = args.output.resolve()
    assert not output.exists(), "Use a fresh evidence directory."
    output.mkdir(parents=True)
    source_before = {folder: inventory(ROOT / folder) for folder, _, _ in PACKS.values()}
    for folder, _, _ in PACKS.values():
        shutil.copytree(ROOT / folder, output / "source" / folder)
    for filename in ("test/verify_core_projects.py", "test/observe_core_native.py",
                     "COURSE_SOURCE_MANIFEST.md", "SOURCE_BACKLOG.md", "STRUCTURE.md",
                     "verify-course-source.sh", ".github/workflows/core-projects.yml"):
        source = ROOT / filename
        destination = output / "source" / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    summary = {"started": now(), "profiles": [], "nativePending": args.contracts_only,
               "observerScope": "Real SDL events; separately labeled controlled terminal states.",
               "sourceInventory": source_before,
               "runtimeContext": {name: os.environ.get(name) for name in
                                  ("GITHUB_REPOSITORY", "GITHUB_SHA", "GITHUB_REF",
                                   "GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT")}}
    for kind, (folder, task, count) in PACKS.items():
        pack = ROOT / folder
        assert (pack / "README.md").is_file()
        starter, reference = inventory(pack / "starter"), inventory(pack / "solution")
        assert set(starter) == set(reference)
        assert {name for name in starter if starter[name] != reference[name]} == {task}
        for role in ("starter", "solution"):
            assert sha(pack / role / "images/alien.png") == ASSET_SHA
            for source in (pack / role).glob("*.py"):
                ast.parse(source.read_text(), filename=str(source), feature_version=(3, 12))
        for profile in ("starter", "completed-starter", "reference", "wrong-reference"):
            proof = output / kind / profile
            with tempfile.TemporaryDirectory(prefix="pygames-core-") as temporary:
                temporary = Path(temporary)
                work = temporary / "project"
                original = "starter" if profile in ("starter", "completed-starter") else "solution"
                shutil.copytree(pack / original, work)
                shutil.copy2(pack / "README.md", work / "README.md")
                if profile == "completed-starter":
                    shutil.copy2(pack / "solution" / task, work / task)
                elif profile == "wrong-reference":
                    (work / task).write_text(wrong_task(kind, (work / task).read_text()))
                baseline = inventory(work)
                environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
                status = 0 if profile in ("completed-starter", "reference") else 1
                text = run([sys.executable, "contracts.py"], work, proof / "contracts",
                           expected=status, env=environment)
                assert text.count("PASS ") + text.count("FAIL ") == count
                if status == 0:
                    assert text.count("PASS ") == count and "FAIL " not in text
                else:
                    assert "FAIL " in text
                if not args.contracts_only:
                    hook = temporary / "hook"
                    hook.mkdir()
                    shutil.copy2(ROOT / "test/observe_core_native.py", hook / "sitecustomize.py")
                    native_output = proof / "native"
                    environment.update(PYTHONPATH=str(hook), SDL_VIDEODRIVER="dummy",
                                       SDL_AUDIODRIVER="dummy", PYGAMES_NATIVE_KIND=kind,
                                       PYGAMES_NATIVE_OUTPUT=str(native_output))
                    run([sys.executable, "main.py"], work, proof / "runtime", env=environment)
                    native = json.loads((native_output / "native.json").read_text())
                    verify_native(kind, profile, native)
                    for capture in native["captures"]:
                        assert sha(native_output / capture["screenshot"]) == capture["screenshotSha256"]
                assert baseline == inventory(work), "Runtime changed the project source."
                summary["profiles"].append({"kind": kind, "profile": profile,
                                            "contracts": count, "expectedExit": status,
                                            "projectHashes": baseline,
                                            "nativeValidated": not args.contracts_only})
    assert source_before == {folder: inventory(ROOT / folder) for folder, _, _ in PACKS.values()}
    summary.update(finished=now(), sourceUnchanged=True, profilesPassed=len(summary["profiles"]))
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"profilesPassed": summary["profilesPassed"], "nativePending": args.contracts_only}))


if __name__ == "__main__":
    main()
