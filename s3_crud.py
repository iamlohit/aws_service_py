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

# Create 'file_1' & 'file_2'
file_1 = 'file_1.txt'
file_2 = 'file_2.txt'

# Upload 'file_1' to the new bucket
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/upload_file.html
s3.Bucket(bucket_name).upload_file(Filename=file_1, Key=file_1)
# OR by using Client instead of resource Positional Args
# S3.Client.upload_file(Filename, Bucket, Key, ExtraArgs=None, Callback=None, Config=None)
s3c = boto3.client('s3')
s3c.upload_file(file_1, bucket_name, file_1)

# READ & print the file from the bucket
obj = s3.Object(bucket_name, file_1)
body = obj.get()['Body'].read()
print(body)

# Update 'file_1' in bucket with new content from 'file_2'
s3.Object(bucket_name, file_1).put(Body=open(file_2, 'rb'))
obj = s3.Object(bucket_name, file_1)
# Print to check the updated body.
body = obj.get()['Body'].read()
print(body)

# Delete the file from bucket
s3.Object(bucket_name, file_1).delete()

# Delete the bucket (Bucket should be empty)
bucket = s3.Bucket(bucket_name)
bucket.delete()