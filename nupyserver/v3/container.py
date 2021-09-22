from os.path import join

from fastapi import HTTPException
from fastapi.responses import FileResponse, Response

from nupyserver.v3.services import BaseService


class ContainerService(BaseService):
    def register_services(self):
        self.services.add_service("/v3/container/", "PackageBaseAddress/3.0.0")

    def register_routes(self):
        # Add routes to server
        @self.server.get("/v3/container/{pkgid}/index.json")
        def _get_package_versions(pkgid: str):
            return self.on_get_versions(pkgid.lower())

        @self.server.get("/v3/container/{pkgid}/{pkgver}/{file}")
        def _get_package(pkgid: str, pkgver: str, file: str):
            if f"{pkgid}.{pkgver}" != file[:file.rindex(".")]:
                raise HTTPException(status_code=404, detail="File not found")

            pkgid = pkgid.lower()
            pkgver = pkgver.lower()

            if file.endswith(".nupkg"):
                return self.on_get_nupkg(pkgid, pkgver)
            elif file.endswith(".nuspec"):
                return self.on_get_nuspec(pkgid, pkgver)
            else:
                raise HTTPException(status_code=422, detail="Unprocessable entitiy")

    def on_get_versions(self, pkgid: str):
        versions = self.db.list_column("tbl_packages", "pkg_info_version",
                                       where=f"LOWER(pkg_info_id)='{pkgid}'")

        if len(versions) == 0:
            raise HTTPException(status_code=404, detail="Item not found")

        return {"versions": versions}

    def on_get_nupkg(self, pkgid: str, pkgver: str):
        filePath = join(self.config.get("_app", "packages"), pkgid, f"{pkgid}.{pkgver}.nupkg")
        return FileResponse(filePath)

    def on_get_nuspec(self, pkgid: str, pkgver: str):
        filePath = join(self.config.get("_app", "packages"), pkgid, f"{pkgid}.{pkgver}.nuspec")
        with open(filePath, "r") as fi:
            return Response(fi.read(), media_type="application/xml")
