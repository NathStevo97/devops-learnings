# 4.0 - Modules and Workspaces

## 4.1 - DRY Principle

- Focused on the aspect of software engineering - **Don't Repeat Yourself**
- This aims to reduce the repetition of software patterns, such as defining functions for specific tasks where possible.
- This can also be applied to Terraform, one can define resources as modules to be called repeatably.

- Modules are typically defined in the following manner:

```go
module "<module name>" {
    source = "/path/to/module"

    input_var = <value>
    ....
    ....
}
```

- When Terraform is ran, it will check the defined source path to determine the configuration details.

## 4.2 - Module Implementation: EC2 Instance

- Adopting the following Architecture:

- Root
  - Modules
  - Projects
    - A
    - B

- A sample EC2 Module can be created by adding the following to a file under `modules`

```go
resource "aws_instance" "myec2" {
  ami           = "ami-0a13d44dccf1f5cf6"
  instance_type = "t2.micro"
  key_name      = "remote-exec-keypair"
  #configure provisioner with inline commands
  provisioner "remote-exec" {
    inline = [
      "sudo amazon-linux-extras install -y nginx1.12", #install nginx
      "sudo systemctl start nginx"
    ]
    connection {
      #connection method
      type = "ssh"
      user = "ec2-user"
      #private key for authentication
      private_key = file("./remote-exec-keypair.pem")
      host        = self.public_ip
    }
  }
}
```

- This can then be referenced by any terraform files in the projects folder, which will pull all the required provider plugins alongside it.
- Using modules makes things significantly easier for management and readability, as all configuration is stored and therefore managed in 1 place.
  - Similarly, any users unfamiliar to Terraform will not be overwhelmed when using the module, as they would only need to reference the module and add any required input variables.

## 4.3 - Variables and Terraform Modules

- A common challenge with infrastructure management is the need to build environments, such as dev, staging, and production, with generally similar setups, but with slightly different variables.
- Module variables cannot be overridden, if you wish to change the values of a property, you can create a variables.tf file to reference in the folder
- Now, if a value is hardcoded in the source module, the variable value can be overwrote by any configuration referencing said module.

```go
module "<module name>" {
    source = "/path/to/module"

    input_var = <value>
    ....
    ....
}
```

## 4.4 - Terraform Registry

- A repository of modules written by the Terraform community.
- Modules are typically developed by third parties, however some community-submitted providers are also available.
- Hashicorp review modules for verification, and verified modules are actively maintained to remain up to date with Terraform and the respective providers.
- In the Terraform registry, modules are typically supported with:
  - Usage examples
  - Documentation and Variable Usage Guidance
- Using a module from Terraform Registry is similar to a standard module stored locally, just reference the source appropriately and specify any other parameters required.
  - `terraform init` will then reference this configuration and pull down the required files.

## 4.5 - Terraform Workspace

- Workspace = Groupings of applications.
- Terraform allows the use of multiple workspaces. Each workspace can use a set of environment variables.
  - This is often useful for running multiple environments on the same machine.

- To utilize workspaces:

| Command                                       | Definition                                                                                   |
| --------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `terraform workspace list`                    | List the existing workspaces <br> Current workspace denoted by *                             |
| `terraform workspace select <workspace_name>` | Switch to a pre-existing workspace                                                           |
| `terraform workspace new <workspace_name>`    | Create a new workspace (automatically switches)                                              |
| `terraform workspace delete <workspace_name>` | Delete a particular workspace <br> Use `-force` to force deletion if not an empty workspace. |
| `terraform workspace show`                    | Show current workspace details                                                               |

## 4.6 - Implementing Terraform Workspace

- Considering a scenario for a set of workspaces, with a variable that's subject to change from workspace-to-workspace.
- Rather than having separate variables files, which would be hard to track and maintain, one can use a standalone variables file in a similar manner to the following:

```go
variable "instance_type" {
    type = "map"
    default = {
        workspace1 = value1
        workspace2 = value2
        workspace3 = value3
    }
}
```

- Using variables like this is achieved by: `lookup(var.<var name>, terraform.workspace)`

- Each workspace's state file is stored in a new folder, `terraform.tfstate.d`. The default workspace's state file remains in the standard location.
