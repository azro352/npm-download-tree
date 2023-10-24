import functools
import json
from os.path import basename
from pathlib import Path

from nodesemver import max_satisfying
from tqdm import tqdm

from npm_download_tree.config import PACKAGES_OUTPATH
from npm_download_tree.request_helper import session


@functools.lru_cache()
def get_tqdm():
    return tqdm(total=0)


def get_max_satisfying_version(version_require: str, versions: list[str]):
    return max_satisfying(versions, version_require, loose=True)


def dl_package_tar(tarball_url, name, version):
    # print(tarball_url)
    tar_path = PACKAGES_OUTPATH.joinpath(*name.split("/"), version, basename(tarball_url))
    tar_path.parent.mkdir(parents=True, exist_ok=True)
    if not tar_path.exists():
        # print("FETCH", tarball_url, tar_path)
        response = session.get(tarball_url, stream=True)
        if response.ok:
            tar_path.write_bytes(response.raw.read())
        else:
            print("NOT OK")
    # else:
    #     print(tar_path.name, "already exists")

    return tar_path


def dl_package_recursive(package: str, recurse_level: int = 3):
    content = None
    result = set()

    # handle package.json dependencies, not package itself
    if package.endswith("package.json"):
        if package.startswith("https://"):  # remote
            content = session.get(package).json()
        elif (package_path := Path(package)).exists():  # local
            content = json.loads(package_path.read_text())

    else:  # npmjs
        name, version = package, "latest"
        if package.rfind("@") > 0:  # has specified version
            name, version = package.rsplit("@", maxsplit=1)

        package_info_url = f"https://registry.npmjs.org/{name}"
        content = session.get(package_info_url).json()

        if not isinstance(content, dict):
            print(f"ERROR '{content}'")
            exit(1)
        else:

            versions = list(content["versions"])
            if version == "latest":
                max_version = get_max_satisfying_version("*", versions)
            else:
                max_version = get_max_satisfying_version(version, versions)

            if not max_version:
                print(f"Failed to get max_version for {package=} {version=} \n{versions=}")

            content = content["versions"][max_version]
            dist = content.get('dist', {})
            if not isinstance(dist, dict):
                print(f"ERROR DIST '{dist}'")
                exit(1)
            else:
                tarball_url = dist.get('tarball')

        if tarball_url:
            result.add(dl_package_tar(tarball_url, name, max_version))
            get_tqdm().update()
        else:
            print("No tarball at", package_info_url)
            exit(1)

    if not content:
        raise FileNotFoundError(f"Package '{package}' not found")

    if recurse_level > 0:
        deps: dict = {**content.get('dependencies', {}), **content.get('devDependencies', {})}
        get_tqdm().total = get_tqdm().total + len(deps)
        get_tqdm().refresh()
        for dep_name, dep_version in deps.items():
            if dep_version.startswith(("file:", "git+")):
                continue
            result.update(dl_package_recursive(dep_name + "@" + dep_version, recurse_level - 1))

    return result
