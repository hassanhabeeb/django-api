class UserBasedRouter:
    def db_for_read(self, model, **hints):
        user = hints.get('user')
        if user and hasattr(user, 'replica_db') and user.replica_db:
            return user.replica_db
        return 'default'  # Default database if user's replica_db is not set

    def db_for_write(self, model, **hints):
        user = hints.get('user')
        if user and hasattr(user, 'replica_db') and user.replica_db:
            return user.replica_db
        return 'default'  # Default database if user's replica_db is not set

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations between any databases
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Allow all models to be migrated in all databases
        return True


class ReplicaDRouter:
    def db_for_read(self, model, **hints):
        # Always return 'replica_1' for reading ReplicaCount data in the admin panel
        if model._meta.app_label == 'apps.clientlimit' and model._meta.db_table == 'ReplicaCount':
            return 'replica_1'
        return None

    def db_for_write(self, model, **hints):
       
        if model._meta.app_label == 'apps.clientlimit' and model._meta.db_table == 'ReplicaCount':
            return 'replica_1'
        return None

    def allow_relation(self, obj1, obj2, **hints):
       
        if 'replica_1' in [obj1._state.db, obj2._state.db]:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        
        if db == 'replica_1':
            return app_label == 'apps.clientlimit'
        return None
