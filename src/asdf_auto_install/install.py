#!/usr/bin/env python
from argparse import ArgumentParser
import sys
import json
from pathlib import Path

import asdf_auto_install
from asdf_auto_install.cls import Plugin


def get_args():
    parser = ArgumentParser(description="auto installer of asdf plugins")

    parser.add_argument("name", nargs="*", help="list of plugin names in your config")
    parser.add_argument("--all", action="store_true",
        help="install all plugins in your config file")
    parser.add_argument("--config", default=None,
        help="path to json config file (default: $HOME/.config/asdf-auto-install/plugins.json)")
    parser.add_argument("--no-run", action="store_true",
        help="show commands without running")
    parser.add_argument("--force-post-install", action="store_true",
        help="run post install commands even if the plugin already installed")
    parser.add_argument('--version', action='version', version=asdf_auto_install.__version__)

    return parser.parse_args()


def load_config(cfgpath: Path) -> dict:
    assert cfgpath.is_file(), f"config file: {str(cfgpath)} is not found"

    with open(cfgpath, "r") as f:
        config_dict = json.load(f)

    plugin_dict = {}
    for key, config in config_dict.items():

        if "post_install" not in config:
            config["post_install"] = []
        if "set_global" not in config:
            config["set_global"] = False
        if "force_post_install" not in config:
            config["force_post_install"] = False

        plugin = Plugin(
            plugin_name=config["plugin_name"],
            version=config["version"],
            post_install=config["post_install"],
            set_global=config["set_global"],
            force_post_install=config["force_post_install"]
        )
        plugin_dict[key] = plugin

    return plugin_dict


def install(args):
    if args.config is None:
        cfgpath = Path.home() / ".config/asdf-auto-install/plugins.json"
    else:
        cfgpath = Path(args.config)

    plugin_dict = load_config(cfgpath)

    plugins = plugin_dict.keys() if args.all else args.name

    for key in plugins:
        print("")
        print("=" * 30)
        print(f"install {key}")
        try:
            plugin = plugin_dict[key]
        except KeyError:
            print(f'Plugin "{key}" is not in plugin_list.', file=sys.stderr)
            print(f'install "{key}" is skipped.')
            continue

        if args.force_post_install:
            plugin.force_post_install = True

        plugin.run_install(args.no_run)
        print(f"install {key} is finished.")


def main():
    args = get_args()
    install(args)


if __name__ == "__main__":
    main()
