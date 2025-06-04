import boto3
import time

# NOTE: Creating and running an Aurora v1 cluster on a Free Tier account WILL RESULT IN CHARGES, even if used briefly and then deleted.
#       Cost is $0.06 per hour + any usage charges

# Instantiate a boto3 client for RDS, Note: There is no Resource method for RDS, only client.
rds = boto3.client('rds')

# User Defined Variables
username = 'lj-user1'
password = '2Lxu1hlT'
# You need to have a VPC and subnet pre existing where this cluster will be hosted.
# We still need to create the db_subnet_group on the console of RDS to use the pre existing subnets and assign them to this
# db subnet group and create it, generating the id which we use below.
db_subnet_group = 'rds-aurora-subnet-vpc-lj'
# The cluster id is the name you give to the cluster.
db_cluster_id = 'rds-lj-cluster'

# Create the DB Cluster
## Run a check to see if the db already exists, else create.
try:
  response = rds.desbribe_db_clusters(DBClusterIdentifier=db_cluster_id)
  print(f"The DB cluster named '{db_cluster_id}' already exists. Skipping creation.")
except rds.exceptions.DBClusterNotFoundFault:
  response = rds.create_db_cluster(
    Engine='aurora-mysql',
    EngineVersion='5.7.msql_autota.2.08.3',
    DBClusterIdentifier=db_cluster_id,
    MasterUsername=username,
    MasterUserPassword=password,
    DatabaseName='rds_lj_db',
    DBSubnetGroupName=db_subnet_group,
    EngineMode='serverless',
    EnableHttpEndpoint=True, # This allows us to run Queries (using Query Editor from console) from the console(Only for Aurora V1)
    ScalingConfiguration={
      'MinCapacity': 1, # Min Aurora Compute Units (V1 can scale to 0, v2 can scale to min 0.5 not lower)
      'MaxCapacity': 8, # Max Aurora Compute Unites (V1 doubles: 1,2,4,8 and V2 goes in increments of 0.5)
      'AutoPause': True, # Cannot be done for V2 since only V1 can scale to 0
      'SecondsUntilAutoPause': 300 # Pause after 5 mins of inactivity
    }
  )
  print(f"The DB cluster named '{db_cluster_id}' has been created.")

  # Wait for DB cluster to become available
  while True:
    response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
    status = response['DBClusters'][0]['Status']
    print(f"The status of the cluster is '{status}'")
    if status == 'available':
      break

    print("Waiting for the DB Cluster to become available...")
    time.sleep(40)


# Modify the DB cluster. Update the scaling config for the cluster.
response = rds.modify_db_cluster(
    DBClusterIdentifier=db_cluster_id,
    ScalingConfiguration={
      'MinCapacity': 1, # Min Aurora Compute Units (V1 can scale to 0, v2 can scale to min 0.5 not lower)
      'MaxCapacity': 16, # Max Aurora Compute Unites (V1 doubles: 1,2,4,8 and V2 goes in increments of 0.5)
      'AutoPause': True, # Cannot be done for V2 since only V1 can scale to 0
      'SecondsUntilAutoPause': 600 # Pause after 5 mins of inactivity
    }
  )
print(f"Updated the scaling config for the DB cluster named '{db_cluster_id}'.")

# Delete the DB Cluster
