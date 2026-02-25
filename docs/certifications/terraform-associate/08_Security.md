# 6.0 - Security

## 6.1 - Handling Access and Secret Keys

- Any credentials should NEVER be stored in a `.tf` file or associated project.
- They should always be stored as secrets or environment variables.
- For AWS, this could be achieved by running `aws configure` upon downloading the AWS CLI.
  - Similar operations available for Azure and GCP e.g. `azure login`

## 6.2 - Provider Use-Case: Multiple Regions

- Deploying to multiple regions can often be a challenge, as it may require multiple sets of authentication keys and regions.
- Using AWS as an example, if the `region` parameter is removed from `providers.tf`, then users will be asked to enter it and runtime.
- To support multi-region deployment, *provider aliases* can be utilised. This is essentially adding an ID to each instance of a provider.

- Example usage:

```go
provider "aws" {
    region = "us-west-1"
}

provider "aws" {
    alias = "aws02"
    region = "ap-south-1"
    profile = "account02"
}
```

- If one was to deploy resources to the region of ap-south-1 rather than the default us-west-1, one can specify the provider to be used via the alias.
- Usage example: `provider = <provider_type>.<provider_alias>`
- Example from above: `provider = aws.aws02`

## 6.3 - Handling Multiple AWS Profiles with Providers

- When considering resource deployment to multiple accounts, in particular with AWS, one must consider the credentials file at `~/.aws/credentials`
- This file can store credentials for multiple accounts, in a format similar to:

```shell
[account01]
aws_access_key_id = ACCESS_KEY
aws_secret_access_key = SECRET_KEY

[account02]
aws_access_key_id = ACCESS_KEY
aws_secret_access_key = SECRET_KEY
```

- To utilise the credentials from a specific account, in the desired provider, add `profile = "<account name>"`

## 6.4 - Terraform and Assume-Role with AWS STS

- When working with multiple accounts and credentials, it's advised to make use of the assume-role functionality of the AWS Security Token Service (STS).
- This is a web service that enables the request of temporary, limited-privilege credentials for AWS Identity and Access Management (IAM) users or for users that you authenticate (federated users)
- By doing so, one can keep a single set of usernames and passwords, along with authentication keys on an *identity account*. Each account underneath can then be accessed using *assume role* functionality.
- Assume-Role can be allowed for IAM roles via a policy similar to the following:

```json
{
    "Version": "YYYY-MM-DD",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": "arn:aws:iam:<ID>:role/<rolename>|
        }
    ]
}
```

- To provision resources via an account with assume-role privileges:
    `aws sts assume-role --role-arn <arn url> --role-session-name <session_name>`

- Then, one needs to add particular values to the provider.tf file to specify the role being used. Within the provider block add:

```go
assume_role {
    role_arn = "<role arn>"
    session_name = "<session_name>"
}
```

- Role ARNs are resource-specific, session names can be chosen to the user's desire.

## 6.5 - The Sensitive Parameter

- When managing large sets of infrastructure in Terraform, it's highly likely it will involve the use of sensitive information such as credentials.
- This should never be output directly in plaintext for security reasons.
- To avoid, use the `sensitive` parameter, refer to the following example:

```go
output "db_password" {
    value = aws_db_instance.db.password
    description = "Password for Database Login"
    sensitive = true
}
```

- Setting the sensitive parameter to true prevents it being output in the CLI, but it will still be stored in the state, so it's better to utilise a secrets manager for this.
