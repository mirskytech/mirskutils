class ModelDatabaseRouter(object):
    """Allows each model to set its own destiny"""
    
    def db_for_read(self, model, **hints):
        # Specify target database with field in_db in model's Meta class
        if hasattr(model._meta, 'in_db'):
            return model._meta.in_db
        return None

    def db_for_write(self, model, **hints):
        # Specify target database with field in_db in model's Meta class
        if hasattr(model._meta, 'in_db'):
            return model._meta.in_db        
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        obj1_db = getattr(obj1._meta,'in_db','default')
        obj2_db = getattr(obj2._meta,'in_db','default')
        
        if obj1_db == obj2_db:
            return True
        return None
    
    def allow_syncdb(self, db, model):      
        # Specify target database with field in_db in model's Meta class
        if hasattr(model._meta, 'in_db'):
            if model._meta.in_db == db:
                return True
            else:
                return False
        else:
            # Random models that don't specify a database can only go to 'default'
            if db == 'default':
                return True
            else:
                return False
