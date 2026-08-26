# 11.0 - Dynamic Inventory

## 11.1 - Introduction

- Commonly inventory files are stored in plaintext form.
- This generally is bad practice, but becomes tedious and unmanageable for larger inventories.
- One may wish to leverage Dynamic Inventories
  - Inventories stored in the cloud or external databases
  - Ansible will retrieve this information programmatically during the play

### Example

- Convert a static inventory file into a python script

```python
#!/usr/bin/env python <- Required as Ansible will try to exec this as a Bash script if not included

import json


def get_inventory_data():
    return {
        "databases": {
            "hosts": ["db_server"],
            "vars": {"ansible_ssh_pass": "value", "ansible_ssh_host": "IP"},
        },
        "web": {
            "hosts": ["wev_server"],
            "vars": {"ansible_ssh_pass": "value", "ansible_ssh_host": "IP"},
        },
    }


if __name__ == "__main__":
    inventory_data = get_inventory_data()
    print(json.dumps(inventory_data))
```

- One would then swap refer to this by `-i [inventory.py](http://inventory.py)` in the `ansible-playbook` command
- When running the script, one should be able to pass `--list` or `--host <hostname>` to list the entire inventory details or get the details of a particular host.
- This could be supported by using a function:

```python
def read_cli_args():
    global args
    parser = argpars.ArgumentParser()
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--host", action="store")
    args = parser.parse_args()
```

- The final conditional could then be edited for example:

```python
if __name__ == "__main__":
  global args
  read_cli_args()
  inventory_data = get_inventory_data()
  if args and args.list:
    print(json.dumps(inventory_data))
  elif args.host:
    print(json.dumps({'_meta': {'hostvars': {}}})
```

- Many dynamic scripts are available via the Ansible Github predeveloped for providers such as:
  - AWS
  - Azure
  - VMware
  - Docker
