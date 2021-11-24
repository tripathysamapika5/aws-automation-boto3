import sys
import os

PROJECT_DIR = os.getcwd()
sys.path.append(PROJECT_DIR)

from src.aws_resources.client_locator import EC2Client, STSClient
from src.aws_resources.resource_locator import EC2Resource

from src.ec2.snapshot import SnapshotService
from src.sts.sts import STS


def print_all_snapshots():
    ec2_client_service = EC2Client()
    snapshot_2 = SnapshotService().set_client(ec2_client_service)

    print("printing using client...")
    for snapshot in snapshot_2.get_all_snapshots():
        print(snapshot)

    ec2_resource_service = EC2Resource()
    snapshot_1 = SnapshotService().set_resource(ec2_resource_service)

    print("printing using resource...")
    for snapshot in snapshot_1.get_all_snapshots():
        print(snapshot)

    sts_client_svc_samapika = STSClient()
    sts = STS(sts_client_svc_samapika)
    owner_id = sts.get_account_id()

    print("printing using client by passing owner Id :{}...".format(owner_id))
    for snapshot in snapshot_2.get_all_snapshots(owner_ids=[owner_id]):
        print(snapshot)

    print("printing using resource by passing owner Id :{}...".format(owner_id))
    for snapshot in snapshot_1.get_all_snapshots(owner_ids=[owner_id]):
        print(snapshot)


def print_snapshots_filtered_on_volume_size():
    ec2_client_service = EC2Client()
    snapshot_2 = SnapshotService().set_client(ec2_client_service)

    print("printing using client...")
    volume_sizes = [8]
    for snapshot in snapshot_2.get_snapshots_filtered_on_volume_size(volume_sizes, filters=[]):
        print(snapshot)

    ec2_resource_service = EC2Resource()
    snapshot_1 = SnapshotService().set_resource(ec2_resource_service)

    print("printing using resource...")
    volume_sizes = ["1"]
    for snapshot in snapshot_1.get_snapshots_filtered_on_volume_size(volume_sizes, filters=[]):
        print(snapshot)


if __name__ == '__main__':
    print("Testing snapshot deployments")
    print_all_snapshots()
    print_snapshots_filtered_on_volume_size()
