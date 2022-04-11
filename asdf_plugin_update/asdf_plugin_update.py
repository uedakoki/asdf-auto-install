#!/usr/bin/env python
from argparse import ArgumentParser
import sys
import json

from plugin_cls import Plugin


def get_args():
    parser = ArgumentParser()

    parser.add_argument("plugins", nargs="*")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--force-post-update", action="store_true")

    return parser.parse_args()


def load_config() -> dict:
    config_file = "asdf_plugin_update_config.json"
    with open(config_file, "r") as f:
        config_dict = json.load(f)

    plugin_dict = {}
    for key, config in config_dict.items():
        plugin = Plugin(
            plugin_name=config["plugin_name"],
            version=config["version"],
            post_update=config["post_update"]
        )
        plugin_dict[key] = plugin

    return plugin_dict


def main(args):
    plugin_dict = load_config()

    if args.all:
        plugins = plugin_dict.keys()
    else:
        plugins = args.plugins

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

        plugin.run_update(args.dry_run, args.force_post_update)
        print(f"install {key} is finished.")


if __name__ == "__main__":
    args = get_args()
    main(args)
