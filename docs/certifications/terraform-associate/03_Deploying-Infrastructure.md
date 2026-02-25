# 1.0 - Deploying Infrastructure

## 1.1 - EC2 Instance Creation

- Terraform supports a significant number of providers, this becomes an important consideration for organisations when working with terraform.
- In the case of AWS, can make use of any of the following:
  - Static credentials
  - Environment variableS
  - Shared credentials files
  - EC2 Roles
- For this demo, using static credentials:
  - AWS Console -> IAM -> Create User -> Allow programmatic access -> create user -> access and secret keys shown
- Add following to first_ec2.tf file:

```go

provider "aws" {
    region = "eu-west-2"
}

resource "aws_instance" "myec2" {
    ami = "ami-<ami id>"
    instance_type = "t2.micro
}
```

- The above code first configures the provider, aws, providing the region
location for the vm deployment, along with the access and secret keys

- The code then looks to create an aws resource, in this case an ec2 instance of
a particular ami and instance type:
  - Instance type specifies parameters such as memory and cpu
- Note: ami and instance_type are the only two required parameters for a aws_instance resource, there are optionals available
- To initialize: `terraform init`
  - Terraform initialises the current directory, downloading additional plugins required; which vary for each provider.
- To validate the syntax used in config files: `terraform validate`
- To format: `terraform fmt`
- To plan the execution of the configuration: `terraform plan`
- To apply: `terraform apply`
- To destroy: `terraform destroy`

## 1.2 - Providers and Resources

### Introduction

- Terraform is capable of supporting multiple providers
- The provider details the infrastructure is to be launched on must be specified in the configuration files
- In some/most cases, authentication tokens will also be required - these should never be included in source code, referenced instead via environment variables or another appropriate method.
- When the command `terraform init` is ran, terraform downloads plugins associated with the provider to the `.terraform` directory in the project root.
- Each provider has different resources that can be created, with each resource type specific to the particular provider e.g. for AWS:
  - `aws_instance` - Virtual Machine/Instance
  - `aws_alp` - Application load balancer
  - `iam_user` - Identification Application Managment User
- The above resources couldn't be provisioned by e.g. Azure with this syntax, would have to use the provided syntax for Azure
- Consider the following example:

```go

provider "digitalocean" {
    token = "<TOKEN>"
}

resource "digitalocean_droplet" "droplet" {
    image = "image id"
    name = "web-1"
    region = "nyc1"
    size = "<size-identifier>"
}

```

- In terms of syntax, the general format is followed, defining a provider and configuring it, followed by a resource which is configured as desired.
  - Since this is for a different provider (DigitalOcean), the syntax for parameters such as the image or region names
  - In terms of authentication, only one token is required for provider configuration unlike AWS.

### Provider Maintainers

- There are 3 main types of provider tiers in Terraform:
  - **Official** - Owned and maintained by HashiCorp
  - **Partner** - Owned and maintained by a direct partner of HashiCorp
  - **Community** - Owned and Maintained by Individual Contributors

### Required Providers

- For providers not directly maintained by HashiCorp, a `required_providers` block is required, taking DigitalOcean as an example, the configuration before would become:

```go
terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean
    }
  }
}

provider "digitalocean" {
    token = "<TOKEN>"
}
```

- Details on how to reference each provider is typically provided in the provider's documentation.

## 1.3 - Destroying Infrastructure

- Obviously we don't want to keep infrastructure running forever and racking up charges
- To bring down infrastructure, can run the command `terraform destroy`
- If you wish to destroy a specific target, add the -target flag in the format:
    `Terraform destroy -target <resource_type>.<resource_name>`
    e.g. `terraform destroy -target aws_instance.ec2`

- Alternatively could comment out the resource you don't wish to be applied or destroyed, though this is not recommended in general practice

**Note:** to automatically destroy: `terraform destroy --auto-approve`

## 1.4 - Terraform State Files

- Terraform keeps track of the infrastructure being created in a state file
- Allows terraform to map real-world resources to existing configurations
- Includes resource details including instance ID, IP addresses, tags,  etc.
- Therefore, when `terraform destroy` is ran against a a particular target, all the details relating to that resource will be removed from the state file
- State file is always named `terraform.tfstate`
- If changes made outside the terraform configuration files, when terraform apply is ran again, the tfstate file will be checked to make sure that the real world configuration is set up correctly, if not it will attempt to apply the appropriate changes to return/update to the desired state.
  - This may not work OR it may require recreation of resources (if the affected resource(s) have any dependencies)
- To destroy a specific resource: `terraform destroy -target <resource_type>.<local_name>`

## 1.5 - Desired and Current States

### 1.5.1 - Desired State

- The state defined within a configuration resource block e.g. in an `aws_instance` resource, if `instance_type = t2.micro`, that is reflective of the desired state - you desire an aws_instance of size `t2.micro` to be created.

### 1.5.2 - Current State

- State defined within the `terraform.tfstate` file.
- Holds configuration data regarding the resources created by Terraform.
- Used as the comparison point to determine any changes that need to be applied during `terraform apply` command execution.

### 1.5.3 - Updating Current State

- The current state can be updated by running `terraform refresh`
- The current state is always refreshed during a `plan` or `apply` command execution
- Terraform will always apply changes to ensure that the current state matches that of the desired state.

## 1.6 - Challenges of Current State and Computed Values

- If not running Terraform in a system with a readily-available editor, one can run `terraform show` to view the state file contents.
- **Note:** Suppose a change is made outside the desired state that isn't defined as code e.g adding a security group, Terraform will not act to update the current state since it's not in the desired state.
  - One would have to use `terraform import` to achieve this.

## 1.7 - Provider Versioning

- Terraform providers exist to provide a link between terraform and the service provider, allowing terraform to provision infrastructure to the appropriate provider.
- Plugins for the providers are released separately from Terraform and are updated in their own time.
- In terraform init, the latest provider plugin will automatically be downloaded if the version isn't specified.
  - In production, it's recommended to specify the version that you know the code works for e.g. AWS version 2.7.
- To specify the provider version, in the provider block of the configuration file, add `version = "version number"` as an exact number or express it as a criteria:

| Version Argument | Description                                                    |
| ---------------- | -------------------------------------------------------------- |
| >=x.y            | Greater than or equal to version value                         |
| <=x.y            | Less than or equal to version value                            |
| ~>x.y            | Any version in the subrange of value x i.e. any version of 2.y |
| >=a.b,<=c.d      | Any version between a.b and c.d                                |

- **Note:** Certain provider plugins aren't compatible with particular versions of Terraform - it will specify and suggest alternate versions if this occurs.
- If wanting to make an upgrade / change: `terraform init -upgrade`

## 1.8 - Provider Versioning

- Providers are split into 2 categories:
  - Hashicorp-Distributed: Automatically downloaded during Terraform init
  - Third-party

- The need for third party providers arises whenever an official provider doesn't support a particular functionality, or when organizations have developed their own platform to run terraform on.

- Hashicorp distributed providers are listed under "Major Cloud Providers" under the HashiCorp website; third party providers are under the "Community" tab.

- When attempting to initialise with a third party provider, it's likely that an error will occur.
- As mentioned, terraform init cannot automatically install the plugins for third party providers, they must be installed manually.
- The installation can be achieved by placing the plugins into the system's user plugins directory (OS-dependent).

| OS                      | Directory                       |
| ----------------------- | ------------------------------- |
| Windows                 | `%APPDATA%\terraform.d\plugins` |
| Other (e.g. Linux, MAC) | `~/.terraform.d/plugins`        |
