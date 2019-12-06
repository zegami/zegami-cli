import base64
from datetime import datetime, timedelta
import hmac
import hashlib
import os
import time
import urllib
import uuid

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


def generate_signed_url(azure_container):
    connection_string = os.environ.get(
        'AZURE_STORAGE_CONNECTION_STRING'
    )
    return generate_sas_with_sdk(connection_string, azure_container)


def generate_sas_with_sdk(connection_string, azure_container):
    block_blob_service = BlockBlobService(connection_string)
    sas_url = block_blob_service.generate_container_shared_access_signature(
        AZURE_CONTAINER,
        BlobPermissions.READ,
        datetime.utcnow() + timedelta(hours=1)
    )
    return 'https://'+ block_blob_service.account_name +'.blob.core.windows.net/'+ azure_container +'/{}?'+ sas_url
