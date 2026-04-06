---
tags:
  - Tooling
  - Packer
---

# Getting Started with HashiCorp Packer

## 1.0 - Creating Basic Images

### 1.1 - Why Packer?

- Packer facilitates the development of immutable infrastructure.
- Cats vs Cattle Analogy
  - **"Cat" Servers**:
    - Require a lot of attention and specific configuration
    - If server goes down, major problems occur.
    - Lots of configuration required to maintain it, as otherwise the workloads supported are totalled.
  - **"Cattle" Servers**:
    - Servers created to serve a specific purpose
    - If the server goes down, not as problematic, another "cattle" can just be spun up quickly to replace it with no immediate difference.

- Summary Comparison:

| Cats                               | Cattle              |
|------------------------------------|---------------------|
| Must be kept alive at all cost     | Expendable          |
| Lots of manual intervention needed | Work out of the box |
| Tough to scale                     | Easy to scale       |
| High-stress management             | Low-stress          |

- Other benefits to immutable infrastructure include:
  - Testable infrastructure -> As infrastructure defined as code (Iac)
  - Easily reproducible environments
  - Infrastructure becomes a "unit of deployment" - deployed alongside the workloads
  - Facilitates confidence in changes

#### Why Packer?

- Packer uses images as its packaging mechanism, offering specific packages per platform
- It's cross-platform, capable of running on and creating images for Windows and Linux
- It allows utilization of existing tools to manage and rollout of infrastructure
- Easily integrates with configuration management tools, such as Ansible, Chef, and standard scripting.

---

#### Packer Basics

- Packer is defined in HCL languages similar to Terraform.
- Images are built via the use of templates, which follow a standard format:

```go
source "type" "name" {

}

build {
    sources = ["source.type.name"]
    provisioner "type" {

    }

    post-processor "type" {

    }
}
```

- `Source` defines the "where" of the configuration build, defining the platform and any specific parameters for the image to be build.
- `Build` defines a unit of execution. Builds refer to 1 or more sources.
  - Within build, you define any number of `provisioners` to carry out configuration tasks for the images.
  - `Post-Processors` are used to "transform" the image after building from one form to another. The most common example for this is "Vagrant".

##### Sources

- Source blocks will always contain:
  - The type of source builder e.g. `amazon-ebs`, `vmware-iso`
  - The local name of the build.
  - Configuration parameters for thhe build:
    - Each build type contains build-specific parameters e.g.:
      - For AWS, one needs to provide an `ami_name`, whereas `vmware-iso` requires ISO information.

##### Builds

- Combine sources with provisioning/post-processing.
- Multiple sources can be included in a single build, so could output multi-platform images with one run, or just do one particular one depending on the needs.
  - This is often beneficial for say different environment builds.

##### Provisioners

- Used to customise the image
- Typically uses scripts (powershell or bash) or configuration management tools like Ansible.
- Provisioners can be configured to run only against particular sources e.g. "fetch ami name" is only applicable to AWS, there's no point running it for a virtualbox build.

##### Post-Processors

- Used to transform build outputs
- Examples include:
  - Checksum generation
  - Export to an AWS AMI or Vagrant Box
- Multiple post-processors can be used sequentially by usage of the `post_porcessors {}` block

#### Common Commands

- `packer fmt <template>.pkr.hcl` - Apply standard formatting
- `packer validate <template>.pkr.hcl` - Syntax validation of configuration
- `packer build <template>.pkr.hcl` - Build the image
  - Common options:
    - `-debug` - pause after each provisioner step and post-processor, provides the SSH key for the machine to verify build process during build.
    - `-var` - supply a variable to the build in the form `<key>=value`
    - `-only` - specify only a particular source
    - `-on-error`

---

### 1.2

- Randomness can be introduced using Packer's function: `${uuidv4()}`

## 2.0 - Adding Configuration, Secrets, and Multi-Platform Functionality

### 2.1 Provisioners

- Provisioners are typically used to help configure Packer images to particular needs.
  - This is typically achieved by allowing files to be used, or:
    - Running configuration management tools (Ansible, Chef, etc)
    - Scripts (Powershell, Bash, etc.) on the image being built or the local system
    - Manage any files to be used by or extracted from the image being built

#### 2.1.1 Provisioners - File

- Used to upload assets, config files, etc. to the image.
- Full directories can be uploaded / downloaded, files included.
- Multiple connector methods available to support this.
- **Note:**
  - The "Packer User" does not have root privileges, it is advised to move any files to a temporary directory before further manipulation in the image, the latter set of operations can be achieved by a script.
  - This provisioner cannot change the permissions of the files, a script(s) should be used for this.

#### Example

```go
source "amazon-ebs" "build" {
    ssh_username = "ubuntu"
    ami_name = "globoticket-${uuidv4()}"
    source_ami = "<ami id>"
    instance_type = "t3.micro"
}

build {
    sources = ["source.amazon-ebs"]

    provisioner "file" {
        source = "config/nginx.service"
        destination = "/tmp/"
    }

    provisioner "file" {
        source = "config/nginx.conf"
        destination = "/tmp/"
    }

    provisioner "file" {
        source = "assets"
        destination = "/tmp/"
    }
}
```

### Provisioners - Script

- Allows running of any scripts used to run programs on the image or local system, with many options available for differing OS. Examples include:
  - Local Shell
    - Run scripts on the local machine, typically used for "prerequisite" actions for other provisioners.
  - Remote Shell
    - Typically used with Linux machines - runs commands on image.
  - Powershell
    - Like remote shell, but used to run Powershell scripts.
  - Windows Shell
    - Used for bash scripts.
  - Windows Restart
    - Causes packer to reboot the VM without losing connectivity.

- **Note:** When running scripts like this in automation, add the `-x` flag to the shebang, which outputs the commands being ran in standard output.

- Example usage, adding beyond the "file" provisioners previously.

```go
build {
    ...
    provisioner "shell" {
        execute_command = "sudo -S env {{.Vars }} {{ .Path }}"
        inline = [
            "mkdir -p /var/globoticket",
            "mv /tmp/nginx.conf /var/globoticket/",
            "mv /tmp/nginx.service /etc/systemd/system/nginx.service",
            "mv /tmp/assets /var/globoticket"
        ]
    }

    provisioner "shell" {
        execute_command = "sudo -S env {{.Vars }} {{ .Path }}"
        script = "scripts/build_nginx_webapp.sh"
    }
    ...
}
```

- In the example above: `execute_command` acts as a prerequisite command to enable the image to run the scripts specified.
- The substitutions in `{{ }}` are substitutions.
  - `.Vars` contains all environment variables needed to pass the command (and any specified as part of the provisioner)
  - `.Path` contains the path to the script Packer will be running, auto-populated.
- `Inline` allows each command to be listed as an array, separated by commas. This is ok for simple operations, but scripts are better for usage.
- When using the `script` parameter, Packer looks to the directory defined, which must be relative to the directory that Packer is being run from (or specify a full path (not recommended)).

### Data Sources

- Data sources are sources of information that can be referenced by Packer to obtain information to be used in image builds. A common example of this is looking up base AMIs in AWS, or looking up secrets manager

```go
data "amazon-ami" "globoticket" {
    filters = {
        virtualization_type = "hvm"
        name = "ubuntu/images/*ubuntu-focal-20.04-amd64-server-*"
        root_device_type = "ebs"
    }
    owners = ["<numeric id>"]
    most_recent = true
}

## Reference the data
source_ami = data.amazon-ami.globoticket.id

data "amazon-secretsmanager" "globoticket-live" {
    name = "Globoticket-live"
    key = "SECRET_ARTIST_NAME"
}

## Reference the secret in `environment`

provisioner "shell" {
    ...
    environment_vars = ["SECRET_ARTIST_NAME=${data.amazon-secretsmanager.globoticket.value}"]
    ...
}
```

### Multi-Provider Builds

- Packer can allow simultaneous generation of images on different providers, such as:
  - VMWare
  - Virtualbox
  - GCP
  - Docker

- There are caveats to this:
  - Some sources are more complex than others
  - Host limitations may become apparent -> may need to run one at a time
  - Outputs can become complex if not managed properly

- For certain providers, you may wish to install provider-specific utilities. Like VMware guest additions.
  - This can be achieved by using another provisioner, and using the `only` parameter to specify it should only run against the specific build

```go
    provisioner "shell" {
        execute_command = "sudo -S env {{.Vars }} {{ .Path }}"
        script = "scripts/virtualbox.sh"
        only = ["virtualbox-iso.globoticket]
    }
```

- Unless specified, packer will build all sources in parallel, to specify, use the `-only` flag on the CLI: `packer build -only 'type.name' template.pkr.hcl`

### 2.1.3 Post-Processors

- Commone examples:
  - Compress
  - Import to Cloud
  - Generate image checksum
  - Generate Manifest
  - Create a Vagrant Box

- For vagrant, one may need to ensure Vagrant is installed to allow the box to be created, steps on this are provided in the documentation.
  - If wanting to keep the input artifact, set `keep_input_artifact=true` in the post_processor block.
