#!/usr/bin/env python3
# Simple pusher to update TXT entries in Route53 DNS, making public keys available.

import sys
import os

import argparse
import boto3
import botocore

class route53(object):
    def __init__(self,hosted_zone=''):
        self.r53         = boto3.client('route53')
        self.hosted_zone = hosted_zone
        self.records     = []


    def update(self, dryrun=False):
        r = self.r53.change_resource_record_sets(
            HostedZoneId=self.hosted_zone,
            ChangeBatch={
                'Comment': "latest",
                'Changes': self.records
                }

            )
        return r


    def create_record(self, name, key):
        d = {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': name,
                    'Type': 'TXT',
                    'TTL': 300,
                    'ResourceRecords': [
                        {
                            'Value': '"' + key + '"'
                        }
                    ]
                }
            }
        self.records.append(d)

    def get_records(self):
        return self.records


def get_key(key):
    with open(key) as f:
        k = f.readline()
        k = k.strip()
    return k


def main():

    parser = argparse.ArgumentParser(
        description=''' A simple script to push a key to a domain TXT record in Route53.'''
        )
    parser.add_argument('-k', '--key', default=os.environ.get('HOME') + '/.ssh/id_rsa.pub', type=str, help="Path to public key")
    parser.add_argument('-n', '--name', default='ssh.keys.caustic.org', type=str, help='FQDN for the key')
    parser.add_argument('-z', '--zone', default='Z[...]', type=str, help='HostedZoneID')

    args = parser.parse_args()

    r53 = route53(hosted_zone=args.zone)

    k = get_key(args.key)

    r53.create_record(args.name, k)
    results = r53.update()
    print(results)


if __name__ == '__main__':
    main()