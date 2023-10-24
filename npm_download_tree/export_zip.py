import zipfile
from datetime import datetime
from pathlib import Path

from npm_download_tree.config import OUTPATH, PACKAGES_OUTPATH


def export_as_zip(downloads: set[Path]):
    zipname = f"npm_tree_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    with zipfile.ZipFile(OUTPATH.joinpath(zipname), "w") as zipout:
        for download in downloads:
            zipout.write(download, arcname=download.relative_to(PACKAGES_OUTPATH))
    return zipname