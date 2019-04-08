from google.cloud import datastore
import config
import socket
import mistune

from google.cloud import storage
from google.cloud.storage import Blob
from werkzeug.utils import secure_filename

client = storage.Client()

def get_storage():  
    if socket.gethostname() == 'Chizzler':
        bucket = client.get_bucket('blogdocs')
    else:
        bucket = client.get_bucket('prod-blogdocs')
    return bucket


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'md'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_upload(file, request_date):
    if file and allowed_file(file.filename):
        new_file_name = request_date.replace(" ", "-").replace(":", "-") + "_" + file.filename
        safename = secure_filename(new_file_name)
        blob = Blob(safename, get_storage())
        blob.upload_from_file(file)
    print('File uploaded successfully')


def get_file(post_filename):
    blob = Blob(post_filename, get_storage())
    blog_as_text = blob.download_as_string().decode()
    return mistune.markdown(blog_as_text, escape=True, hard_wrap=True)


def get_file_link(post_filename):
    blob = Blob(post_filename, get_storage())
    file = blob.download_to_file()
    return file

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


def update(data, id=None):
    ds = get_client()
    if id:
        key = ds.key('blogbase', int(id))
    else:
        key = ds.key('blogbase')

    entity = datastore.Entity(key=key)

    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)

def blog_list():
    ds = get_client()
    query = ds.query(kind='blogbase')
    query.order = ['-date_posted']

    return query.fetch()

def read(id):
    ds = get_client()
    key = ds.key('blogbase', int(id))
    results = ds.get(key)
    return from_datastore(results)






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


