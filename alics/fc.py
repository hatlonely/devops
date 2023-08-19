#!/usr/bin/env python3

import argparse
import json
import fc2
import sys
import re


def do(client: fc2.Client, req):
    action = re.sub(r'(?<!^)(?=[A-Z])', '_', req["Action"]).lower()
    del req["Action"]
    res = getattr(client, action)(**req)
    return {
        "headers": dict(res.headers),
        "data": res.data
    }


def main():
    parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=200), description="""example:
      python3 fc.py -i ak -s sk -e owner-id.cn-shanghai.fc.aliyuncs.com --request '{
        "Action": "CreateService",
        "serviceName": "imm-probe",
        "role": "acs:ram::owner-id:role/AliyunFCLogExecutionRole"
      }'
      python3 fc.py -i ak -s sk -e owner-id.cn-shanghai.fc.aliyuncs.com --request '{
        "Action": "GetService",
        "serviceName": "imm-probe"
      }'
      python3 fc.py -i ak -s sk -e owner-id.cn-shanghai.fc.aliyuncs.com --request '{
        "Action": "CreateFunction",
        "serviceName": "imm-probe",
        "functionName": "imm-probe",
        "runtime": "custom-container",
        "handler": "index.handler",
        "memorySize": "512",
        "customContainerConfig": {
          "image": "registry-vpc.cn-shanghai.aliyuncs.com/imm-dev/imm-probe:0.0.3"
        },
        "environmentVariables": {
          "OPS_ENV": "imm-dev-hl",
          "CFG_ACCESS_KEY_ID": "ak",
          "CFG_ACCESS_KEY_SECRET": "sk"
        }
      }'
      python3 fc.py -i ak -s sk -e owner-id.cn-shanghai.fc.aliyuncs.com --request '{
        "Action": "CreateTrigger",
        "serviceName": "imm-probe",
        "functionName": "imm-probe",
        "triggerType": "timer",
        "triggerName": "imm-probe-trigger1",
        "triggerConfig": {
          "payload": "",
          "cronExpression": "0 0/5 * * * *",
          "enable": true
        },
        "sourceArn": "1",
        "invocationRole": ""
      }'
    """)
    parser.add_argument("-i", "--access-key-id", required=True, help="access key id")
    parser.add_argument("-s", "--access-key-secret", required=True, help="access key secret")
    parser.add_argument("-r", "--region-id", help="region id")
    parser.add_argument("--owner-id", help="owner id")
    parser.add_argument("-a", "--action", help="action")
    parser.add_argument("-e", "--endpoint", help="endpoint")
    parser.add_argument("--request", type=str, help="request json body. read from file if start with @; read from stdin if none")
    args = parser.parse_args()

    if not args.endpoint:
        args.endpoint = "{}.{}.fc.aliyuncs.com".format(args.owner_id, args.region_id)

    client = fc2.Client(
        endpoint=args.endpoint,
        accessKeyID=args.access_key_id,
        accessKeySecret=args.access_key_secret,
    )

    if not args.request:
        request = json.load(sys.stdin)
    elif args.request.startswith("@"):
        request = json.load(open(args.request[1:]))
    else:
        request = json.loads(args.request)

    if args.action:
        request["Action"] = args.action

    print(json.dumps(do(client, request), indent=2))


if __name__ == '__main__':
    main()
