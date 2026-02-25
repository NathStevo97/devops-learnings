# 7.0 - Terraform Cloud and Enterprise

## 7.1 - Terraform Cloud Overview

- Terraform Cloud manages Terraform runs in a consistent and reliable environment. It provides various features such as:
  - Access controls
  - Private registry for module sharing
  - Policy controls

- Terraform Cloud projects are stored in workspace repositories
- Within these workspace repositories, information detailing the project can be found alongside additional info regarding Terraform runs, such as:
  - Plan details
  - Monthly cost estimates
  - `terraform apply` details.

- In some cases, policy checks may be present, this is essentially to verify any tags associated with resources.
- Users are allowed to comment on runs to keep track of progress and provide updates when necessary.

- Environment variables can be set within Terraform Cloud, and the TFstate file can be viewed.

- Terraform cloud can also be linked to Github repositories for projects, so when any changes are made, they are automatically applied to the workspace repository.

## 7.2 - Creating Infrastructure with Terraform Cloud

- Pricing for Terraform Cloud depends on the user's requirements.
  - For teams and governance, more features would be required compared to a personal user.
  - TO create an account, review the following [link](https://app.terraform.io/signup/account)
- When getting started, you must first create an organization and a workspace.
  - Then link a version control tool e.g. Github.
  - Providers may need to be added - achievable via `Settings -> VCS Providers`

- For Github, the following needs to be added:
  - An optional display name for the VCS provider.
  - Client ID
  - Client Secret

- For the latter two, setup on Github is required:
  - In a repository of choice: `settings -> developer settings -> oauth applications`
  - Register the oauth application, detailing parameters such as:
    - Homepage URL (refer to Terraform Documentation)
    - Template Callback URL
  - The above step will present the client ID and secret to be added in Terraform Cloud's VCS Provider setup.
  - Add the Client parameters to the Terraform Cloud setup generates the Callback URL -> add this to the Github application.

- To create infrastructure with Terraform Cloud, add/commit any sets of files to the Github repository, then create a Workspace in Terraform Cloud.
  - When creating the workspace, connect the chosen VCS provider, and select the desired repository.

- Once configuration is complete, Terraform-related variables and environment variables must be configured, this can include AWS access keys, defaults, etc.
- Queue a plan - Initiating a `terraform plan` invocation using the code in the linked repository
- If the plan is successful, the `terraform apply` command can be invoked, or a comment can be added alongside in the event of failure.

- Terraform state file is stored on Terraform Cloud by default in this scenario for plan, apply and destroy operations.
- For production environments or plans, cost estimation for running projects and applying configurations can be obtained.

## 7.3 - Sentinel

- An embedded policy-as-code framework integrated with the products provided by Hashicorp.
- Allows fine-grained, logic-based policy decisions, which can be extended to use info from external sources.
- A paid feature of Terraform.
- Carries out policy checks during `plan` and `apply` invocations.

- As an example:
  - A policy may be put in place for EC2 instances e.g. "forbid creation if no tags are set"
  - This policy would be attached to a policy set, which would then be applied to a workspace.

- To create a policy set:
  1. Settings -> Policy Set -> Connect a Policy Set
  2. Configure VCS Connection as Required
  3. Configure Settings for policy and what workspace(s) to apply the policy to.

- To create the policy:
  1. Settings -> Policies -> Create Policy
  1. Add policy where required.
  1. Set enforcement mode.
        1. Hard-Mandatory: Cannot Override
        1. Soft-Mandatory: Can be Overrode
        1. Advisory: For logging purposes
  1. Add policy code (see Terraform Documentation)
  1. Associate the policy with a policy set

- Now when a plan is queued, the policies will be checked to see if the `apply` can be ran, displaying the results as logs in the UI.

- Example Policy:

```go
import "tfplan"


main = rule {
    all tfplan.resources.aws_instance as _, instances {
        all instances as _, r {
            (length(r.applied.tags) else 0) > 0
        }
    }
}
```

## 7.4 - Remote Backend

- The remote backend stores Terraform state files and may be used to run operations in the Terraform Cloud.
- TF Cloud may also be used with local operations, in which case, only the state is stored in the remote backend.

### 7.4.1 - Remote Operations

- When using full remote operations, commands like `terraform plan` can be executed in Terraform Cloud's runtime environment, with log output streamed to the local terminal.
- To configure the backend, the following must be applied to the Terraform configuration files

- In the file containing the resource(s), add a block containing `backend "remote" {}`
- In `backend.hcl` add the following:
  - `workspaces { name = "repository_name" }`
  - `hostname = "app.terraform.io"`
  - `organization = "organization_name"`

- Once setup, when Terraform plan or apply is ran, it will run the Terraform Cloud UI. The logs can then be viewed directly via this method.
- Additionally, cost estimations and Sentinel Policies will be checked if enabled.
- If resources are configured locally but remote operations are desired, a workspace with a VCS connection cannot be used.

## 7.5 - Implementing Remote Backend

- Steps:
  1. Create workspace without VCS Connection
  2. Configure `backend.hcl` - detailing workspace, hostname, and organization info
  3. Configure resource configuration files with Terraform block containing `backend "remote" { .... }`
  4. Initialize the config with the backend file via `terraform init -backend-config=backend.hcl`

- For authenticaiton with a remote backend, a token is required.
  - Run `terraform login` to generate the token - the credentials are stored to a particular path upon successful execution.
  - The API token can be found on the Terraform Cloud UI, which is then copied into the user input requested.

  - Step 4 can then be re-ran if there were any issues - ensuring any required environment variables are set in the TF Cloud Workspace.
