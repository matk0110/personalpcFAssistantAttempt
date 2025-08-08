# Deprecated legacy module. Use core.persistence.JsonFilePersistence.
class PersistenceManager:  # kept for backward compatibility
    def __init__(self, *_, **__):
        raise RuntimeError("PersistenceManager is deprecated. Use JsonFilePersistence.")