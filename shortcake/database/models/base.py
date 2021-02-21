import peewee

database_proxy = peewee.Proxy()


class BaseModel(peewee.Model):
    class Meta:
        database = database_proxy
        # TODO: Remove in Peewee 4
        legacy_table_names = False
