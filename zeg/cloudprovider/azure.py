import time
import uuid
import hmac
import base64
import hashlib
import urllib
from datetime import datetime, timedelta
from azure.storage import (
    AccessPolicy,
    ResourceTypes,
    AccountPermissions,
    CloudStorageAccount,
)
from azure.storage.blob import (
    BlockBlobService,
    ContainerPermissions,
    BlobPermissions,
    PublicAccess,
)

AZURE_ACC_NAME = '<account_name>'
AZURE_PRIMARY_KEY = '<account_key>'
AZURE_CONTAINER = '<container_name>'

def generate_sas_with_sdk():
    block_blob_service = BlockBlobService(connection_string)
    sas_url = block_blob_service.generate_container_shared_access_signature(
        AZURE_CONTAINER,
        BlobPermissions.READ,
        datetime.utcnow() + timedelta(hours=1)
    )
    #print sas_url
    print 'https://'+ block_blob_service.account_name +'.blob.core.windows.net/'+ AZURE_CONTAINER +'/{}?'+ sas_url
