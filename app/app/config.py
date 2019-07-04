import os


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ('TRUE', '1')

    return result


SECRET_KEY = 'issosecret'
DOMAIN = os.getenv("DOMAIN")
BIGDATA_PRIVATE_KEY = os.getenv('BIGDATA_PRIVATE_KEY')
COUCHBASE_MEMORY_QUOTA_MB = os.getenv('COUCHBASE_MEMORY_QUOTA_MB', '256')
COUCHBASE_INDEX_MEMORY_QUOTA_MB = os.getenv(
    'COUCHBASE_INDEX_MEMORY_QUOTA_MB'
    '256'
)
COUCHBASE_FTS_MEMORY_QUOTA_MB = os.getenv(
    'COUCHBASE_FTS_MEMORY_QUOTA_MB',
    '256'
)
COUCHBASE_HOST = os.getenv('COUCHBASE_HOST', 'couchbase')
COUCHBASE_PORT = os.getenv('COUCHBASE_PORT', '8091')
COUCHBASE_FULL_TEXT_PORT = os.getenv('COUCHBASE_FULL_TEXT_PORT', '8094')
COUCHBASE_ENTERPRISE = getenv_boolean('COUCHBASE_ENTERPRISE')
COUCHBASE_USER = os.getenv('COUCHBASE_USER', 'admin')
COUCHBASE_PASSWORD = os.getenv('COUCHBASE_PASSWORD', 'admin.2010%')
COUCHBASE_BUCKET_NAME = os.getenv('COUCHBASE_BUCKET_NAME', 'app')

# Couchbase query timeouts
COUCHBASE_DURABILITY_TIMEOUT_SECS = 60.0
COUCHBASE_OPERATION_TIMEOUT_SECS = 30.0
COUCHBASE_N1QL_TIMEOUT_SECS = 300.0

# Couchbase Sync Gateway settings
COUCHBASE_CORS_ORIGINS = os.getenv('COUCHBASE_CORS_ORIGINS')

