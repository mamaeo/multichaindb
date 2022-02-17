
from arango import ArangoClient

class ArangoConnection(ArangoClient):

    def __init__(self, hosts, username=None, password=None, **kwargs):
        super().__init__(hosts, kwargs)
        # Define defaults credentials
        self.username = username if username is not None else 'root'
        self.password = password if password is not None else ''
        '''The system database has some special privileges and properties,
        for example, database management operations such as create or drop
        can only be executed from within this database.
        Additionally, the _system database itself cannot be dropped'''
        self._system = None

    @property
    def system(self):
        if not self._system:
            self._system = self.db('_system', username=self.username,
                password=self.password, verify=True)
        return self._system
    
    def has_database(self, dbname):
        return self.system.has_database(dbname)

    def create_database(self, dbname, *args):
        return self.system.create_database(dbname, args)

    def __getitem__(self, dbname):
        return self.db(dbname, self.username, self.password)