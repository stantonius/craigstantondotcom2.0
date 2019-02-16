#TODO: create a new datastore kind
#TODO: create a new storage bucket, including folders
#TODO: add folder upload to form
#TODO: match datastore submission with file storage meta data
#TODO: view the storage bucket file by calling the datastore details (account and prevent for posts with either content or file)

from google.cloud.storage import Blob

client = storage.Client()
bucket = client.get_bucket('blogdocs')
blob = Blob('PLACEHOLDER_FOR_NAME_FROM_FORM_OR_FILE', bucket)
with open('PLACEHOLDER_FOR_FILE_FROM_FORM', 'rb') as NAME_OF_FILE_TO_GO_INTO_DATASTORE:
    blob.upload_from_file(NAME_OF_FILE_TO_GO_INTO_DATASTORE)

