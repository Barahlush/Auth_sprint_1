from peewee_migrate import Router  # type: ignore

from src.db.datastore import datastore

router = Router(datastore)

# Create migration
router.create('auth')

# Run migration/migrations
router.run('auth')

# Run all unapplied migrations
router.run()
