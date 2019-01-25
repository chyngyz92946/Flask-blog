class Configuration(object):
	DEBUG = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:qwerty@localhost/dbforblog'
	SECRET_KEY = 'very very secret key'

	### Flask Security
	SECURITY_PASSWORD_SALT = 'salt'
	SECURITY_PASSWORD_HASH = 'sha512_crypt' 
