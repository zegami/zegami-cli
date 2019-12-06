# Copyright 2019 Zegami Ltd

"""Generate sas tokens to download images from azure."""


from datetime import datetime, timedelta
import os

from azure.storage.blob import BlockBlobService
from azure.storage.blob import BlobPermissions


def generate_signed_url(azure_container):
    connection_string = os.getenv(
        'AZURE_STORAGE_CONNECTION_STRING'
    )
    return generate_sas_with_sdk(connection_string, azure_container)


def build_creds(connection_string):
    return (
        connection_string.split('AccountName=')[1].split(';')[0],
        connection_string.split('AccountKey=')[1].split(';')[0],
    )


def generate_sas_with_sdk(connection_string, azure_container):
    account_name, account_key = build_creds(connection_string)
    block_blob_service = BlockBlobService(
        account_name=account_name, account_key=account_key)
    sas_url = block_blob_service.generate_container_shared_access_signature(
        azure_container,
        BlobPermissions.READ,
        datetime.utcnow() + timedelta(hours=1)
    )
    return 'https://{}.blob.core.windows.net/{}/{{}}?{}'.format(
        account_name, azure_container, sas_url
    )
