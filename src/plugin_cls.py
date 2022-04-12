#!/usr/bin/env python
from __future__ import annotations
import subprocess
from pathlib import Path


class Plugin:
    def __init__(self,
                 plugin_name: str,
                 version: str = "latest",
                 post_update: list[str] = [],
                 set_global: bool = True,
                 force_post_update: bool = False):
        self.plugin_name: str = plugin_name
        self.version: str = version
        self.post_update: list[str] = post_update
        self.set_global: bool = set_global
        self.force_post_update: bool = force_post_update

        self._repohome: Path = Path(__file__).parents[1]
        self._tmpdir = self._repohome / "tmp"
        self.already_installed: bool = False

    def _mkdir_tmpdir(self, dry_run=False) -> None:
        script = f"mkdir -p {str(self._tmpdir)}"
        _run_script(script, dry_run)

    def _clean_tmpdir(self, dry_run=False) -> None:
        tmpfile = self._tmpdir / ".tool-versions"
        if tmpfile.is_file():
            script = f"rm {str(tmpfile)}"
            _run_script(script, dry_run)

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

    def _local(self, dry_run=False) -> None:
        script = f"asdf local {self.plugin_name} {self.version}"
        _run_script(script, dry_run, cwd=self._tmpdir)

    def _run_post_update(self, dry_run=False) -> None:
        if len(self.post_update) == 0:
            return
        print("==> Post update")
        if self.set_global:
            for script in self.post_update:
                _run_script(script, dry_run)
        else:
            for script in self.post_update:
                _run_script(script, dry_run, cwd=self._tmpdir)

    def run_update(self, dry_run=False):
        self._add(dry_run)
        self._update(dry_run)
        self._install(dry_run)

        if self.set_global:
            self._global(dry_run)
        else:
            self._mkdir_tmpdir(dry_run)
            self._clean_tmpdir(dry_run)
            self._local(dry_run)

        if self.force_post_update or (not self.already_installed):
            self._run_post_update(dry_run)
        else:
            print("==> Post update is skipped.")

        if not self.set_global:
            self._clean_tmpdir(dry_run)


def _run_script(script: str, dry_run=False, cwd=None) -> str:
    if cwd is None:
        print(f"==> Run `{script}`")
    else:
        print(f"==> Run `{script}` at {str(cwd)}")
    stdout = ""
    if not dry_run:
        p = subprocess.Popen(script, shell=True, cwd=cwd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        while p.poll() is None:
            line = p.stdout.readline().decode().strip()
            print(line)
            stdout += line + "\n"
    return stdout
