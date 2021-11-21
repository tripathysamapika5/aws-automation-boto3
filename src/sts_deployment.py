import sys
import os

PROJECT_DIR = os.getcwd()
sys.path.append(PROJECT_DIR)

from src.aws_resources.client_locator import STSClient

from src.sts.sts import STS

def main():
    sts_client_svc_s3_dev = STSClient(profile_name= "s3_developer")
    sts_client_svc_ec2_dev = STSClient(profile_name= "ec2_developer")
    sts_client_svc_samapika = STSClient()
    
    sts_s3_dev = STS(sts_client_svc_s3_dev)
    print("user : s3_developer, user id : {}, account id : {}, arn : {}"
          .format(
              sts_s3_dev.get_user_id(),
              sts_s3_dev.get_account_id(),
              sts_s3_dev.get_iam_user_arn()
              )
          )
    
    sts_ec2_dev = STS(sts_client_svc_ec2_dev)
    print("user : ec2_developer, user id : {}, account id : {}, arn : {}"
          .format(
              sts_ec2_dev.get_user_id(),
              sts_ec2_dev.get_account_id(),
              sts_ec2_dev.get_iam_user_arn()
              )
          )

    sts_samapika = STS(sts_client_svc_samapika)
    print("user : samapika, user id : {}, account id : {}, arn : {}"
          .format(
              sts_samapika.get_user_id(),
              sts_samapika.get_account_id(),
              sts_samapika.get_iam_user_arn()
              )
          )
    
if __name__ == '__main__':
    main()