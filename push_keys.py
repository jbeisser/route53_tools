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
            DryRun=dryrun,
            HostedZoneId=self.host_zone,
            ChangeBatch={
                'Comment': "latest",
                'Changes': self.records
                }

            )

    def create_record(self, name, key):
        d = {
                'Action': 'UPSERT',
                'ResourceRecordSet': name,
                'Type': 'TXT',
                'TTL': 300,
                'ResourceRecords': [
                    {
                        name: key
                    }
                ]
            }

        self.records.append(d)


def get_key(key):
    with open(key) as f:
       k = f.readlines()
    return k

def main():
    r53 = route53()

    parser = argparse.ArgumentParser(
        description=''' A simple script to push a key to a domain TXT record in Route53.'''
        )
    parser.add_argument('-k','--key', default='sshkey', type=str, help="Path to public key")
    parser.add_argument('-n', '--name', default='~/.ssh/id_rsa.pub', type=str, help='Record name for the key')

    args = parser.parse_args()

    k = get_key(args.key)


if __name__ == '__main__':
    main()