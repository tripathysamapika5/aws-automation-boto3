# to install python on linux and making python3 available to the linux in any path. 
But python3.7 is already there so choice is urs. to install or not.

https://tecadmin.net/install-python-3-8-amazon-linux/

```
cd /usr/local/bin
ls -l
ln -s /usr/local/bin/python3.7 /bin/python3
ln -s /usr/local/bin/python3.7 /bin/python3
cd /home/ec2-user
python3 -m venv aws
source aws/bin/activate
```

# User data for ec2 instance

```
python3 -m venv aws
source aws/bin/activate
pip3 install boto3
pip3 install awscli
pip3 install pyboto3
```

# aws cli configuration
Create two Iam users for aws account with programatic access
One for full s3 access and one for full ec2 access

```

aws configure --profile ec2_developer
aws configure --profile s3_developer

Example

(aws) (base) BLRC02Z81FNLVCH:aws-code satripathy$ aws configure --profile s3_developer
AWS Access Key ID [None]: XXXXXXXXXXXXXXXXXXXXXX
AWS Secret Access Key [None]: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Default region name [None]: us-east-1
Default output format [None]: json


```

also create a user with admin access with name samapika

```
aws configure --profile samapika
```

# Check your AWS configration profiles by following commands

```
cat  ~/.aws/config
cat  ~/.aws/credentials
```
