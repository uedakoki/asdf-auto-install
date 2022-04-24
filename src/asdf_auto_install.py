#!/usr/bin/env python
from argparse import ArgumentParser
import sys
import json
from pathlib import Path

from plugin_cls import Plugin


def get_args():
    parser = ArgumentParser()

    parser.add_argument("plugins", nargs="*")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--force-post-install", action="store_true")

    return parser.parse_args()


def load_config() -> dict:
    repohome = Path(__file__).parents[1]
    config_file = repohome / "asdf_plugin_config.json"
    with open(config_file, "r") as f:
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
    plugin_dict = load_config()

    plugins = plugin_dict.keys() if args.all else args.plugins

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

        plugin.run_install(args.dry_run)
        print(f"install {key} is finished.")


def main():
    args = get_args()
    install(args)


if __name__ == "__main__":
    main()
