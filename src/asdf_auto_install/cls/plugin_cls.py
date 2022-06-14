#!/usr/bin/env python
from __future__ import annotations
import subprocess
from pathlib import Path


class Plugin:
    def __init__(
            self,
            plugin_name: str,
            version: str = "latest",
            post_install: list[str] = [],
            set_global: bool = True,
            force_post_install: bool = False
            ):
        self.plugin_name: str = plugin_name
        self.version: str = version
        self.post_install: list[str] = post_install
        self.set_global: bool = set_global
        self.force_post_install: bool = force_post_install

        self._repohome: Path = Path(__file__).parents[1]
        self._tmpdir = self._repohome / "tmp"
        self.already_installed: bool = False

    def _mkdir_tmpdir(self, no_run=False) -> None:
        script = f"mkdir -p {str(self._tmpdir)}"
        _run_script(script, no_run)

    def _clean_tmpdir(self, no_run=False) -> None:
        tmpfile = self._tmpdir / ".tool-versions"
        if tmpfile.is_file():
            script = f"rm {str(tmpfile)}"
            _run_script(script, no_run)

    def _add(self, no_run=False) -> None:
        script = f"asdf plugin add {self.plugin_name}"
        _run_script(script, no_run)

    def _update(self, no_run=False) -> None:
        script = f"asdf plugin update {self.plugin_name}"
        _run_script(script, no_run)

    def _install(self, no_run=False) -> None:
        script = f"asdf install {self.plugin_name} {self.version}"
        stdout = _run_script(script, no_run)
        if "is already installed" in stdout:
            self.already_installed = True

    def _global(self, no_run=False) -> None:
        script = f"asdf global {self.plugin_name} {self.version}"
        _run_script(script, no_run)

    def _local(self, no_run=False) -> None:
        script = f"asdf local {self.plugin_name} {self.version}"
        _run_script(script, no_run, cwd=self._tmpdir)

    def _run_post_install(self, no_run=False) -> None:
        if len(self.post_install) == 0:
            return
        print("==> Post install")
        if self.set_global:
            for script in self.post_install:
                _run_script(script, no_run)
        else:
            for script in self.post_install:
                _run_script(script, no_run, cwd=self._tmpdir)

    def run_install(self, no_run=False):
        self._add(no_run)
        self._update(no_run)
        self._install(no_run)

        if self.set_global:
            self._global(no_run)
        else:
            self._mkdir_tmpdir(no_run)
            self._clean_tmpdir(no_run)
            self._local(no_run)

        if self.force_post_install or (not self.already_installed):
            self._run_post_install(no_run)
        else:
            print("==> Post install is skipped.")

        if not self.set_global:
            self._clean_tmpdir(no_run)


def _run_script(script: str, no_run=False, cwd=None) -> str:
    message = "Command" if no_run else "Running"
    if cwd is None:
        print(f"==> {message} `{script}`")
    else:
        print(f"==> {message} `{script}` at {str(cwd)}")
    stdout = ""
    if not no_run:
        p = subprocess.Popen(script, shell=True, cwd=cwd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        while p.poll() is None:
            line = p.stdout.readline().decode().strip()
            if line != "":
                print(line)
                stdout += line + "\n"
        print()
    return stdout
