# VPC is created with the EC2 resource/client.
import boto3
import time

# Create VPC
ec2 = boto3.client('ec2')
vpc_name = 'vpc-lj'

## Getting VPC info stored in vpcs to run checks if VPC exists.

response = ec2.describe_vpcs(
  Filters=[{'Name': 'tag:Name', 'Values': [vpc_name]}]
  )

vpcs = response.get('Vpcs', [])

if vpcs:
  vpc_id = vpcs[0]['VpcId']
  print(f"VPC '{vpc_name}' with ID '{vpc_id}' already exists")
else:
  vpc_response = ec2.create_vpc(CidrBlock='10.0.0.0/16')
  vpc_id = vpc_response['Vpc']['VpcId']

  time.sleep(5)

  ec2.create_tags(Resources=[vpc_id], Tags=[{'Key': 'Name', 'Value': vpc_name}])
  print(f"VPC '{vpc_name}' with ID '{vpc_id}' has been created.")

# Create internet gateway
ig_name = 'ig-vpc-lj'
response = ec2.describe_internet_gateways(
  Filters=[{'Name': 'tag:Name', 'Values': [ig_name]}]
  )

internet_gateways = response.get('InternetGateways', [])

if internet_gateways:
  ig_id = internet_gateways[0]['InternetGateways']
  print(f"Internet Gateway '{ig_name}' with ID '{ig_id}' already exists")
else:
  ig_response = ec2.create_internet_gateway()
  ig_id = ig_response['InternetGateway']['InternetGatewayId']
  ec2.create_tags(Resources=[ig_id], Tags=[{'Key': 'Name', 'Value': ig_name}])
  ec2.attach_internet_gateway(VpcId=vpc_id, InternetGatewayId=ig_id)
  print(f"Internet Gateway '{ig_name}' with ID '{ig_id}' has been created.")

# Create a route table and public route
rt_response = ec2.create_route_table(VpcId=vpc_id)
rt_id = rt_response['RouteTable']['RouteTableId']
route = ec2.create_route(
  RouteTable=rt_id,
  DestinationCidrBlock='0.0.0.0/0',
  GatewayId=ig_id
  )
print(f"Route Table with ID '{rt_id}' has been created.")

# Create 3 subnets

