# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['asdf_auto_install', 'asdf_auto_install.cls']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['asdf-auto-install = asdf_auto_install.install:main']}

setup_kwargs = {
    'name': 'asdf-auto-install',
    'version': '0.1.1',
    'description': 'auto installer of asdf plugins',
    'long_description': None,
    'author': 'uedakoki',
    'author_email': 'k7ml8.p31@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
