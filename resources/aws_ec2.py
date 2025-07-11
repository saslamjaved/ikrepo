import boto3

   session = boto3.Session(
      aws_access_key_id='YOUR_ACCESS_KEY',
      aws_secret_access_key='YOUR_SECRET_KEY',
      region_name='us-west-2'
   )

   ec2_resource = session.resource('ec2')

   instances = ec2_resource.create_instances(
      ImageId='ami-0c55b159cbfafe1f0',
      MinCount=1,
      MaxCount=1,
      InstanceType='t2.micro',
      TagSpecifications=[
         {
            'ResourceType': 'instance',
            'Tags': [
               {
                  'Key': 'Name',
                  'Value': 'MyInstance'
               },
            ]
         },
      ]
   )