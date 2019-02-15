from google.cloud import datastore
import config
import socket

builtin_list = list


def get_client():
    if socket.gethostname() == 'Chizzler':
        db = datastore.Client('craigstanton2', namespace='base-db')
    else:
        db = datastore.Client('craigstanton2', namespace='prod-db')
    return db

def from_datastore(entity):
    """Translates Datastore results into the format expected by the
    application.

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        {id: id, prop: val, ...}
    """
    if not entity:
        return None
    if isinstance(entity, builtin_list):
        entity = entity.pop()

    entity['id'] = entity.key.id
    return entity


def update(data):
    ds = get_client()
    
    # Can use the key'5717023518621696'
    key = ds.key('blogbase')

    entity = datastore.Entity(key=key)

    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)

def blog_list():
    ds = get_client()
    query = ds.query(kind='blogbase')
    return query.fetch()




#TODO: remove this code below once sure it doesnt add any more value

datastore_client = datastore.Client()

def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)


def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times


