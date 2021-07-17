from pydantic import BaseSettings


class DbSettings(BaseSettings):
    db_type: str
    db_server: str
    db_name: str
    db_user: str
    db_passwd: str

    def get_settings(self):
        return self.db_type, self.db_server, self.db_name, self.db_user, self.db_passwd


class ElasticSettings(BaseSettings):
    es_host: str