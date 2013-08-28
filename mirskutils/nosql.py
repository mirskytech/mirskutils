from couchdb import client, PreconditionFailed
from django.conf import settings
from couchdb.design import ViewDefinition
from uuid import uuid4


class Server(object):
        
    def __init__(self, name, model_class, *args, **kwargs):
        self._db = None
        self.name = name
        self._registry = [] # simple at first, just register the ViewDefinition
        self.klass = model_class
    
    # since this could be called from a fork, we're not guaranteed a connection
    # http://code.google.com/p/couchdb-python/issues/detail?id=205    
    def db(self):
        if not self._db:
            server = client.Server(url=settings.COUCHDB_SERVER)    
            server.resource.credentials = (settings.COUCHDB_USERNAME, settings.COUCHDB_PASSWORD)
            try:
                server.create(self.name)
            except PreconditionFailed:
                pass
            finally:
                self._db = server[self.name]
                
        return self._db
    
    def load(self, _id):
        return self.klass.load(self.db(), _id)
    
    def store(self, obj):
        if isinstance(obj, self.klass):
            return obj.store(self.db())
        raise TypeError("'%s' should be of type %s" % (type(obj),self.klass.__name__))

    def remove(self, obj):
        if isinstance(obj, self.klass):
            return self.db().delete(obj)
        raise TypeError("'%s' should be of type %s" % (type(obj),self.klass.__name__))
    
    def sync(self, view_definition, force=False):
        if not force:
            # TODO ?? check to see if the view is already registered. by pass if it is. (?)
            raise PreconditionFailed('View syncing causes index rebuilds. Force sync required.')
        return view_definition.sync(self.db())
    
    def sync_all(self):
        # TODO : add ability to pass in a list of ViewDefinitions (?)
        # TODO : optimization check the db to see if the viewdefinition has changed (compare function?) (?)
        for vd in self._registry:
            self.sync(vd, True)
        
    def register(self, view_definition):
        if not isinstance(view_definition, ViewDefinition):
            raise TypeError('%s should be of type \'couchdb.design.ViewDefinition\'')
        
        # TODO: should check that two views aren't registered with the same primary/secondary key
        self._registry.append(view_definition)
    
    def create(self, main, secondary, function):
        view_definition = ViewDefinition(main, secondary, function)
        return self.sync(view_definition)
    
    def view(self, view, **params):
        return self.klass.view(self.db(), view, **params)
    
    def copy(self, doc_or_id):
        _id = uuid4().hex
        self.db().copy(doc_or_id, _id)
        return self.load(_id)
    
    def query(self, view_function, **params):
        return self.db().query(view_function, **params)
