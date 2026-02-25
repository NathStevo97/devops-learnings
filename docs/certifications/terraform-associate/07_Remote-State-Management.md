# 5.0 - Remote State Management

## 5.1 - Integrating with Git for Team Management

- For personal projects and testing, local terraform state will suffice.
- When working on client projects and in a team, it's likelier and easier to use a remote state; storing it in a backend within the cloud.
- Source code should always be stored in a central Git repository (Without exposing any credentials!).

## 5.2 - Security Challenges

- For security purposes, sensitive information such as usernames and passwords should not be stored in an online repository.
- For sensitive information, one could store them in separate files outside the repository to be referenced by the `file` function, however this still commits the values to state; so not that secure.

## 5.3 - Remote State Management

- A feature of Terraform that allows you to store tfstate files in a central repository that isn't easily accessible like Git.

- Typically, many cloud providers offer solutions for this, such as using an S3 bucket in AWS.
- Generally, Terraform supports 2 types of remote backends:
  - **Standard:** Allows state storage and locking
  - **Enhanced:** All features of standard backends, with the addition of remote management.

## 5.4 - Implementing S3 Backend

- Terraform has multiple backends supported for remote storage.
- For AWS, the standard practice is to use an S3 bucket.
- Unless a remote backend is specified, the TFstate file will be stored locally by default.

- Remote backends can be implemented in a similar format to:

```go
terraform {
    backend "s3" {
        bucket = "bucket name"
        key    = "tfstate_filename.tfstate"
        region = "<region>"
    }
}

```

- **Note:** The bucket has to be created manually in AWS prior to remote state creation.

## 5.5 - State File Locking

- During any operation that affects the state file, such as an `apply` command, the state file is locked by Terraform.
- This is hugely important as if someone edited the state file during application, the state will become corrupted.
- State file locking automatically occurs when working with Terraform in the CLI and state file if stored locally.
  - For remote backends, other methods are required for state locking.

## 5.6 - Integrating DynamoDB with S3 for State Locking

- To implement state locking on a TFState file stored in an S3 bucket, one can utilize a DynamoDB table.
- This DB, like the S3 bucket for remote stage storage, must be created manually.
- Once created, it can be referenced in Terraform in  a similar manner to the following:

```go
resource "aws_dynamodb_table" "terraform_state_lock" {
    name = "terraform-lock"
    read_capacity = 5
    write_capacity = 5
    hash_key = "LockID"
    attribute {
    name = "LockID"
    type = "S"
    }
}
```

## 5.7 - Terraform State Management

- It's good practice to use the `terraform state` command to make any state file modifications, rather than editing the state directly.
- State commands:

| State Command      | Description                                        |
| ------------------ | -------------------------------------------------- |
| `list`             | List resources in the state                        |
| `mv`               | Move an item in the state                          |
| `pull`             | Pull current state and output to a standard format |
| `push`             | Update a remote state from a local state file      |
| `replace-provider` | Replace a provider in the state                    |
| `rm`               | Remove instances from the state                    |
| `show`             | Show a resource in the state                       |

- The `mv` command is primarily used when you want to rename an existing resource without destroying and recreating it.
- The command will output a backup copy of the state prior to saving any changes.
- The mv command syntax generally follows:
  - `terraform state mv [options] /path/to/src`
  - `terraform state mv <name1> <name2>`

- The `pull` command is used to manually download and output the state from a remote state.
  - This is useful for reading values out of the state file and pairing it with other commands.

- The `push` command, though rarely used, can manually upload a local state file to a remote state.

- The `rm` command can be used to remove items from the state - this will not destroy the items, just stops Terraform from managing them.

- `show` shows all the attributes for all the resources. For a particular resource, use `terraform state show  <resource type>.<resource id>`

## 5.8 - Importing Existing Resources with Terraform Import

- If a resource has been created via manual methods, but you wish to manage it via Terraform, it must be imported.
- To import a resource, a  corresponding resource block with particular parameters must be defined.
  - This resource block is defined as normal, but must contain values specific to the resource e.g. name must be correct.

- To import, run `terraform import <resource type>.<resource_identifier>`

- This will look up the resource based on the provided configuration and save the mapping to the Terraform state.
  - This can be verified by `terraform state` commands.

- Once verified, any changes to the resource will now have to be made via Terraform.
