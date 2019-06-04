# ley Transparente

## VM Amazon
To access your instance:
Locate your private key file (leytransparente.pem). The wizard automatically detects the key you used to launch the instance.

Your key must not be publicly viewable for SSH to work. Use this command if needed:

chmod 400 leytransparente.pem

Connect to your instance using its Public DNS:

ec2-54-214-127-118.us-west-2.compute.amazonaws.com

Example:
ssh -i "leytransparente.pem" ubuntu@ec2-54-214-127-118.us-west-2.compute.amazonaws.com

Please note that in most cases the username above will be correct, however please ensure that you read your AMI usage instructions to ensure that the AMI owner has not changed the default AMI username.

If you need any assistance connecting to your instance, please see our connection documentation.