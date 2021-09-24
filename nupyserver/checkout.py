import base64
import json
import logging
import re
import uuid
from datetime import datetime
from os import listdir, mkdir, remove
from os.path import join, getsize, exists
from shutil import copy
from xml.etree.ElementTree import XML
from zipfile import ZipFile

from nupyserver.utils import detect_codec, hash_file

_CHECKOUT_RUNNING: bool = False
_COLS = ["pkg_file_size", "pkg_file_hash", "pkg_info_id", "pkg_info_version", "pkg_info_authors",
         "pkg_info_description", "pkg_info_summary", "pkg_info_repos", "pkg_info_license", "pkg_info_title",
         "pkg_info_url", "pkg_info_release_notes", "pkg_info_copyright", "pkg_info_icon", "pkg_commit_id",
         "pkg_commit_timestamp"]


class CheckOut:
    def __init__(self, db, config):
        self._db = db
        self._config = config
        self._log = logging.getLogger("CheckOut")

    def run(self):
        global _CHECKOUT_RUNNING
        if _CHECKOUT_RUNNING:
            return

        _CHECKOUT_RUNNING = True
        self._log.info("Run checkout...")

        pkgInfoList = []
        for f in listdir(self._config.get("checkout")):
            if f.endswith(".nupkg"):
                self._log.debug(f"Check {f}")
                pkgInfo = self._read_nupkg(join(self._config.get("checkout"), f))
                if pkgInfo:
                    pkgInfoList.append(pkgInfo)

        # TODO check package already in database
        self._db.insert_many("tbl_packages", _COLS, pkgInfoList)
        self._log.info(f"{len(pkgInfoList)} new packages added...")
        _CHECKOUT_RUNNING = False

    def _read_nupkg(self, pkg):
        nuspecBin = None
        with ZipFile(pkg) as zipFile:
            for entry in zipFile.namelist():
                if entry.endswith(".nuspec"):
                    nuspecBin = zipFile.read(entry)
                    break

        if nuspecBin is None:
            return None

        nuspecStr = nuspecBin.decode(detect_codec(nuspecBin, 'utf-8'))
        # parse XML and select metadata node
        xml = XML(re.sub(' xmlns="[^"]+"', '', nuspecStr, count=1))
        metadata = xml.find('metadata')

        repositories = []
        for rep in metadata.findall("repository"):
            repositories.append({
                "type": rep.attrib['type'] if 'type' in rep.attrib else None,
                "url": rep.attrib['url'] if 'url' in rep.attrib else None,
                "branch": rep.attrib['branch'] if 'branch' in rep.attrib else None,
                "commit": rep.attrib['commit'] if 'commit' in rep.attrib else None
            })

        pkgInfo = [
            getsize(pkg),
            base64.standard_b64encode(hash_file(pkg).digest()).decode('utf-8'),
            metadata.findtext("id"),
            metadata.findtext("version"),
            metadata.findtext("authors"),
            metadata.findtext("description"),
            metadata.findtext("summary", default=None),
            json.dumps(repositories),
            metadata.findtext("license", default=metadata.findtext("licenseUrl", default=None)),
            metadata.findtext("title", default=None),
            metadata.findtext("projectUrl", default=None),
            metadata.findtext("releaseNotes", default=None),
            metadata.findtext("copyright", default=None),
            metadata.findtext("icon", default=metadata.findtext("iconUrl", default=None)),
            str(uuid.uuid4()),
            datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        ]

        # Next we try to create a storage directory and save needed files
        try:
            pkgPath = join(self._config.get("packages"), pkgInfo[2].lower())
            if not exists(pkgPath):
                mkdir(pkgPath)

            pkgFilename = join(pkgPath, f"{pkgInfo[2].lower()}.{pkgInfo[3].lower()}.nupkg")
            nuspecFilename = join(pkgPath, f"{pkgInfo[2].lower()}.{pkgInfo[3].lower()}.nuspec")
            copy(pkg, pkgFilename)

            with open(nuspecFilename, "w") as f:
                f.writelines(nuspecStr)
        except Exception as ex:
            self._log.error(f"Error create package storage path: {ex}")
            return None

        # All Done so try to delete the checkout file
        try:
            remove(pkg)
        except:
            pass

        return pkgInfo
