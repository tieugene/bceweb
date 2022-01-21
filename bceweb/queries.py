"""SQL queries storage"""
import os


class Qry:
    __storage: dict = {}

    @staticmethod
    def __chk_load() -> bool:
        """Load __storage on demand"""
        if not Qry.__storage:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            sql_dir = os.path.join(base_dir, 'sql')
            with os.scandir(sql_dir) as itr:
                for entry in itr:
                    if not entry.is_file() or not entry.name.endswith('.sql'):
                        continue
                    with open(entry.path, 'rt') as istream:
                        Qry.__storage[entry.name[:-4].upper()] = istream.read()
        return True

    @staticmethod
    def get(name: str):
        if Qry.__chk_load():
            return Qry.__storage.get(name)
