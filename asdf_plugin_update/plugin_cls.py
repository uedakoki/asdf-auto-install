#!/usr/bin/env python
from __future__ import annotations
import subprocess


class Plugin:
    def __init__(self,
                 plugin_name: str,
                 version: str = "latest",
                 post_update: list[str] = []):
        self.plugin_name: str = plugin_name
        self.version: str = version
        self.post_update: list[str] = post_update
        self.already_installed: bool = False

    def _add(self, dry_run=False) -> None:
        script = f"asdf plugin add {self.plugin_name}"
        _run_script(script, dry_run)

    def _update(self, dry_run=False) -> None:
        script = f"asdf plugin update {self.plugin_name}"
        _run_script(script, dry_run)

    def _install(self, dry_run=False) -> None:
        script = f"asdf install {self.plugin_name} {self.version}"
        stdout = _run_script(script, dry_run)
        if "is already installed" in stdout:
            self.already_installed = True

    def _global(self, dry_run=False) -> None:
        script = f"asdf global {self.plugin_name} {self.version}"
        _run_script(script, dry_run)

    def _run_post_update(self, dry_run=False) -> None:
        if len(self.post_update) == 0:
            return
        print("==> Post update")
        for script in self.post_update:
            _run_script(script, dry_run)

    def run_update(self, dry_run=False, force_post_update=False):
        self._add(dry_run)
        self._update(dry_run)
        self._install(dry_run)
        self._global(dry_run)
        if force_post_update or (not self.already_installed):
            self._run_post_update(dry_run)
        else:
            print("==> Post update is skipped.")


def _run_script(script: str, dry_run=False) -> str:
    print(f"==> Run `{script}`")
    if not dry_run:
        p = subprocess.Popen(script.split(" "), stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        stdout = ""
        while p.poll() is None:
            line = p.stdout.readline().decode().strip()
            print(line)
            stdout += line + "\n"
        return stdout
    return ""
