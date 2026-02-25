# 2.0 - Working with Configurations

## 2.1 - Attributes and Output Values

- Terraform can output the values of certain attributes of a resource.
- Output attributes can be used for both user reference, as well as input variables for other resources to be created.
  - **Example:** When an elastic IP address is created, it should automatically be added to the security group for whitelisting.
- For an output, if you set a value as `<resource_type>.<resource_id>`, this will output all the attributes associated with that resource.
- For a particular output, append the attribute name to the above reference i.e. `<resource_type>.<resource_id>.<attribute_name>`.
  - Example: `aws_eip.lb.public_ip`

- **Note:** A list of attributes that can be output is generally listed with each resource in the Terraform documentation.

- **In general:**
  - Attribute: Reference of a value associated with a particular property of a resource
  - Outputs: Used to output the value of a particular attribute.

- Example output:

```go
output "public_ip" {
    value = aws_eip.lb.public_ip
    description = "<insert description>"
}
```

- For all the attribute outputs available, omit the attribute name from the output value i.e.:

```go
output "public_ip" {
    value = aws_eip.lb
    description = "<insert description>"
}
```

- Note: Outputs can also be used by other projects to reference specific values e.g. if project B needs to refer to the IP address output by project A - this is done by referring to the terraform state outputs of the source project.

## 2.2 - Referencing Cross-Account Resource Attributes

### Introduction

- As suggested previously, when creating resources, one should be able to use attributes and outputs to allow automatic configuration
- Examples follow:
  - Creating an Elastic IP and assigning it to an AWS EC2 Instance.
  - Creating an Elastic IP and assigning it to a Security Group for whitelisting

### 2.2.1 - EIP Association to EC2 Instance

- Associating an EIP with the EC2 instance, one requires an `aws_eip_association` resource, which will specify the following values based on other attributes:
- `instance_id = aws_instance.instance.id`
- `allocation_id = aws_eip_eip.id`

### 2.2.2 - EIP Association with Security Group

- Defining the security group should follow a format similar to:

```go
resource "aws_security_group" "allow_tls" {
    name = "allow_tls"
    description = "Allow TLS inbound traffic"
    vpc_id = aws_vpc.main.id
    ingress {
        description = "TLS from VPC"
        from_port = 443
        to_port = 443
        8
        protocol = "tcp"
        cidr_blocks = [aws_eip.myeip.public_ip]
    }
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
    tags = {
        Name = "allow_tls"
    }
}
```

## 2.3 - Terraform Variables

- When working with Terraform. there's a significant chance there will be multiple static values in the project e.g. ami, ports, commands.
- Changing these values can become tedious to alter if used multiple times.
- To avoid this, it's advised to utilise variables.
- Typically variables are supplied from a file `variables.tf` in a centralised location, stored in the format:

```go
variable "<variable id>" {
    default = "<value default>"
    type = <type>
    description = "<variable description>"
}
```

- To reference a variable in a configuration, add `var.<variable_id>` where appropriate.
- Depending on the type of the variable, to adhere to data types, you may need to include it within parentheses e.g. [] for lists, or {} for maps.

- Once done, when `terraform apply` is ran, the variables stored in `variables.tf` are referenced.
- This massively simplifies things in production for variable values subject to change, such as IP addresses.

## 2.4 - Variable Assignment

- Variables can be assigned via 4 main methods:
  - **Environment Variables:**
    - A fallback method in case the others do not work.
    - Terraform will search its own local environment to find an environment variable to apply.
    - Terraform environment variables are set by any environment variables prefixed with `TF_VAR_`.
    - Example: `export TF_VAR_<variable name> <variable value>`
  - **Command-line flags:**
    - Not recommended unless only altering 1 variable,
    - Used by appending a flag during `plan` or `apply` commands e.g.:
      - `terraform plan -var="variable_id=value"`
    - Usually used when wanting to quickly test the effects of a new variable.
  - **From a file:**
    - Recommended over command line flags
    - In a new file `terraform.tfvars`, one can specify each variable's value in the form `variable_id = <value>`
    - To reference this file, append `-var-file="filename.tfvars"` when running `plan` or `apply` commands.
    - This will overrule any defaults set in `variables.tf`
  - **Variable Defaults:**
    - Store variable values in `variables.tf` and specify default values, referencing via `var.variable_id`.

- If no additional variable values are specified, the value will be assumed to be the default value (specified in `variables.tf`)
- If no default is specified, the value will need to be entered during command execution.
- Any variables entered at CLI level will take precedence over defaults and environment variables.

## 2.5 - Data Types

### 2.5.1 - Example

- Consider a company where every employee has a particular identification number, if that employee wanted to create a form of infrastructure, it should be done with that number
only.
- So in `variables.tf`, the variable `instance_name` should be of type number.

- Suppose that in the `terraform.tfvars` the value for instance_name is set to a value that isn't of that data type/the data type also isn't specified, eg. john-123; what will happen?
  - This value will not be accepted and the plan will fail.

### 2.5.2 - Data Types Overview

- To specify a variable's data type, simply add the type in the variable within `variables.tf` in the form `type = type`.
- Key types used include:
  - **String:** A set of unicode characters representing text e.g. `"hello"`
  - **List:** A sequential list of values identified by position within the list, position starting with 0 e.g. `["London", "Paris", "Helsinki"]`
  - **Map:** A group of values categorized by labels e.g. `{name = "Joe", age = 23}`
    - This can contain multiple data types if desired.
  - **Number:** Numerical values

- By defining data types in `variables.tf`, users can use this as a reference point when defining variables in the `.tfvars` file.
- In some cases, if a variable type isn't specified, errors will arise as the program will assume a different type is expected.

## 2.6 - Fetching Data from Maps and Lists in Variables

- When working with lists in terraform, sometimes you wish to reference a particular value from that list, rather than include all the values.
- When referencing items from a map, follow the format: `var.map_id["map_key"]`
- When referencing items from a list: `var.list_id[list_position]`
- List positions ALWAYS start from [0].

## 2.7 - Count and Count Index

- The count parameter on resources can simplify configurations and allow easier scalability of configurations.
- Commonly, if wanting to create a small number of the same resource, e.g. 2 identical instances, one could define them as separate instances, however this is not sustainable.
- The Terraform function `count` can be used to save code space by adding `count = value`
- In resource blocks where count is set, an additional count object is available in expressions,
so each instance's configurations can still be modified.
- This object has just one attribute: `count.index`, which starts with 0 for the first instance and continues like a list index.
  - This is commonly used for altering properties such as the name.

- When wanting to utilize the count index, append `.count.index` to the chosen property.

- Example application to create 3 virtual machines:
  - `machine_instance.0` -> count = 1
  - `machine_instance.1` -> count = 2
  - `machine_instance_2` -> count = 3

- The above isn't a common practice, usually resources are configured for different environments like staging, development, etc.
  - Count can still be utilized for this, but it'll reference positions in a list instead.
  - This can be done in a similar manner to `var.<variable>[count_index]` - which will look iteratively through the list and apply each desired entry.

## 2.8 - Conditional Expressions

- Expressions that use booleans to select one of two values, true or false.
- Defined in Terraform in a similar manner to `condition ? true_val : false_val`

- Example: Suppose there are a set of resources that should only be created if a particular variable is set e.g. `use_dev_env = true`

- For each resource, add an attribute property followed by the condition:
    `attribute = var.<variable name> == true ? <true value> : false value`

- In the other dependent variable:
    `attribute = var.<variable name> == false ? <true_value> : <false_value>`

- The boolean variable is defined with a default value in `terraform.tfvars` and `variables.tf`

## 2.9 - Local Values

- A local value assigns a a name to an expression, allowing it to be used multiple times within a module without repeating it.

- To define local tags, add `locals {}` and then the desired values in the required format.
- Locals can be categorized and referenced accordingly e.g. `development = {}`, `production = {}`
  - To reference a category, add `local.<category_name>.<category value`
- An example follows:

```go
locals {
    common_tags {
        Owner = "DevOps Team"
        service = "backend
    }
}
```

- A common example for using locals is for non-sensitive defaults and conditionals, like resource name prefixes:
  - `name_prefix = var.name !="" ? var.name : local.name`

- The above example defines a naming convention. If `var.name` is blank, then the prefix defined in `local.name` is used.

- Locals can be helpful to avoid repeating the same values or expressions multiple times.

- They should be used in moderation, as they can make a configuration hard to read by future users of the files, they should only be used in situations where a single value or result is used in many places and said value is likely to be changed.

## 2.10 - Functions

- Terraform has many built-in functions that can be used to transform and combine values.
- The general syntax for a function is the function name followed by arguments separated by commas.
- *User-defined functions aren't supported*, but built-in function categories are:
  - Numeric
  - String
  - Collection
  - Encoding
  - Filesystem
  - Date and time
  - Hash and Crypto
  - IP Network
  - Type connection

- Further details for each is provided in the Terraform documentation.
- A popular function is `lookup`, which can be used to look up the value of a single element from a map given its key. If the key doesn't exist, a default value will be used.

- Example: `lookup(map, key, default)`

- Another function is `element`, which retrieves a single element from a list, example usage: `element(list, index)` - `count.index` is often used here.

- File" `file("/path/to/file")` reads the contents of the file defined in quotation marks, commonly used for ssh keys, etc.

- `formatdate` & `timestamp` are often used in conjunction to format the value returned by `timestamp` into a more readable manner

## 2.11 - Data Sources

- Data sources allow data to be fetched or computed for use elsewhere within Terraform configuration.
- As an example, if an AWS EC2 Instance was to be configured, the desired AMI will differ depending on the region.
- Rather than manually hardocde the AMI, a data source can be used to filter the appropriate AMIs for a given region.
- Data source code is defined under a `data` block and reads from a specific data source, exporting it to the data block identifier.

- Example:

```go
data "aws_ami" "app_ami" {
    most_recent = true
    owners = ["amazon]
    filter {
        name = "name"
        values = ["amazn2-ami-hvm*"]
    }
}
```

- Now when `terraform plan` is applied, the data source block will automatically search for the latest iteration for the Amazon Linux 2 AMI for the chosen region. This can be altered for different owners, ami values, etc.

## 2.12 - Terraform Debugging

- Terraform tracks all changes in a series of logs, which can be enabled by setting the environment variable `TF_LOG`.
  - Accepted values are:
    - TRACE
    - DEBUG
    - INFO
    - WARN
    - ERROR
- Set `TF_LOG` via `export TF_LOG=<value>`
- To save logs, set `TF_LOG_PATH=/path/to/log/file`

- Now when all commands are ran, the logs are pushed to the path set in `TF_LOG_PATH`
- `TRACE` is the most extensive overview and the default setting for `TF_LOG`, the logs increase in verbosity in the order of the list above.

## 2.13 - Terraform Format

- When working with Terraform, readability is very important. Good practice for example is to ensure that all equals signs are aligned.

- To format in this manner, run `terraform fmt`.
- This will automatically apply any indentations and alignments needed to make the configuration valid.

## 2.14 - Validate Config Files

- Prior to running `terraform plan`, it's important to ensure configuration files are syntactically correct.

- Otherwise, when `plan` and `apply` are ran, errors may occur which can derail things.

- To validate, run `terraform validate`

- This checks the syntax for the configuration files ensuring there are no incorrect attributes, all variables are declared, etc.

## 4.15 - Load Order and Semantics

- Generally, Terraform will load all the configuration files within the specific directory in alphabetical order, so long as the files end in `.tf`.
- In general practice, code should be split into multiple files. For example, a file for providers, a file for all networking resources, etc.
  - This allows for easier management of infrastructure.
- **Note:** When adding 2 of the same resource, you must give different IDs after defining the resource type.

## 2.16 - Dynamic Blocks

- Often there are repeatable nested blocks of resource code that need to be defined.
- If not managed carefully, this could lead to long stretches of code that are difficult to manage. Commonly, this occurs with resources that have multiple entries e.g.:
  - Security Groups
  - Ingress Rules
  - Egress Rules

- To work with this, one can use a dynamic block, indicated by the usage of `dynamic` prior to the resource identifier.
- Dynamic blocks allow you to iteratively add content defined in a separate variable list or map.

- Ingress Property Example:

```go

resource "aws_security_group" "dynamicsg" {
    name = "dynamic-sg"
    description = "Ingress for Vault"

    dynamic "ingress" {
        for_each = var.sg_ports
        iterator = port
        content {
            from_port = port.value
            to_port = port.value
            protocol = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
        }
    }

    dynamic "egress" {
        for_each = var.sg_ports
        content {
            from_port = egress.value
            to_port = egress.value
            protocol = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
        }
    }
}

```

- This dynamic block will iteratively fill out the contents of the ingress and egress blocks with the content defined in a separate variable as a list. The egress block is filled out in a similar manner.

- Iterators are optional arguments which set the name of a temporary variable that represents the current element of a more complex value. It's commonly seen in conjunction with the `for_each` operator i.e. `for_each = var.sg_ports` - where `sg_ports` is a list to be iterated over.

- If omitted, the name of the variable defaults to the dynamic block's label (similar to the egress example above).

## 2.17 - Tainting Resources

- Consider a scenario where a new resource has been created, but users have made a lot of manual changes to it in terms of both infrastructure and within the server.
- To deal with this, one can either import the changes to Terraform or delete and recreate the resource to update the configuration.
- The command `terraform taint` manually marks a resource as "tainted", forcing the resource to be destroyed and recreated during the next `terraform apply` execution.
- To taint, use the command similar to: `terraform taint <resource type>.<resource_id>`

- Newer approach (from version ~0.15 onwards) is to utilize the `-replace` flag i.e. `terraform apply -replace="<resource type>.<resource id>"`, this cuts out the middle-man step.

## 2.18 - Splat Expressions

- An expression that produces a list of all the attributes, denoted by *.
- Essentially denotes "anything" or "all".
- Example:

```go
provider "aws" {
    region = "eu-west-2"
}

resource "aws_iam_user" "lb" {
    name  "iamuser.${count.index}"
    count = 3
    path = "/system/"
}

output "arns" {
    value = aws_iam_user.lb[*].arn
}
```

- The above aims to create 3 IAM users in AWS.
- The value `aws_iam_user.lb[*].arn` will look for each of the 3 arns associated with the IAM user.
- The resultant output will therefore be:

```go
arns = [
"arn:aws:iam::746085785702:user/system/iamuser.0",
"arn:aws:iam::746085785702:user/system/iamuser.1",
"arn:aws:iam::746085785702:user/system/iamuser.2"
]
```

- This could also be applied to any other listable properties.
- Officially: *A splat expression provides a more concise way to express a common operation that could otherwise be performed by a `for` operation*

## 2.19 - Terraform Graph

- A command used to generate a visual representation of a configuration or execution plan.
- Expressed in the DOT format, which can be converted to an image format.
- Usage: `terraform graph > filename.dot`
- For conversion, one can utilize a graph visualization package like Graphviz.

## 2.20 - Saving Terraform Plan to a File

- When generating a Terraform plan, it can be beneficial to save it to a particular path.
- By doing so, this plan can be viewed later or can be used toa pply changes specified only by that plan.
- To save a plan: `terraform plan -out /path/to/file`
- To apply a saved plan: `terraform apply /path/to/file`

## 2.21 - Terraform Output

- Used to extract the value of an output variable from the state file.
- Configured by `terraform output <state file attribute>`
- Advised to use for verification and debugging purposes. Particular outputs can be manually added in the .tf configs for ease e.g. Load Balancer DNS.

## 2.22 - Terraform Settings

- The `terraform {}` block is used to configure the behavior of Terraform itself when acting upon the configuration defined.
- Common settings include:
  - `required_version` - string criteria to determine the minimum / acceptable versions of Terraform that can be used with the configuration
  - `required_providers {}` - Specifies all providers required by the current module, mapping each to a specific source and assigning version constraints.

- Example:

```go
terraform {
  required_Version = "> <major>.<minor>.<patch>"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.52.0"
    }
  }
}

<AWS Provider configuration>
```

## 2.23 - Challenges with Large Infrastructure

- When dealing with significantly large configurations, API limits for a provider may be incurred.
- This occurs as when Terraform plan runs, the state is refreshed for each resource defined - this can take significantly long for large amounts of infrastructure.
- To work around this, it's advised to break resources up into separate configuration files, this can be on per-resource type, per function, per component, etc.

- If still facing issues post-breaking configuration down, one can stop Terraform from querying the current state by adding the `-refresh=false` flag.
- Alternatively, Terraform commands can be used to target specific resources e.g. `-target=<resource type>.<resource name>` or `-target=<resource type>` for all instances of a particular resource.
  - This is **NOT** a recommended approach for production!

## 2.24 - ZipMap Function

- Creates a map from a list of keys and values e.g.:

```shell
zipmap(["a", "b", "c"], ["1", "2", "3"])

|
v

{
    "a" = "1",
    "b" = "2",
    "c" = "3"
}
```

## 2.25 - Comments in Terraform

- Terraform supports multiple ways of writing comments:
  - Single-line: `#` or `//`
  - Multi-line: `/*` and `*/`

## 2.26 - Resource Behavior and Meta Arguments

## 2.27 - Meta Arguments: Lifecycle

## 2.28 - Challenges with Count

## 2.29 - Set Data Type

## 2.30 - For_Each
