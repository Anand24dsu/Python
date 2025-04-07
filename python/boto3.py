from ansible.module_utils.basic import AnsibleModule
import boto3

def main():
    module = AnsibleModule(argument_spec={})
    client = boto3.client('ec2')
    instances = client.describe_instances()
    module.exit_json(changed=False, instances=instances)

if __name__ == '__main__':
    main()


