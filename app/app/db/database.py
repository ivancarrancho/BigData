from couchbase import LOCKMODE_WAIT
from couchbase.bucket import Bucket
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator

from config import COUCHBASE_BUCKET_NAME
from config import COUCHBASE_HOST
from config import COUCHBASE_N1QL_TIMEOUT_SECS
from config import COUCHBASE_OPERATION_TIMEOUT_SECS
from config import COUCHBASE_PASSWORD
from config import COUCHBASE_PORT
from config import COUCHBASE_USER
from db.couchbase_utils import get_cluster_couchbase_url


def get_default_bucket():
    return get_bucket(
        username=COUCHBASE_USER,
        password=COUCHBASE_PASSWORD,
        bucket_name=COUCHBASE_BUCKET_NAME,
        host=COUCHBASE_HOST,
        port=COUCHBASE_PORT,
    )


def get_cluster(username: str, password: str, host='couchbase', port='8091'):
    cluster_url = get_cluster_couchbase_url(host=host, port=port)
    cluster = Cluster(cluster_url)
    authenticator = PasswordAuthenticator(username, password)
    cluster.authenticate(authenticator)

    return cluster


def get_bucket(
    username: str,
    password: str,
    bucket_name: str,
    host='couchbase',
    port='8091',
    timeout: float = COUCHBASE_OPERATION_TIMEOUT_SECS,
    n1ql_timeout: float = COUCHBASE_N1QL_TIMEOUT_SECS,
):
    cluster = get_cluster(
        username=username,
        password=password,
        host=host,
        port=port
    )
    bucket = cluster.open_bucket(bucket_name, lockmode=LOCKMODE_WAIT)
    bucket.timeout = timeout
    bucket.n1ql_timeout = n1ql_timeout

    return bucket


def ensure_create_primary_index(bucket: Bucket):
    manager = bucket.bucket_manager()
    return manager.n1ql_index_create_primary(ignore_exists=True)


def ensure_create_type_index(bucket: Bucket):
    manager = bucket.bucket_manager()

    return manager.n1ql_index_create(
        'idx_type',
        ignore_exists=True,
        fields=['type']
    )
