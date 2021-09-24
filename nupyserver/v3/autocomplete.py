from nupyserver.v3.services import BaseService


class AutoCompleteService(BaseService):
    def register_services(self):
        self.services.add_service("/v3/auto", "SearchAutoCompleteService")
        self.services.add_service("/v3/auto", "SearchAutoCompleteService/3.0.0-beta")
        self.services.add_service("/v3/auto", "SearchAutoCompleteService/3.0.0-RC")
        self.services.add_service("/v3/auto", "SearchAutoCompleteService/3.5.0")

    def register_routes(self):
        @self.server.get("/v3/auto")
        def _autocomplete(q: str = None, skip: int = 0, take: int = 500, prerelease: bool = False, pkgid: str = None):
            if pkgid:
                return self.on_auto_versions(pkgid.lower(), q, skip, take, prerelease)
            else:
                return self.on_auto(q, skip, take, prerelease)

    def on_auto(self, q: str, skip: int, take: int, prerelease: bool):
        sql = "SELECT DISTINCT pkg_info_id FROM tbl_packages {where}{pre}LIMIT {take} OFFSET {skip}".format(
            where="" if q is None else "WHERE (pkg_info_id LIKE " +
                                       "{t} OR pkg_info_description LIKE {t} OR pkg_info_title LIKE {t}) ".format(
                                           t=f"'{q}%'"
                                       ),
            pre="" if prerelease else ("AND " if q else "WHERE ") + "pkg_info_version NOT LIKE '%-%' ",
            take=take,
            skip=skip
        )

        data = []

        def _handler(cur):
            data.append(cur[0])

        self.db.foreach(sql, _handler)
        return {
            "totalHits": len(data),
            "data": data
        }

    def on_auto_versions(self, pkgid: str, q: str, skip: int, take: int, prerelease: bool):
        return {"data": self.db.list_column("tbl_packages", "pkg_info_version",
                                            where=f"LOWER(pkg_info_id)='{pkgid}'" +
                                                  ("" if prerelease else " AND pkg_info_version NOT LIKE '%-%'"))}
