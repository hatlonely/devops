#!/usr/bin/env python3

import argparse
import json

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkots.request.v20160620.GetInstanceRequest import GetInstanceRequest
from aliyunsdkots.request.v20160620.InsertInstanceRequest import InsertInstanceRequest


def get_instance(client: AcsClient, endpoint, instance_name):
    req = GetInstanceRequest()
    req.set_endpoint(endpoint)
    req.set_InstanceName(instance_name)
    res = client.do_action_with_exception(req)
    return json.loads(str(res, encoding='utf-8'))


def insert_instance(client: AcsClient, endpoint, instance_name, cluster_type=""):
    try:
        return get_instance(client, endpoint, instance_name)
    except ServerException as e:
        if e.http_status != 404:
            raise e
    for typ in cluster_type.split(","):
        try:
            typ = typ.strip()
            req = InsertInstanceRequest()
            req.set_endpoint(endpoint)
            req.set_InstanceName(instance_name)
            req.set_ClusterType(typ)
            res = client.do_action_with_exception(req)
            return json.loads(str(res, encoding='utf-8'))
        except ServerException as e:
            continue
    raise e


def main():
    parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=200), description="""example:
  python3 ots-admin.py -i ak -s sk -e ots.cn-shanghai.aliyuncs.com -a GetInstance --instance-name imm-dev-hl
  python3 ots-admin.py -i ak -s sk -e ots.cn-shanghai.aliyuncs.com -a InsertInstance --instance-name imm-dev-hl-test
""")

    parser.add_argument("-i", "--access-key-id", help="access key id")
    parser.add_argument("-s", "--access-key-secret", help="access key secret")
    parser.add_argument("-r", "--region-id", help="region id")
    parser.add_argument("-e", "--endpoint", help="endpoint")
    parser.add_argument("--instance-name", help="instance name")
    parser.add_argument("--cluster-type", help="cluster type")
    parser.add_argument("-a", "--action", help="action", choices=[
        "GetInstance", "InsertInstance",
    ])
    args = parser.parse_args()
    if not args.endpoint:
        args.endpoint = "ots.{}.aliyuncs.com".format(args.region_id)
    client = AcsClient(args.access_key_id, args.access_key_secret, args.region_id)

    if args.action == "GetInstance":
        print(json.dumps(get_instance(client, args.endpoint, args.instance_name)))
    elif args.action == "InsertInstance":
        print(json.dumps(insert_instance(client, args.endpoint, args.instance_name, args.cluster_type)))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

