import boto3

# Instantiate a boto3 resource for s3
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/service-resource/index.html#S3.ServiceResource
s3 = boto3.resource('s3')
# Bucket names cannot have '_'
bucket_name = 'lj-s3-crud-1'

# Check if bucket exists
# Create bucket if it does NOT exist
all_my_buckets = [bucket.name for bucket in s3.buckets.all()]
if bucket_name not in all_my_buckets:
  print(f"'{bucket_name}' bucket does not exist. Creating now...")
  s3.create_bucket(Bucket=bucket_name)
  print(f"'{bucket_name}' bucket has been created.")
else:
  print(f"'{bucket_name}' bucket already exists. No need to create new one.")
