import os

base_dir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.join(base_dir, '../db/api_db.sqlite')

class _Config(object):
	SQLALCHEMY_DATABASE_URI = "sqlite:///" + db_dir


class _DevelopmentConfig(_Config):
	DEBUG = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_ECHO = False

class _GaeDevelopmentMigrationConfig(_Config):
	DEBUG = False

class _GaeDevelopmentConfig(_Config):
	DEBUG = False

_configs = {
	'development': _DevelopmentConfig,
	'gae_development': _GaeDevelopmentConfig,
	'gae_development_migration': _GaeDevelopmentMigrationConfig
}

config = _configs[os.getenv('ENVINRONMENT', 'development')]