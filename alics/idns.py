#!/usr/bin/env python3


import argparse
import datetime
import json
import requests


# 修改公网域名解析 https://yuque.antfin-inc.com/adms/te885n/sc6z3q
DNS_INTERNET_ENDPOINT = "http://super-dns-api.vip.tbsite.net:9999"


# https://yuque.antfin-inc.com/adms/te885n/dreyw6
def add_rr(app_id, key, name, line, type_, value):
    body = {
        "appId": app_id,
        "appKey": key,
        "group": "200",
        "line": line,
        "name": name,
        "type": type_,
        "value": value,
        "ttl": "60",
        "transactionId": str(datetime.datetime.now().timestamp()),
    }

    print(json.dumps(body, indent=2))

    res = requests.post(
        '{}/rr/addRr'.format(DNS_INTERNET_ENDPOINT),
        headers={
            "Content-Type": "application/json"
        },
        json=body
    )
    return {
        "Status": res.status_code,
        "Headers": dict(res.headers),
        "Body": res.json(),
    }


def del_rr(app_id, key, name, line, type_, value):
    body = {
        "appId": app_id,
        "appKey": key,
        "group": "200",
        "line": line,
        "name": name,
        "type": type_,
        "value": value,
        "ttl": "60",
    }

    print(json.dumps(body, indent=2))

    res = requests.post(
        '{}/rr/delRr'.format(DNS_INTERNET_ENDPOINT),
        headers={
            "Content-Type": "application/json"
        },
        json=body
    )
    return {
        "Status": res.status_code,
        "Headers": dict(res.headers),
        "Body": res.json(),
    }


def main():
    parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=200), description="""example:
  python3 idns.py -i aliyun-imm -k key -a AddRR --name test.svc.aliyuncs.com --line ldns --type A --value 139.196.123.123
  python3 idns.py -i aliyun-imm -k key -a DelRR --name test.svc.aliyuncs.com --line ldns --type A --value 139.196.123.123
  python3 idns.py -i aliyun-imm -k key -a AddRR --name test.svc.aliyuncs.com --line ldns --type CNAME --value test.svc.aliyuncs.com.w.alikunlun.com
  python3 idns.py -i aliyun-imm -k key -a DelRR --name test.svc.aliyuncs.com --line ldns --type CNAME --value test.svc.aliyuncs.com.w.alikunlun.com
""")
    parser.add_argument("-i", "--app-id", required=True, help="app id")
    parser.add_argument("-k", "--key", required=True, help="key")
    parser.add_argument("-a", "--action", help="action")
    parser.add_argument("--name", help="name @see: <https://yuque.antfin-inc.com/adms/te885n/gf4ia2>")
    parser.add_argument("--line", default="ldns", help="name @see: <https://yuque.antfin-inc.com/adms/te885n/il7xrd>")
    parser.add_argument("--type", help="dns type @see: <https://yuque.antfin-inc.com/adms/te885n/ik6en7>")
    parser.add_argument("--value", help="value @see: <https://yuque.antfin-inc.com/adms/te885n/ik6en7>")
    args = parser.parse_args()

    if args.action == "AddRR":
        print(json.dumps(add_rr(args.app_id, args.key, args.name, args.line, args.type, args.value), indent=2))
    elif args.action == "DelRR":
        print(json.dumps(del_rr(args.app_id, args.key, args.name, args.line, args.type, args.value), indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
