import requests
from ..exceptions.wms_exception import S3Exception
def upload(data, file):
    files = {'file':file.read()}
    response = requests.post(data['url'], data = data['fields'],files= files)
    if response.status_code == 200 or response.status_code== 204:
        return 'Document Uploaded successfully'
    else:
        raise S3Exception("Unable to upload documents to s3")

def get_token(request, api_gateway):
    response = requests.post(api_gateway)
    if response.status_code == 200:
        return response.json()
    else:
        raise S3Exception("Unable to upload documents to s3")