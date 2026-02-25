# 3.0 - Provisioners

## 3.1 - Introduction to Provisioners

- Provisioners are used to execute scripts or commands locally or on a remote instance during resource creation. A classic example is installing NGINX on a web-server.

```go
provisioner "remote-exec" {
    inline = [
        "sudo amazon-linux-extras install -y nginx1.12",
        "sudo systenmctl start nginx"
    ]

    connection {
        type = "ssh"
        user = "ec2-user"
        private_key = file("~/path/to/key")
        host = self.public_ip
    }
}
```

- When defining the `remote-exec` provisioner, one must define the inline commands to be run as well as the method of connection (with associated parameters).

## 3.2 - Provisioner Types

- There are 2 main types of provisioner:
  - **Local-Exec:**
    - Allows invocation of local executables after the resource is created
    - Commands defined run on the machine where terraform's being run on e.g. "runner VM", local machine, etc.
  - **Remote-Exec:**
    - Commands executed directly on the remote machine / resource.
    - Connection made typically via SSH, defined in Terraform code.

## 3.3 - Remote-Exec Implementation

- For remote-exec to run, the resource must be created first i.e. the provisioner must be added within a resource block.
- Requires 2 properties to be defined:
  - Inline: The commands to be ran
  - Connection: Connection parameters for the desired method.

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

- In the `inline` block, any commands to be run in the machine are added, separated by a comma - these must be syntactically correct.
- Under connection, specify the parameters required for the desired connection method e.g. for SSH, one needs the user, private key, and host IP.

## 3.4 - Local-Exec Implementation

- Allows commands to be run on the local machine immediately after resource creation.
- Typically, this is in the form of triggering Ansible playbooks.
- Define the commands required in a similar manner to that of remote-exec, but remove any notion of connections.
