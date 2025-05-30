import boto3
import json

# Create ec2 resource and instance name
ec2 = boto3.resource('ec2')
ec2_client = boto3.client('ec2')
instance_name = 'dct-ec2-lj'
response = ec2_client.describe_instances()

# Print the entire response as pretty JSON
# print(json.dumps(response, indent=2))

# Store the instance id
instance_id = None

# Check if instnace which we are trying to create already exists.
# and only work with an instance that hasn't already been terminated
instances = ec2.instances.all()
instance_exists = False

for instance in instances:
  for tag in instance.tags:
    if tag['Key'] == 'Name' and tag['Value'] == instance_name:
      instance_exists = True
      instance_id = instance.id
      print(f"An instance name '{instance_name} with id '{instance_id}' already exists.")
      print("----------------------------------------------------------------------------")
      print(f"All instances listed below: \n'{instances}'")
      break
    if instance_exists:
      break

if not instance_exists:
# Launch a new EC2 instance if it hasn't already been created
  new_instance = ec2.create_instances(
    ImageId='ami-0554aa6767e249943',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='my-ec2-key',
    TagSpecifications=[
      {
        'ResourceType': 'instance',
        'Tags': [
          {
            'Key': 'Name',
            'Value': instance_name
          }
        ]
      }
    ]
  )
  instance_id = new_instance[0].id
  print(f"An instance name '{instance_name} with id '{instance_id}' has been created.")

# Stop an instance
ec2.Instance(instance_id).stop()
print(f"An instance name '{instance_name} with id '{instance_id}' has been stopped.")

# # Start an instance
# ec2.Instance(instance_id).start()
# print(f"An instance name '{instance_name} with id '{instance_id}' has been started.")

# Terminate an instance
ec2.Instance(instance_id).terminate()
print(f"An instance name '{instance_name} with id '{instance_id}' has been terminated.")