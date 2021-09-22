from nupyserver.v3.services import BaseService


class QueryService(BaseService):
    _columns = "pkg_info_id, pkg_info_description, pkg_info_icon, pkg_info_license, " + \
               "pkg_info_url, pkg_info_summary, pkg_info_title"

    def register_services(self):
        self.services.add_service("/v3/query", "SearchQueryService")
        self.services.add_service("/v3/query", "SearchQueryService/3.0.0-beta")
        self.services.add_service("/v3/query", "SearchQueryService/3.0.0-RC")
        self.services.add_service("/v3/query", "SearchQueryService/3.5.0")

    def register_routes(self):
        @self.server.get("/v3/query")
        def _query(q: str = None, skip: int = 0, take: int = 500, prerelease: bool = False):
            return self._on_query(q, skip, take, prerelease)

    def _on_query(self, q: str, skip: int, take: int, prerelease: bool):
        sql = "SELECT DISTINCT {cols} FROM tbl_packages {where}{pre}LIMIT {take} OFFSET {skip}".format(
            cols=self._columns,
            where="" if q is None else "WHERE (pkg_info_id LIKE " +
                                       "{t} OR pkg_info_description LIKE {t} OR pkg_info_title LIKE {t}) ".format(
                                           t=f"'%{q}%'"
                                       ),
            pre="" if prerelease else ("AND " if q else "WHERE ") + "pkg_info_version NOT LIKE '%-%' ",
            take=take,
            skip=skip
        )

        data = []

        def _handler(cur):
            versions = self.db.list_column("tbl_packages", "pkg_info_version", where=f"pkg_info_id = '{cur[0]}'")
            info = {
                "id": cur[0],
                "version": versions[len(versions) - 1],
                "description": cur[1],
                "iconUrl": cur[2],
                "licenseUrl": cur[3],
                "projectUrl": cur[4],
                "summary": cur[5],
                "title": cur[6],
                "totalDownloads": 0,
                "verified": True,
                "versions": [],
                "authors": self.db.list_column("tbl_packages", "pkg_info_authors", where=f"pkg_info_id = '{cur[0]}'")}

            for ver in versions:
                info["versions"].append({
                    "version": ver,
                    "download": 0,
                    "@id": f"{self.config.get('_app', 'url')}/v3/registry/{cur[0]}/{ver}"
                })
            data.append(info)

        self.db.foreach(sql, _handler)

        return {
            "totalHits": len(data),
            "data": data
        }
