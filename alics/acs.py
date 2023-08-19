#!/usr/bin/env python3

import argparse
import json
import sys

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth.credentials import StsTokenCredential
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.request import CommonRequest

product_info = {
    "ots": "2016-06-20",
    "imm": "2017-09-06",
    "ram": "2015-05-01",
    "slb": "2014-05-15",
    "ack": "2015-12-15",
    "rds": "2014-08-15",
    "redis": "2015-01-01",
    "ecs": "2014-05-26",
    "vpc": "2016-04-28",
    "kms": "2016-01-20",
    "sts": "2015-04-01",
    "immv2": "2020-09-30",
    "cdn": "2018-05-10",
    "cr": "2018-12-01",
    "ons": "2019-02-14",
    "ons": "2019-02-14"
}


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def do(client: AcsClient, endpoint, disable_https, method, product_id, action, request):
    req = CommonRequest()
    req.set_accept_format("json")
    req.set_method(method)
    if disable_https:
        req.set_protocol_type("http")
    else:
        req.set_protocol_type("https")
    if "Endpoint" in request:
        req.set_domain(req["Endpoint"])
    elif endpoint:
        req.set_domain(endpoint)
    if product_id:
        req.set_version(product_info[product_id])
    elif "Version" in request:
        req.set_version(request["Version"])
    if action:
        req.set_action_name(action)
    elif "Action" in request:
        req.set_action_name(request["Action"])
    for key in request:
        req.add_query_param(key, request[key])
    res = client.do_action_with_exception(req)
    return json.loads(str(res, encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=200), description="""example:
  python3 acs.py -i ak -s sk -e https://slb-share.cn-zhangjiakou.aliyuncs.com --request '{
    "Action": "InnerQueryLoadbalancerByInstanceId",
    "RegionId": "cn-zhangjiakou",
    "LoadBalancerId": "lb-8vb3wrwhxvr00i27rxjh4",
    "Version": "2014-05-15"
  }' | jq -r .Data | jq .
  python3 acs.py -i ak -s sk -r cn-shanghai -e ots.cn-shanghai.aliyuncs.com -p ots -a GetInstance --request  '{
    "InstanceName": "imm-dev-hl"
  }' | jq .
  python3 acs.py -i ak -s sk -r cn-shanghai -e ots.cn-shanghai.aliyuncs.com -p ots -a InsertInstance --method POST --request  '{
    "InstanceName": "imm-dev-hl-test",
    "ClusterType": "HYBRID"
  }' | jq .
  python3 acs.py -i ak -s sk -r cn-shanghai -e imm.cn-shanghai.aliyuncs.com -p imm -a GetProject --request '{
    "Project": "hl-shanghai-doc-project"
  }' | jq .
  python3 acs.py -i ak -s sk -r cn-shanghai -e imm.cn-shanghai.aliyuncs.com -p imm --request '{
    "Action": "GetWebofficeURL",
    "Project": "hl-shanghai-doc-project",
    "FileID": "1234",
    "User": "{\"ID\": \"user1\",\"Name\": \"wps-user1\",\"Avatar\": \"http://xxx.cn/?id=user1\"}",
    "Permission": "{\"Rename\": true, \"Readonly\": false, \"History\": true}",
    "File": "[{\"Modifier\": {\"Avatar\": \"http://xxx.cn/?id=user1\", \"ID\": \"user1\", \"Name\": \"wps-user1\"}, \"Name\": \"checklist.docx\", \"Creator\": {\"Avatar\": \"http://xxx.cn/?id=user1\", \"ID\": \"user1\", \"Name\": \"wps-user1\"}, \"SrcUri\": \"oss://imm-test-hl-shanghai/checklist.docx\", \"Version\": 3, \"TgtUri\": \"oss://imm-test-hl-shanghai/checklist.docx\"}]",
    "NotifyEndpoint": "",
    "NotifyTopicName": "",
    "Watermark": "{\"Rotate\": -0.7853982, \"Vertical\": 100, \"Value\": \"hatlonely\", \"FillStyle\": \"rgba(192, 192, 192, 0.6)\", \"Horizontal\": 50, \"Font\": \"bold 20px Serif\", \"Type\": 1}",
    "Hidecmb": "false"
  }' | jq .
  python3 acs.py -i ak -s sk -e imm.cn-shanghai.aliyuncs.com -p imm --request @1.json | jq .
  cat 1.json | python3 acs.py -i ak -s sk -e imm.cn-shanghai.aliyuncs.com -p imm | jq .
  python3 acs.py -i ak -s sk -r cn-shanghai -e kms.cn-shanghai.aliyuncs.com -p kms -a ListKeys --request '{}' | jq .
  python3 acs.py -i ak -s sk -r cn-shanghai -e kms.cn-shanghai.aliyuncs.com -p kms -a GenerateDataKey --request '{
    "KeyId": "b9154493-2e02-46a4-a922-ebd1aa5c0370"
  }' | jq .
  python3 acs.py -i ak -s sk -e ram.aliyuncs.com -p ram -a CreateRole --request '{
    "RoleName": "AliyunIMMDefaultRole7",
    "AssumeRolePolicyDocument": "{\"Statement\":[{\"Action\":\"sts:AssumeRole\",\"Effect\":\"Allow\",\"Principal\":{\"RAM\":[\"acs:ram::1335926999564873:root\"],\"Service\":[\"imm.aliyuncs.com\"]}}],\"Version\":\"1\"}",
    "Description": "create by acs.py"
  }' | jq .
  python3 acs.py -i ak -s sk -e ram.aliyuncs.com -p ram -a CreatePolicy --request '{
    "PolicyName": "AliyunIMMDefaultRolePolicy7",
    "PolicyDocument": "{\"Version\":\"1\",\"Statement\":[{\"Action\":[\"oss:Get*\",\"oss:List*\",\"oss:PutBucketLifecycle\",\"oss:PutBucketNotification\",\"oss:DeleteBucketNotification\",\"oss:PutBucketAcl\",\"oss:PutObjectAcl\",\"oss:CopyObject\",\"oss:AppendObject\",\"oss:PutSymlink\",\"oss:PutObject\"],\"Resource\":\"*\",\"Effect\":\"Allow\"},{\"Action\":[\"ots:BatchGet*\",\"ots:Describe*\",\"ots:Get*\",\"ots:List*\",\"ots:Create*\",\"ots:Update*\",\"ots:BatchWrite*\",\"ots:Delete*\",\"ots:Put*\",\"ots:Update*\"],\"Resource\":\"*\",\"Effect\":\"Allow\"},{\"Action\":[\"mns:PublishMessage\",\"mns:SendMessage\"],\"Resource\":\"*\",\"Effect\":\"Allow\"},{\"Action\":[\"nas:DescriptFileSystems\",\"nas:DescriptAccessGroup\",\"nas:DescriptAccessRule\",\"nas:CreateAccessRule\",\"nas:DeleteAccessRule\"],\"Resource\":\"*\",\"Effect\":\"Allow\"},{\"Action\":[\"kms:Decrypt\"],\"Resource\":\"*\",\"Effect\":\"Allow\"}]}",
    "Description": "create by acs.py"
  }' | jq .
  python3 acs.py -i ak -s sk -e ram.aliyuncs.com -p ram -a AttachPolicyToRole --request '{
    "RoleName": "AliyunIMMDefaultRole7",
    "PolicyName": "AliyunIMMDefaultRolePolicy6",
    "PolicyType": "Custom"
  }' | jq .
  python3 acs.py -i ak -s sk -e ram.aliyuncs.com -p ram -a ListUsers --request '{
    "RoleName": "AliyunIMMDefaultRole7",
    "PolicyName": "AliyunIMMDefaultRolePolicy6",
    "PolicyType": "Custom"
  }' | jq .
  python3 acs.py -i ak -s sk -r cn-shanghai -e sts.cn-shanghai.aliyuncs.com -p sts -a AssumeRole --request '{
    "RoleArn": "acs:ram::1023210024677934:role/imm-test-hl-role",
    "RoleSessionName": "test",
    "DurationSeconds": 3600
  }' | jq .
  # https://yuque.antfin-inc.com/vpc_yaochi/keo6yr/nmwl2f
  python3 acs.py -i ak -s sk -r cn-shanghai -p slb --request '{
    "Action": "CreateLoadBalancerForCloudService",
    "RegionId": "cn-shanghai",
    "LoadBalancerName": "weboffice-anytunnel",
    "LoadBalancerSpec": "slb.s1.small"
    "CloudInstanceType": "imm",
    "CloudInstanceUid": "1335926999564873",
    "TunnelType": "anyTunnel",
  }'
  python3 acs.py -i ak -s sk -r cn-shanghai -p vpc --endpoint vpc.aliyuncs.com --request '{
    "Action": "DescribeVpcs",
    "RegionId": "cn-shanghai"
  }'
  # https://yuque.antfin-inc.com/vpc_yaochi/keo6yr/zvpg3c
  python3 acs.py -i ak -s sk -r cn-shanghai -p vpc --endpoint vpc.aliyuncs.com --request '{
    "Action": "ModifyBypassToaAttribute",
    "RegionId": "cn-shanghai",
    "InstanceType": "EcsInstance",
    "InstanceId": "i-uf65fi9tsrxjdb11ru0w",
    "BypassToa": 1
  }'
  # https://yuque.antfin-inc.com/vpc_yaochi/keo6yr/vphad6
  python3 acs.py -i ak -s sk -r cn-shanghai -p slb --request '{
    "Action": "CreateVServerGroup",
    "LoadBalancerId": "lb-uf6dt91rq5bdj7vhw5d3k",
    "RegionId": "cn-shanghai",
    "VServerGroupName": "weboffice-imm-regression-anytunnel",
    "BackendServers": [{
      "ServerId": "i-uf65fi9tsrxjdb11ru0w",
      "Weight": "100",
      "Type": "ecs_fnat",
      "Port": "60080"
    }]
  }'
  python3 acs.py -i ak -s sk -r cn-shanghai -p slb --request '{
    "Action": "DeleteVServerGroup",
    "LoadBalancerId": "lb-uf6dt91rq5bdj7vhw5d3k",
    "RegionId": "cn-shanghai",
    "VServerGroupId": "rsp-uf62lns6hpqik"
  }'
  python3 acs.py -i ak -s sk -r cn-shanghai -p slb --request '{
    "Action": "CreateLoadBalancerTCPListener",
    "LoadBalancerId": "lb-uf6dt91rq5bdj7vhw5d3k",
    "RegionId": "cn-shanghai",
    "Bandwidth": -1,
    "ListenerPort": 80,
    "BackendServerPort": 60080,
    "VServerGroupId": "rsp-uf62lns6hpqik"
  }'
  python3 acs.py -i ak -s sk -r cn-shanghai -p slb --request '{
    "Action": "StartLoadBalancerListener",
    "LoadBalancerId": "lb-uf6dt91rq5bdj7vhw5d3k",
    "RegionId": "cn-shanghai",
    "ListenerPort": 80
  }'
  python3 acs.py -i ak -s sk -r cn-shanghai -p slb --request '{
    "Action": "StopLoadBalancerListener",
    "LoadBalancerId": "lb-uf6dt91rq5bdj7vhw5d3k",
    "RegionId": "cn-shanghai",
    "ListenerPort": 80
  }'
  python3 acs.py -i ak -s sk -r cn-shanghai -p slb --request '{
    "Action": "DeleteLoadBalancerListener",
    "LoadBalancerId": "lb-uf6dt91rq5bdj7vhw5d3k",
    "RegionId": "cn-shanghai",
    "ListenerPort": 80
  }'

  # 创建 cdn <https://help.aliyun.com/document_detail/91176.htm>
  python3 acs.py -i ak -s sk -p cdn --endpoint cdn.aliyuncs.com --request '{
    "Action": "AddCdnDomain",
    "CdnType": "web",
    "DomainName": "regression.office-static.dev.imm.aliyuncs.com",
    "Sources": "[{\"type\": \"oss\", \"content\": \"office-static-imm-dev-cn-shanghai.oss-cn-shanghai.aliyuncs.com\"}]",
    "Scope": "domestic"
  }'
  # 上传 cdn 证书 <https://help.aliyun.com/document_detail/91189.html>
  python3 acs.py -i ak -s sk -p cdn --endpoint cdn.aliyuncs.com --request "{
    \"Action\": \"SetDomainServerCertificate\",
    \"DomainName\": \"regression.office-static.dev.imm.aliyuncs.com\",
    \"ServerCertificateStatus\": \"on\",
    \"CertName\": \"imm-20230109\",
    \"CertType\": \"upload\",
    \"ServerCertificate\": $(cat tls.crt | jq -aRs),
    \"PrivateKey\": $(cat tls.key | jq -aRs),
    \"ForceSet\": 0
  }"
  # 获取 cdn 域名证书信息 <https://help.aliyun.com/document_detail/91182.html>
  python3 acs.py -i ak -s sk -p cdn --endpoint cdn.aliyuncs.com --request '{
    "Action": "DescribeDomainCertificateInfo",
    "DomainName": "regression.office-static.dev.imm.aliyuncs.com"
  }'
  # 查询 cdn 域名信息 <https://help.aliyun.com/document_detail/91187.htm>
  python3 acs.py -i ak -s sk -p cdn --endpoint cdn.aliyuncs.com --request '{
    "Action": "DescribeCdnDomainDetail",
    "DomainName": "regression.office-static.dev.imm.aliyuncs.com"
  }'
  # 获取加速域名的配置信息 <https://help.aliyun.com/document_detail/90924.html>
  python3 acs.py -i ak -s sk -p cdn --endpoint cdn.aliyuncs.com --request '{
    "Action": "DescribeCdnDomainConfigs",
    "DomainName": "regression.office-static.dev.imm.aliyuncs.com"
  }'
  # 批量配置域名-配置私有 oss bucket 回源 <https://help.aliyun.com/document_detail/90915.htm> <https://help.aliyun.com/document_detail/388460.html>
  python3 acs.py -i ak -s sk -p cdn --endpoint cdn.aliyuncs.com --request '{
    "Action": "BatchSetCdnDomainConfig",
    "DomainNames": "regression.office-static.dev.imm.aliyuncs.com",
    "Functions": "[{\"functionName\": \"l2_oss_key\", \"functionArgs\": [{\"ArgName\": \"private_oss_auth\", \"ArgValue\": \"on\"}]}]"
  }'
  # rocketmq 4.0 <https://help.aliyun.com/document_detail/445290.html>
  python3 alics/acs.py -i ak -s sk -p ons -e "ons.cn-beijing.aliyuncs.com" -a OnsInstanceInServiceList --request '{}'
  python3 alics/acs.py -i ak -s sk -p ons -e "ons.cn-beijing.aliyuncs.com" -a OnsInstanceCreate --request '{
    "InstanceName": "imm-test-hl"
  }'
""")

    parser.add_argument("-i", "--access-key-id", required=True, help="access key id")
    parser.add_argument("-s", "--access-key-secret", required=True, help="access key secret")
    parser.add_argument("-t", "--security-token", help="security token")
    parser.add_argument("-r", "--region-id", help="region id")
    parser.add_argument("-a", "--action", help="action")
    parser.add_argument("-p", "--product-id", help="product id")
    parser.add_argument("-e", "--endpoint", help="endpoint")
    parser.add_argument("--request", type=str, help="request json body. read from file if start with @; read from stdin if none")
    parser.add_argument("--method", choices=["GET", "POST"], default="GET", help="method")
    parser.add_argument("--disable-https", nargs="?", const=True, default=False, type=str2bool, help="disable https")
    parser.add_argument("--disable-verify", nargs="?", const=True, default=False, type=str2bool, help="disable https verify")
    args = parser.parse_args()
    if args.security_token:
        credential = StsTokenCredential(args.access_key_id, args.access_key_secret, args.security_token)
    else:
        credential = AccessKeyCredential(args.access_key_id, args.access_key_secret)

    client = AcsClient(region_id=args.region_id, credential=credential)
    if args.disable_verify:
        client = AcsClient(region_id=args.region_id, credential=credential, verify=False)
    if not args.endpoint:
        args.endpoint = "{}.{}.aliyuncs.com".format(args.product_id, args.region_id)
    if not args.request:
        request = json.load(sys.stdin)
    elif args.request.startswith("@"):
        request = json.load(open(args.request[1:]))
    else:
        request = json.loads(args.request)

    print(json.dumps(do(client, args.endpoint, args.disable_https, args.method, args.product_id, args.action, request)))


if __name__ == '__main__':
    main()
