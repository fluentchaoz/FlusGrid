"""Real vanilla 26.3 smoke check for queued-tile dispatch.

Runs in a disposable, local dedicated-server process on CI. It does not
test graphical clients, portal transport or a full terrain-conversion job.
"""
import json
import queue
import shutil
import subprocess
import tempfile
import threading
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "dist" / "FlusGrid-0.7.0-10k-experimental.zip"
MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
VERSION = "26.3"


def get_json(url):
    with urllib.request.urlopen(url, timeout=45) as response:
        return json.load(response)


def download_server(destination):
    manifest = get_json(MANIFEST_URL)
    match = next((v for v in manifest["versions"] if v["id"] == VERSION), None)
    if not match:
        raise RuntimeError(f"Mojang version {VERSION} is unavailable")
    data = get_json(match["url"])
    jar = data["downloads"]["server"]
    with urllib.request.urlopen(jar["url"], timeout=120) as source:
        with destination.open("wb") as target:
            shutil.copyfileobj(source, target)


def run():
    if not PACK.exists():
        raise RuntimeError("Generate the 0.7 ZIP first")
    with tempfile.TemporaryDirectory(prefix="flusgrid-runtime-") as tmp:
        base = Path(tmp)
        download_server(base / "server.jar")
        (base / "eula.txt").write_text("eula=true\n")
        (base / "server.properties").write_text(
            "level-name=smoke\nlevel-type=minecraft:flat\n"
            "online-mode=false\nview-distance=2\nsimulation-distance=2\n"
            "max-players=1\nspawn-protection=0\n"
        )
        data_dir = base / "smoke" / "datapacks"
        data_dir.mkdir(parents=True)
        shutil.copy2(PACK, data_dir / PACK.name)
        proc = subprocess.Popen(
            ["java", "-Xms512M", "-Xmx1536M", "-jar", "server.jar", "nogui"],
            cwd=base, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, bufsize=1,
        )
        messages = queue.Queue()
        log = []
        def consume():
            for line in proc.stdout:
                line = line.rstrip()
                log.append(line)
                messages.put(line)
        threading.Thread(target=consume, daemon=True).start()

        def command(value):
            if proc.poll() is not None:
                raise RuntimeError("Minecraft server exited unexpectedly")
            proc.stdin.write(value + "\n")
            proc.stdin.flush()

        try:
            ready = False
            deadline = time.monotonic() + 180
            while time.monotonic() < deadline:
                try:
                    line = messages.get(timeout=1)
                except queue.Empty:
                    if proc.poll() is not None:
                        break
                    continue
                if "Done (" in line and "For help" in line:
                    ready = True
                    break
            if not ready:
                raise RuntimeError("Server never reported ready")

            # Assert the real server actually registered our function before
            # testing it, not just that Python generated some string.
            command('data merge storage flusgrid:realm {state:"ready",live:1b,model:10000,manual_pause:0b}')
            command('data modify storage flusgrid:realm queue append value {dimension:"overworld",x:0,z:0}')
            command("function flusgrid:realm/tile_start")
            command('execute if data storage flusgrid:realm {owner:"overworld",plan:{dimension:"overworld",x:0,z:0}} run say FG_RUNTIME_OWNER_OK')
            command('execute if data storage flusgrid:job {state:"running",chunk_total:1024,total:24576} run say FG_RUNTIME_WORKER_OK')
            command('execute unless data storage flusgrid:realm queue[0] run say FG_RUNTIME_QUEUE_CONSUMED')
            target = ["FG_RUNTIME_OWNER_OK", "FG_RUNTIME_WORKER_OK", "FG_RUNTIME_QUEUE_CONSUMED"]
            deadline = time.monotonic() + 45
            while time.monotonic() < deadline and not all(
                any(t in line and ("Server" in line or "server" in line) for line in log)
                for t in target
            ):
                if proc.poll() is not None:
                    break
                time.sleep(0.2)
            missing = [t for t in target if not any(t in line for line in log)]
            if missing:
                raise RuntimeError("Queue handoff failed: " + ", ".join(missing))
            errors = [l for l in log if ("Failed to load function" in l or "Failed to parse function" in l)]
            if errors:
                raise RuntimeError("Vanilla function parser errors: " + repr(errors[:8]))
            print("PASS vanilla 26.3: queue head consumed and Overworld tile worker started")
        finally:
            if proc.poll() is None:
                command("stop")
                try:
                    proc.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=10)
            if proc.returncode not in (0, None):
                print("Vanilla server returned:", proc.returncode)
            if "PASS vanilla" not in "\n".join(log[-30:]):
                print("\n".join(log[-80:]))


if __name__ == "__main__":
    run()
