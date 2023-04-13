import os

AWS_ACCESS_KEY_ID=os.environ.get("AWS_ACCESS_KEY_ID")
AWS_S3_ACCESS_KEY_ID=os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_S3_SECRET_ACCESS_KEY=os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME=os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL = 'public-read' 
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
AWS_LOCATION = f"https://{AWS_STORAGE_BUCKET_NAME}.nyc3.digitaloceanspaces.com"
AWS_S3_REGION_NAME = "nyc3"
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400'
}

DEFAULT_FILE_STORAGE = "technance_app.cdn.backends.MediaStorage"
STATICFILES_STORAGE = "technance_app.cdn.backends.StaticStorage"

AWS_STATIC_LOCATION = 'static'
STATIC_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, AWS_STATIC_LOCATION)
STATIC_URL = '/static/'

AWS_MEDIA_LOCATION = 'media'
PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, AWS_MEDIA_LOCATION)
