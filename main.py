#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path

import click

from npm_download_tree.downloader import dl_package_recursive
from npm_download_tree.export_zip import export_as_zip


@click.command()
@click.option('-r', '--recurse', default=3, help='Number of level to recurse')
@click.argument('packages', nargs=-1, required=True)
def main(recurse, packages):
    """
    Dl packages tree

    PACKAGES The packages, can be a name, of local package.json or a remote package.json
    """
    print(f"{recurse=}")
    print(f"{packages=}")
    start = datetime.now()
    downloads: set[Path] = set().union(*[dl_package_recursive(package, recurse) for package in packages])
    zipname = export_as_zip(downloads)
    print("DOWNLOADED", len(downloads), "in", datetime.now() - start)
    print("ZIPPED into", zipname)


if __name__ == '__main__':
    main()
