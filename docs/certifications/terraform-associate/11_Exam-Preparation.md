# 8.0 - Exam Preparation

## 8.1 - Important Pointers

### 8.1.1 - Overview

| Exam Property             | Description      |
|---------------------------|------------------|
| Type                      | Multiple Choice  |
| Format                    | Online Proctored |
| Duration                  | 1 Hour           |
| Total Number of Questions | 57               |
| Price                     | $70.50           |
| Language                  | English          |
| Expiration Time           | 2 Years          |

### 8.1.2 - Question Types

- True/False: Based on statement provided.
- Multiple-Choice: Select correct answer(s) from options.
- Text-Match: Given a text box or code extract, what should be added?

### 8.1.3 - Example Questions

<details>
<summary>What is the Name of the file that stores state information?</summary>
<br>
terraform.tfstate
</details>

<details>
<summary>When referencing a file, for terraform 0.11, it would follow a format similar to ${file("path/to/file")}, how does this translate to terraform v0.12?</summary>
<br>
file("path/to/file")
</details>

<details>
<summary>What does the command `terraform init` do?</summary>
<br>
This would likely be a multiple-choice question, choose all applicable.
</details>

### 8.1.4 - Important Pointers

#### Providers

- Responsivle for understandign API interactions adn exposing resources
- Most providers correspond to one cloud or on-prem platform, offering resource types corresponding to each of the platform's features.
- Provider(s) used are specified by the `provider {}` block.
- One can automatically upgrade to the latest version of the designated provider by using `terraform init -upgrade`

#### Provider Architecture

- Providers act as the link between cloud providers and Terraform Configurations.
- They handle the underlying API interactions and authentication between host and provider.
- Multiple instances of the same provider can be used via the `alias` property.

#### Terraform Init

- Run `terraform init` to initialize the working directory where the Terraform config files are stored.
- Configuration is searched for module blocks and the required source code is retrieved from the specified sources
- Any providers specified have to be initialised via Terraform before use.
- No additional files are created with `terraform init`.

#### Terraform Plan

- `terraform plan` creates an execution of the infrastructure described in the configuration files.
- Unless told otherwise, will perform a refresh of the terraform state to determine the exact changes required to meet the desired state.
- Typically used to check the changes match expectations without applying changes.

#### Terraform Apply

- `terraform apply` applies the changes specified to reach the desired state of the configuration
- Changes detailed in `terraform.tfstate` file

#### Terraform Refresh

- Used to refresh the state file of the configuration to account for any changes made not via Terraform
- Only updates the state file, any configuration files are unchanged
- `terraform refresh`

#### Terraform Destroy

- `terraform destroy` will tear down all or specific parts of the infrastructure defined in the configuration.
- Not the only way of destruction, one could simply remove the configuration of the resource(s)

#### Terraform Format

- `terraform fmt` rewrites terraform configuration files in a canonical format and style.
- Recommended for use in projects to maintain readability

#### Terraform Validate

- `terraform validate` validates the configuration files in a directory
- Checks whether a configuration is syntactically valid or not.
- Useful for general verification of reusable modules, as well as attribute names and value types.
- Generally runs automatically as a test step or post-save check for a reusable module in a CI system prior to execution.
- Cannot be run until `terraform init` has been executed.

#### Terraform Provisioners

- Used to specify model-specific actions on a local or remote machine to carry out configuration / setup tasks.
- Should only be used as a last resort, typically one would use Packer in conjunction with Terraform.
- Provisioners are added within resource blocks.
- For remote-exec, inline commands and connection method must be specified in a similar manner to the following:

```go
provisioner "remote-exec" {
    inline = [
        "sudo amazon-linux-extras install -y nginx1.12", #install nginx
        "sudo systemctl start nginx" ## start nginx
    ]
    connection {
        #connection method
        type = "ssh"
        user = "ec2-user"
        #private key for authentication
        private_key = file("./remote-exec-keypair.pem")
        host = self.public_ip
    }
}
```

- For local-exec, similar to the above, but without the `connection {}` block.

#### Debugging Terraform

- Terraform has logs that can be enabled by setting the `TF_LOG` environment variable to one of the following, depending on desired verbosity:
  - TRACE
  - DEBUG
  - INFO
  - WARN
  - ERROR
- To persist log output, set `TF_LOG_PATH="/path/to/file"`
- Logs should be saved as a `.log` format.

#### Terraform Import

- `terraform import` allows one to import existing infrastructure and bring it under Terraform's management
- Current implementation can only import resources into the state, it doesn't generate the configuration, which must be written manually.
- Prior to command execution, write a resource configuration block for the resource, which the live resource will be mapped to.
- Usage Example: `terraform import aws_instance.myec2 <instance ID>`

#### Local Values

- Assigns a name to an expression, allowing easy reuse within a module without having to manually type it each time
- Locals can refer to other locals, but as standard practice, reference cycles aren't allowed i.e. a local cannot refer to itself or a variable that refers backt to it.
- It's advised to group together logically-related local values to a single block, particularly if the values are dependent upon one another.

#### Data Types

- There are 4 maind ata types in Terraform:
  - **String** - Unicode characters representing text
  - **List** - Sequential list of values identified by their position, first value being position "0"
  - **Map** - A group of values identified by named labels/keys e.g. age=52
  - **Number** - Numerical values

#### Terraform Modules

- Resources can be centralised and called out from TF modules when required.

##### Terraform Modules - Root and Child

- Each terraform configuration has at least one module, the root module, which consists of the resources in `.tf` files in the main directory.
- Modules can call other modules, which allos the inclusion of the child module's resources into the configuration in a concise manner.
- A module that includes a module block in the following manner is a child module.

```go
module "ec2" {
    source = "../../modules/ec2"
}
```

##### Modules - Accessing Output Values

- Resources defined in a module are encapsulated, the calling module cannot access their attributes directly
- The child module can declare output values to selectively export certain values to be accessed by the calling module in a similar manner to

```go
output "mys3bucket" {
    value = aws_s3_bucket.mys3.bucket_domain_name
}
```

#### Suppressing Values in CLI Output

- An output can be marked as sensitive information using the `sensitive` argument in a similar manner to:

```go
output "db_password" {
    value = aws_db_instance.db_password
    Description = "The password for logging into the database"
    Sensitive = true
}
```

- Setting an output value in the root module as sensitive prevents Terraform from showing its value when outputs are generated during `terraform apply`.
- Sensitive outputs are still recorded in the state as fully accessible values, anyone who can access the state file can therefore view the sensitive information.

#### Module Versions

- It's recommended to constrain the acceptable version numbers for each external module to avoid unexpected changes.
- Version constraints are supported for modules installed from a module registry e.g. Terraform Registry in a similar manner to the following:

```go
module "ec2_cluster" {
    source = "terraform-aws-modules/ec2-instance/aws"
    version = "~> 2.0"
    name = "my-cluster"
    instance_count = 1
    ami = "ami-0a13d44dccf1f5cf6"
    instance_type = "t2.micro"
    subnet_id = "subnet-5fbf1013"
    tags = {
        Terraform = "true"
        Environment = "dev"
    }
}
```

#### Terraform Registry

- A registry directly integrated into Terraform, containing modules submitted by the Terraform community, including third-party providers.
- General syntax for referencing a registry module: `<NAMESPACE>/<NAME>/<PROVIDER>`

#### Private Registry for Module Sources

- To use a module from a private registry, such as those provided by Terraform cloud, use the general syntax `<HOSTNAME><NAMESPACE>/<NAME>/<PROVIDER>`
- When fetching a private registry module, a version must be specified.

#### Functions

- Terraform includes a number of built-in functions to transform and combine values.
- No user-defined functions are supported.
- Examples of built-in functions include:
  - Min
  - Max
  - Element
  - Lookup

#### Count and Count Index

- The count parameter on resources can simplify configurations and allow scaling resources by incremental values.
- In resource blolocks where the `count` value is set, an additional count object `count.index` is available in expressions to be applied to other parameters associated with the resource.
- Example:

```go
Resource 1 Configuration (Instance 1)
resource "aws_instance" "instance-1" {
    key_name = "machine_instance.${count.index}"
    ami = "ami-0a13d44dccf1f5cf6"
    instance_type = "t2.micro"
    count = 3
}
```

- Alternatively:

```go
variable "elb_names" {
    type = list
    default = [
        "dev-loadbalancer",
        "stage-loadbalanacer",
        "prod-loadbalancer"
    ]
}

resource "aws_iam_user" "lb" {
    name = var.elb_names[count.index]
    count = 3
    path = "/system/"
}
```

#### Use Case: Find the Issue

- Some exam questions require one to find an issue with a sample piece of configuration to ensure it is aligned to best practice. An example follows:

```go
terraform {
    backend "s3" {
        bucket = "mybucket"
        key = "path/to/key"
        region = "us-east-1"
        access_key = 1234
        secret_key = 1234567890
    }
}
```

- For the above, tje ossie jere os tjat `access_key` and `secret_key` are not required as `key` is already specified.

#### Terraform Lock

- If supported by the backend, Terraform will lock the state file for all operations that affect it.
- There is a force-unlock command to manually unlock the state file in the event of any issues: <br> `terraform force-unlock <lock id>`

#### Use Case: Resources Deleted Out of Terraform

- Scenario-based questions are also a possibility.
- "You have created an EC2 instance. Someone has modified it manually, what
happens when terraform plan is ran?"
- Possible scenarios here would be:
  - If the instance type is changed, the resource is terminated and to be recreated.
  - Terraform will attempt to rever the instance type to that of the desired type
  - Terraform will look to create the resource once again.

#### Resource Block

- Resource blocks describe one or more infrastructure objects, such as virtual networks, compute instances, etc.
- Each resource block declares a resource of a given type e.g. `aws_instance` along with a local identifiacation name e.g `web`.

#### Sentinel

- An embedded policy-as-code framework integrated with the Hashicorp Enterprise products.
- Use cases include:
  - Verification for tags on resources
  - Verification of encryption methods.
- In general for Terraform Enterprise, the workload follows plan -> sentinel checks -> apply

#### Sensitive Data in State File

- When managing any  sensitive data in Terraform, it's good practice to treat the state file as a whole, as sensitive data.
- Terraform Cloud always encrypts the state at rest and protects it with TLS in transit.
- Terraform Cloud is capable of tracking the identity of the user requesting the state file and logging any changes made to it.
- If using a backend like S3, encryption at rest is supported when encryption is active.

#### Dealing with Credentials in Config

- Hardcoding credentials is never good practice as it poses significant security risks.
- Credentials can be stored outside of the terraform configuration.
- Storing credentials as environment variables is generally considered as best practice as they aren't committed.
- One could also use secret managers or external tools like Hashicorp Vault.

#### Remote Backend - Terraform Cloud

- Stores Terraform state and may be used to run operations in Terraform Cloud
- When using for remote operations tasks, tasks like `terraform apply` can be executed in Terraform Cloud's runtime environment; output logs are then viewable on the local machine.

#### Miscellaneous

- Terraform doesn't require GO as a prerequisite.
- Terraform works well with Linux, Windows and MAC
- Windows Server isn't required for usage.

#### Terraform Graph

- A command used to generate a visual representation of either a configuration or execution format.
- The output format of Terraform graph is in the DOT format, which can be converted to SVG, PNG, etc for visutalization.

#### Splat Expressions

- Allows quick access to a list of all attributes
- Will output all possible values within the configuration where applicable.
- Referencing modules:

```go
resource "aws_instance" "example" {
    ami = "ami-abc123"
    instance_type = "t2.micro"

    ebs_block_device {
        device_name = "sda2"
        volume_size = 16
    }
    ebs_block_device {
        device_name = "sda3"
        volume_size = 20
    }
}
```

- The arguments on the `ebs_block_device` nested blocks can be accessed via a splat expression.
- Example usage to obtain all device name values: `aws_instance.example.ebs_block_device[*].device_name`
- The nested blocks in this particular resource type don't have any exported attributes, but if `ebs_block device` were to have a documented `id` attribute, then a list of them could be accessed via `aws_instance.example.ebs_block_device[*].id`

#### Terraform Technologies

- In any given terraform resource block, there are 4 main term types used:
  - Resource Type: Specifies what resource is being defined in the resource block
  - Local Identification name for the resource
  - Attributes e.g. `AMI`, `ACCESS_KEY`, etc.
  - Attribute values.

#### Provider Configuration

- A block for provider configuration isn't mandatory for all terraform configurations.
- When no resources are to be created, no provider needs to be specified.

#### Terraform Unlock

- If supported by the backend, terraform will lock the state file for all the operations that could write to the state file
- Not all backends have locking unctionality
- Terraform has a `force-unlock` command if unlocking failed
- Example usage: `terraform force-unlock <lock id>`

#### Miscellaneous Pointers - 01

- Primary benefits of Infrastructure as Code tools:
  - Automation
  - Versioning
  - Reusability
- There are various tools available for IaC:
  - Terraform
  - AWS CloudFormation
  - Azure Resource Formation
  - Google Cloud Deployment Manager

#### Miscellaneous Pointers - 02

- Sentinel is a proactive service
- Terraform doesn't modify the infrastructure, only the state file
- Slice function is not a function to be used with strings, unlike join and split.
- It is not necessary to include the module version when pulling code from Terraform registry.

#### Miscellaneous Pointers - 03

- Overuse of dynamic blocks can make configurations unreadable
- Terraform apply can change, destroy and provision resources, but not import configuration directly.

#### Terraform Enterprise and Cloud

- Terraform Enterprise allows several additional features not included in cloud, such as:
  - Single-Sign On (SSO)
  - Auditing
  - Private Data Center
  - Clustering
- It should also be noted that Team and Governance features are not available for free on Terraform Cloud.

#### Variables with Undefined Values

- If a variable is included with an undefined value, an error will not immediately occur.
- Terraform will ask for the user to supply a value to be associated with the undefined variable.

#### Environment Variables

- Can be used to set variables
- Environment variables must be fof the format `TF_VAR_<variable name>` e.g.
  - `export TF_VAR_region=us-west-1`
  - `export TF_VAR_alist='[1,2,3]'`

#### Structural Data Types

- A structural type allows multiple values of several distinct types to be grouped together as a single value.
- List contains multiple values of the same type while object can contain multiple values of different types:

| Structural Type | Description                                                                                                          |
|-----------------|----------------------------------------------------------------------------------------------------------------------|
| Object          | A collection of named attributes that each have their own type e.g. <br> `object({<Attribute Name> = <Type>, ... })` |
| Tuple           | `tuple ([<TYPE>, ... ])`                                                                                             |

#### Backend Configuration

- Backends are configured directly in Terraform files via the `terraform {}` block.
- Once configured, any remote backends must be initialized.
- Example Usage - S3 Backend

```go
terraform {
    backend "s3" {
        bucket = "demoremotebackend"
        key = "remotedemo.tfstate"
        region = "eu-west-2"
        access_key = "<ACCESS KEY>"
        secret_key = "<SECRET KEY>"
        #dynamodb_table = "s3-state-lock"
    }
}
```

##### Backend Configuration Types

- First-Time Configuration:
  - When Cconfiguring a backend for the first time (moving from no defined backend to an explictly configured one), Terraform will give an option to migrate the currently-existing state to the new backend.
  - Allows adoption of backends without losing data in the state file.
- Partial Configuration
  - Not every required argument needs to be specified for a backend configuration
  - It may be better to omit certain arguments to avoid storing secrets within the main configuration
  - With a partial configuration, the remaining arguments must be provided as part of the initialization process.

- Partial Configuration Example:

```go
terraform {
    backend "consul" {}
}
```

- The arguments are then supplied via the `terraform init` command i.e. <br>
`terraform init -backend-config=<parameter 1>=<value 1> -backend-config=<parameter 2>=<value 2> ...`

#### Terraform Taint

- Manually marks a Terraform-managed resource as tainted, forcing it to be destroyed and recreated on the next execution of `apply`.
- Once tainted, the next `plan` will show the resource tainted will be destroyed and recreated.

- Can be used to taint resources within a module
- Usage: `terraform taint [options] <resource type>.<resource id>`
- For multiple submodules, apply: `module.foo.module.bar.<resource_type>.<resource_id>`

#### Local Provisioner

- The local-exec provisioner invokes commands to be ran on your local machine after a resource is created.
- Defined in a similar manner to:

```go
resource "aws_instance" "myec2" {
    ami = "ami-0a13d44dccf1f5cf6"
    instance_type = "t2.micro"
    provisioner "local-exec" {
        command = "echo ${aws_instance.myec2.private_ip} >> privateips.txt"
    }
}
```

#### Remote-Exec Provisioner

- Invokes commands on a remote resource after it's created.
- Supports multiple connection types including SSH and WinRM
- Example Usage:

```go
resource "resource type" "local ID" {
    .....
    provisioner "remote-exec" {
        inline = [
            "sudo amazon-linux-extras install -y nginx1.12", #install nginx
            "sudo systemctl start nginx" ## start nginx
        ]
        connection {
            #connection method
            type = "ssh"
            user = "ec2-user"
            #private key for authentication
            private_key = file("./remote-exec-keypair.pem")
            host = self.public_ip
        }
    }
}
```

#### Provisioner Failure Behaviour

- By default, provisioners that fail will cause the `apply` command to fail.
- This behaviour can be altered by changing the `on_failure` setting to 1 of 2 values:
  - **Continue:** Ignore the error and continue with the resource creation
  - **Fail:** Raise an error and stop the apply (default behaviour).

#### Provisioner Types

- Two types of provisioners:
  - **Creation-Time**
    - Only run during creation, not during updating or any other lifecycle
    - If a creation-time provisioner fails, the resource is marked as tainted
  - **Destroy-Time**
    - Ran before the resource is destroyed.

#### Input Variables

- The value associated with a variable can be assigned via multiple methods
- Value associated can be defined either by the CLI or TFVars file.
- To load a custom tfvars file: `terraform apply -var-file="filename.tfvars"`

#### Variable Definition Precedence

- Terraform loads variables in the following order, with the importance increasing as the list progresses:
  1. Environment Variables
  1. Terraform.tfvars
  1. Terraform.tfvars.json
  1. Any `*.auto.tfvars` or `*.auto.tfvars.json` files processed alphabetically
  1. Any `-var` or `-var-file` CLI arguments provided.
- If a variable is defined multiple times with different values, the last definition will be the applied value.

#### Local Backend

- Stores the state on the local file system
- Locks the state using system APIs
- Performs operations locally
- The default backend used by Terraform
- Path should be specified where appropriate

#### Required Providers

- Each Terraform module must declare which providers it needs so Terraform can install and use them
- Provider requirements are declared in a `required_providers` block in a similar manner to:

```go
terraform {
    required_providers {
        mycloud = {
            source = "mycorp/mycloud"
            version = "~> 1.0"
        }
    }
}
```

#### Required Version

- The `required_version` setting accepts a version constraint string, specifying the version of Terraform to be used with your configuration.
- If the running of Terraform doesn't match the specified constraints, Terraform will produce an error and exit without applying any more changes.

##### Version Arguments

| Version Argument | Description                        |
|------------------|------------------------------------|
| >= x.y           | Greater than or equal to x.y       |
| <                | Less than or equal to x.y          |
| ~>x.y            | Any version in the range x.y       |
| >=X.Y,<=A.B      | Any version in the range X.Y - A.B |

#### Fetching Values from a Map

- Reference a value from a map variable via `var.<variable name>["<key>"]`

#### Terraform and GIT

- In practice, careful consideration should be taken when committing Terraform code.
- The `.gitignore` should be configured to ignore files which may contain sensitive information such as:
  - `terraform.tfstate`
  - `*.tfvars`
- Arbirtrary git repositories can be used by prefixing the address with a special `git::` prefix
  - Any valid git URL can be specified to select one of the protocols supported by GIT.
- By default, Terraform will clone and use the default branch (HEAD) in the selected repository
  - This can be overwritten by adding the ref argument e.g.:

```go
module "vpc" {
    source = "git:://https://example.com/repo.git?ref=v1.0"
}
```

- The value of the `ref` argument can be any reference that would be accepted by the `git checkout` command, including branch and tag names.

#### Dependency Types - Implicit

- With implicity dependencies, terraform automatically finds references of the object and creates an implicit ordering requirement between the two resources.
- A common example is creating an Elastic IP address to be associated with an EC2 instance's Public IP, which can be specified as `aws_eip.my-eip.private_ip`
  - This defines an implicit dependency that will inform Terraform to create the EIP first before creating the EC2 instance.

#### Dependency Types - Explicit

- Explicitly specifying a dependency is only required when a resource relies on another's behaviour but doesn't access any of that resource's data.
- One can add `depends_on = [<resource_type.<resource_id>]` to specify an explicit dependency

#### State Command

- List resources in the state: `terraform state list`
- Move or rename items within the state: `terraform state mv`
- Manually download and output the state from state file: `terraform state pull`
- Remove items from the state file: `terraform state rm`
- Show the attributes of a resource in the state file: `terraform state show`

#### Data Source Code

- Data sources allow data to be fetched or computed for use elswhere within the configuration.
- Reads from a specific data source and exports the results under a particular value.
- Common example is AWS AMIs as these vary from region to region.

#### Terraform Plan Destroy

- The behaviour of `terraform destroy` can be previewed by `terraform plan -destroy`

#### Terraform Module Sources

- The module installer supports installation from a number of different source types, such as local paths, terraform registry, etc.
- Local path references allow for factoring out portions of configuration within a single source repository.
- A local path must begin with either a `./` or `../` to indicate it's a local path.

#### Larger Infrastructure

- Cloud providers have certain amounts of rate limiting, meaning only a certain number of resources can be reqiested over a period of time.
- It's recommended that larger configurations are broken into multiple smaller sets that can be independently applied.
- Alternatively, can use the `-refresh=false` and target flags, though this is not recommended.

#### Miscellaneous Pointers

- Lookup retrieves the value of a single element from a map `lookup(map, key, default)`
- Various commands refresh the state implicitly, such as `plan`, `apply`, and `destroy`, `init` and `import` do not.
- Array data type is not supported by Terraform.
- Various variable definition files can be loaded such as:
  - `terraform.tfvars`
  - `terraform.tfvars.json`
  - Any files with `.auto.tfvars.json`
- Both implicit and explicit dependencies are stored in `terraform.tfstate`
- `terraform init -upgrade` automatically will upgrade all previously installed plugins to their newest versions.
- The terraform console provides an interactive console for evaluating expressions.
- The declaration of variables differs between terraform 0.11 and 0.12:
  - 0.11: `"${var.varname}"`
  - 0.12: `var.varname`
