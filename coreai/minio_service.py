from minio import Minio


access_key = "gvOldBjc58YjGNIxTGNx"
secret_key = "SonZwSq3sdFNFaQ3z4QVNYa9Byr6Du3mU9dO5SoW"
server_url = "anhpn.ddns.net:8022"
bucket_name = "mnist"


minio_client = Minio(
    server_url,
    access_key=access_key,
    secret_key=secret_key,
    secure=False
)
    
    