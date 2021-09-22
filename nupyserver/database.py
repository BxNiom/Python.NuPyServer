import logging
import sqlite3
from os.path import exists
from sqlite3 import Error, Connection, Cursor


class Database:
    def __init__(self, dbFile):
        self._dbFile = dbFile
        self._log = logging.getLogger("DB")
        if not exists(dbFile):
            self._log.info("Create new database")
            self.connect(lambda c: c.cursor().executescript(__DDL__))

    def connect(self, handler):
        try:
            conn = sqlite3.connect(self._dbFile)
            return handler(conn)
        except Error as sqlErr:
            print(sqlErr)
        finally:
            if conn:
                conn.close()

    def scala(self, table: str, column: str, where: str = None, order: str = None,
              distinct: bool = True):
        sql = "SELECT{d} {col} FROM {tbl}{w}{o} LIMIT 1".format(
            d=" DISTINCT" if distinct else "",
            col=column,
            tbl=table,
            w=f" WHERE {where}" if where else "",
            o=f" ORDER BY {column} {order}" if order else ""
        )

        self._log.debug("Scala: " + sql)
        r = self.connect(lambda conn: conn.cursor().execute(sql).fetchOne())
        return r[0] if r is not None else None

    def list_column(self, table: str, column: str, where: str = None, order: str = None,
                    distinct: bool = True, offset: int = 0, limit: int = 500) -> list:
        sql = "SELECT{d} {col} FROM {tbl}{w}{o} LIMIT {li} OFFSET {of}".format(
            d=" DISTINCT" if distinct else "",
            col=column,
            tbl=table,
            w=f" WHERE {where}" if where else "",
            o=f" ORDER BY {column} {order}" if order else "",
            li=limit,
            of=offset
        )
        self._log.debug("List column: " + sql)

        def _handler(conn: Connection) -> list:
            lst = []
            cur = conn.cursor().execute(sql)
            for rec in cur:
                lst.append(rec[0])
            return lst

        return self.connect(_handler)

    def count(self, table: str, column: str, where: str = None, distinct: bool = True,
              offset: int = 0, limit: int = 500) -> int:
        sql = "SELECT{d} COUNT({col}) FROM {tbl}{w} LIMIT {li} OFFSET {of}".format(
            d=" DISTINCT" if distinct else "",
            col=column,
            tbl=table,
            w=f" WHERE {where}" if where else "",
            li=limit,
            of=offset
        )

        self._log.debug("Count: " + sql)
        r = self.connect(lambda conn: conn.cursor().execute(sql).fetchOne())
        return r[0] if r is not None else 0

    def foreach(self, sql, action):
        def _handler(conn):
            cursor = conn.cursor()
            cursor.execute(sql)
            for record in cursor:
                action(record)

        self._log.debug("ForEach: " + sql)
        self.connect(_handler)

    def insert_many(self, table: str, columns: [], items: []):
        if len(items) == 0:
            return

        sql = self._create_insert_stmt(table, columns)
        self._log.debug("Insert many: " + sql)

        def _handler(conn):
            cursor: Cursor = conn.cursor()
            cursor.executemany(sql, items)
            conn.commit()

        self.connect(_handler)

    def _create_insert_stmt(self, table, columns):
        cols = ""
        vals = ""

        for col in columns:
            cols += f"{col},"
            vals += "?,"

        return f"INSERT INTO {table}({cols[:-1]}) VALUES({vals[:-1]})"


__DDL__ = """
-- SQLite DDL for NuPyServer
-- !!! DO NOT CHANGE !!!

create table tbl_packages
(
    pkg_id                 integer not null
        constraint tbl_packages_pk
            primary key autoincrement,
    pkg_file_size          integer not null,
    pkg_file_hash          text    not null,
    pkg_info_id            text    not null,
    pkg_info_version       text    not null,
    pkg_info_authors       text    not null,
    pkg_info_description   text    not null,
    pkg_info_summary       text,
    pkg_info_repos         text,
    pkg_info_license       text,
    pkg_info_title         text,
    pkg_info_url           text,
    pkg_info_release_notes text,
    pkg_info_copyright     text,
    pkg_info_icon          text,
    pkg_dep                bool default false not null,
    pkg_dep_msg            text,
    pkg_commit_id          text    not null,
    pkg_commit_timestamp   text    not null
);

create unique index tbl_packages_uidx
    on tbl_packages (pkg_info_id, pkg_info_version);
"""
