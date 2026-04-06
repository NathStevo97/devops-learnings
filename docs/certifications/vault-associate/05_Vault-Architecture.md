# 5.0 - Vault Architecture

## 5.1 - Vault for Production Environments

### Overview

- Up until this point, Vault has been used in development mode only.
- In this, all data is stored in-memory ONLY.
- This is obviously not suitable for production, a new storage class is required. Vault supports a multitude of storage class options, such as:
  - Filesystem
  - S3 Bucket (AWS)
  - Databases (MySQL, PostgreSQL, etc.)

#### Deploying in Production Mode

- Vault servers are configured using a particular file in JSON or HCL.
- **Example config:**

```go
storage "file" {
 path = "/root/vault-data"
}

listener "tcp" {
  address      = "0.0.0.0:8200"
  tls_disable  = 1
}
```

- Once setup, the Vault can be started using the config file: `vault server -config /path/to file`
- As we're using a new backend, once the Vault server is started, it must be initialized.
  - In this step, encryption keys are generated, as well as unseal keys and the initial root token.
  - To do so: `vault operator init`
  - This will output the Unseal keys and Root Tokens.
- Once initialized, the Vault must be unsealed. This is true of every initialized Vault.
  - Unsealing is required as Vault knows where to look in the particular storage backend, but it does not have the key to decrypting it and reading the data.
  - To unseal the Vault: `vault operator unseal`

#### Practical Example

- For any VMs used, ensure that SSH port 22 is open for ease of use.
- This example will be set up for Linux.

1. Creating the config file. The following areas should be added:
    1. Storage (required)
    2. Listener (required)
    3. Telemetry (optional)

    ```go
    storage "file" {
      path = "/path/to/vault/data" # path will be created if it doesn't exist!
    }

    listener "tcp" {
      address      = "0.0.0.0:8200"
      tls_disable  = 1 # shouldn't be disabled when running in production
    }
    ```

2. Starting the server: `vault server -config /path/to/config.hcl`
3. Initialize the Vault:
    1. Ensure `VAULT_ADDR` environment variable is set
    2. Verify vault operations by running `vault status`
    3. Run `vault operator init`
    4. Save the unseal keys and root tokens - they will disappear and be inaccessible after this!
4. Unseal the Vault: `vault operator unseal`
    1. Provide 1 of the 5 unseal keys provided
    2. Repeat two more times such that 3 of the 5 unseal keys have been provided.
5. You can test Vault operations by using e.g. `vault list auth/token/accessors`
    1. This will fail though, as Vault in Production mode by default does not set the root token as the token for usage.
    2. Login via root `vault login` and provide the root token
        1. Future requests will automatically use the token.
        2. The same will be applied for any other tokens created (so long as the user has sufficient permission!)

---

#### Verifying Storage Persistence

- As production mode persists storage, if Vault is shut down, the data isn't deleted.
- Upon restart of Vault, the process outlined previously must be followed to unseal the vault and verify data persistence.

- **Note:** THE UNSEAL KEYS SHOULD NOT BE STORED WITH ONLY 1 PERSON - THEY SHOULD BE DISTRIBUTED AMONGST TEAM MEMBERS

## 5.2 - Vault UI for Production

- By default, the Vault GUI is disabled for production. It can be enabled via the Vault config file however.
- All that is needed is adding the following to the config file:

```go
ui = true # boolean
```

- Note: For production environments, you may wish to update the private address of the server under `listener`.
- You can verify the system is listening to the desired address using `netstat -ntlp`
- Once the Vault is unsealed, ensure that the desired port for HashiCorp Vault is open - in this case `8200`, to allow the user to access the Vault UI.

- **Note:** When accessing the UI whilst the Vault is in a sealed state, users are able to provide the unseal keys to unseal the vault.

## 5.3 - Understanding Vault Agent

### Challenges

- For applications needing to interact with Vault, they must first authenticate to Vault and then use the tokens for their required tasks.
- Outside of this, logic related to token renewal, etc may be required with the application.
- Rather than building custom logic for the application(s), the Vault agent can be utilised.

### Vault Agent Overview

- A client daemon that automates the workflow of client login and token refresh.
- It automatically authenticates to Vault for supported auth methods.
- It ensures tokens are renewed by re-authenticating as required, until renewal is no longer allowed.
- Additionally, it is designed with robustness and fault-tolerance in mind.

The Vault agent works as follows:

1. Authenticates and acquires a token via the configured auth method
2. The token is written to the backend
3. The token is used to authenticate to Vault

### Running Vault Agent

- To use the Vault agent, the binary can be ran in "agent mode"
- To do so, run `vault agent config=<config file>`
  - The agent configuration file must specify the auth method and sink locations where the tokens are to be written.

### Working of Vault Agent

- When Vault is started in agent mode, it will attempt to get a Vault token via the auth method specified in the agent config file.
- Upon successful authentication, the token is written to the sink locations.
- Whenever the current token's value changes; the agent writes to the sinks.

### Vault Agent Example

- Various Auth methods are available, including AppRole, Azure, and AWS.
- Ensure the AppRole Auth method is enabled either via the CLI or UI
  - `vault auth enable approle`
- Create a policy for the agent. An example follows:

```go
path "auth/token/create" {
  capabilities = ["update"]
}
```

- Create an approle to use the policy defined above: `vault write auth/approle/role/<role name> token_policies="<policy name>"`
- Fetch the role ID: `vault read auth/approle/role/<role name>/role-id`
- Obtain the secret ID: `vault read auth/approle/role/<role name>/secret-id`
- Add the following code (example) at minimum to the agent config file (written in HCL):

```go
exit_after_auth = false
pid_file = "./pidfile"

auto_auth {
 method "approle" {
  mount_path = "auth/approle"
  config = {
    role_id_file_path = "/path/to/role-id" # files must exist!
    secret_id_file _path = "/path/to/secret-id" # files must exist!
    remove_secret_id_file_after_reading = false
  }
}

sink "file" {
 config = {
  path = "/path/to/token"
 }
}

vault {
 address = "http://127.0.0.1:8200
}
```

- Start the Vault in agent mode via `vault agent -config=/path/to/file.hcl`
  - Information provided regarding the sink file with the token
  - This can be looked up via `vault token lookup <token>`
- Now, any application wishing to use the token must fetch it from the sink file location. As an example, a Kubernetes secret could be based on this.

## 5.4 - Vault Agent Caching

### Primary Functionalities of Vault Agent

- Auto-Auth
  - Automatically authenticates to Vault and manages the token removal process
- Caching
  - Allows client-side caching of responses containing newly-created tokens.

### Overview of Caching

- Vault Caching follows a particular general process:

1. Application/Service requests a lease or token from Vault Agent
2. **Vault Agent Response: Upon Receiving the Request, Vault checks its Cache**
    1. If the requested lease or token is in cache, it is returned to the app/service
    2. If not found in the cache, a request is forwarded to Vault Server to obtain the lease or token
3. If step 2b occurred, Vault Server returns the requested lease or token
4. The returned lease or token is stored in the Agent Cache of the Vault client; then returned to the application or service for usage.

### In-Practice

- When looking to utilise the caching mechanism of the Vault agent, two particular areas must be added to the config:

```go
cache {
 use_auto_auth_token = true
}

listener "tcp" {
 address = "127.0.0.1:8007"
 tls_disable = true
}
```

- Starting the vault using the config: `vault agent -config=/path/to/config.hcl`
- Run a test command: `<token> vault token create`
  - No logs will appear in the agent logs as this request goes directly to the Vault Server
  - To resolve, `export VAULT_AGENT_ADDR=127.0.0.1:8007`
  - If the request is made again, the same token will be returned rather than a new one generated - this is because the original token was stored in the cache of the agent.
- In separate users, so long as they have the Vault Agent Address variable set, they will not require a token to run commands as the client token is used.

## 5.5 - Shamirs Secret for Unsealing Process

- Storage backend in Vault is considered to be untrusted.
- Any data stored is within the encrypted state.
- When vault is initialized, it generates an encryption key to protect all data stored within.
  - This key is then protected by a master key
- Vault then uses Shamir's secret sharing algorithm to split the master key into 5 separate shares, where any 3 of which can be used to reconstruct the master key.
  - This is why 3 keys must be used to unseal the vault.

### Notes

- The number of shares and minimum threshold required can both be specified.
- Shamirs technique can be disabled such that the master key can be used directly for unsealing.
- Once Vault receives the encryption key, it can decrypt the data in the storage backend and the Vault becomes unsealed

### Seal Stanza

- In the Vault server config file, the particular seal type can be configured if usage of Shamir's technique is not desired.

```go
seal [name] {
 # seal details
}
```

- This is optional configuration -  by default Shamir's algorithm will be used if not configured.
  - Most people tend to use this by default.
- Alternatives could include HSM or Cloud Key Management Solutions e.g. AWS KMS.

## 5.6 - Vault Auto-Unseal Overview

### Background

- During Vault Unseal process, users must enter they key(s) required.
- This allows each share of the master key to be stored separately for improved security.
- This can lead to issues:
  - If there are multiple Vault clusters in an organization, unsealing them can be a tiresome process heavily dependent upon the availability of users with the keys.
  - Unsealing makes the process of automating a Vault install difficult.
    - Automation tools can easily install, configure and start Vault, but unsealing it via Shamir's technique is heavily manual.
- To resolve these issues, Vault's Auto-Unseal mechanism can be utilised.

### Auto-Unseal Overview

- This delegates the responsibility of securing the unseal key from users to a trusted device or service.
- At startup, Vault will connect to the device or service implementing the seal, then request it decrypt the master key, such that Vault can read from storage.
- Cloud-based key(s) provides master key information → Provided master key used to access encryption key and decrypt.
- This provides pre-setup via the desired unseal method e.g.:
  - AWS KMS
  - Transit Secret Engine
  - Azure Key Vault
  - HSM
  - GCP Cloud KMS

## 5.7 - Auto-Unseal with AWS KMS

### Setting up AWS Auto-Unseal From Scratch

- As a prerequisite when implementing auto-unseal, you should have an understanding of the mechanism to be used.
- From Services → Key Management Service (KMS)
  - Create a symmetric key
  - Leave all settings as default (unless otherwise)
- Create an IAM user for authentication.
  - Provide sufficient permissions (Admin for demo purposes)
  - Note the access and secret keys associated with the IAM users.
    - Typically, one would export them as environment variables for security purposes.
- Add the following to the Vault Server Config file:

```go
seal "awskms" {
 region = "<region code>"
 access_key = "<access key>" # typically included as env variable instead
 secret_key = "<secret key>" # typically included as env variable instead
 kms_key_id = "<kms key id>"
 endpoint = "<KMS API endpoint>" # optional - typically used for private connactions over vpc from an EC2 instance
}
```

- Starting the Vault using this config: `vault server -config <config>.hcl`
- Upon first starting, an error/warning will be provided saying that no keys were found. Vault must be initialized to provide the master key and key shares.
  - `vault operator init`
  - Provides the root token and recovery keys
  - This will automatically unseal the vault.
  - The keys generated are automatically stored into the kms - they can now be called automatically for future usage of Vault.

## 5.8 - Vault Plugin Mechanism

- Plugins are the building blocks of Vault. All auth and secret backends are considered plugins.
- This allows Vault to extensible to suit user needs.
- This doesn't just apply to pre-existing plugins, custom plugins can also be developed.
- In general, to integrate a 3rd-party plugin, the following steps need to be done:
  - Create the plugin
  - Compile the plugin
  - Start Vault pointing towards where the plugin is stored.

### In Practice

- Install any desired packages e.g. go, git, etc. (Use Apt, Yum, etc as appropriate)
- Clone the code down for the plugin using GIT e.g. vault-guides/secrets/mock
- Compile the plugin using go: `go build -o /path/to/output/dir`
- Start Vault, pointing to the plugin directory: `vault server -dev -dev-root-token-id=root -dev-plugin-dir=/path/to/dir`
- Test the plugin functionality:
  - `export VAULT_ADDR="http://127.0.0.1:8200`
  - `vault login root`
  - `vault secrets enable my-mock-plugin`
  - `vault secrets list`
    - Verify the plugin is working and the secret path exists.
  - Read and Write operations to the plugin path:
    - `vault write my-mock-plugin/test message="Hello World"`
    - `vault read my-mock-plugin/test`

### Production

- In production, to use plugins, the following should be added to the config file: `plugin_directory = /path/to/directory"`

## 5.9 - Audit Devices

- Components in Vault that log requests and responses to Vault.
- As each operation is an API request/response - the audit log includes every authenticated interaction with Vault; including errors.
- By default, auditing is not enabled. It must be enabled by a root user using `vault audit enable`.

### Audit Devices Example

- To enable file audit: `vault audit enable file file_path=path/to/file.log`
- Audit mechanisms in place can be viewed by `vault audit list`
- Note: The audit log is by default in JSON format.
- Details logged include:
  - Client token used
  - Accessor
  - User
  - Policies involved
  - Token type.
- Note: Other options are available:
  - Syslog
  - Socket
- Enabling in Linux:
  - `vault audit enable -path="audit_path" file file_path=/var/log/vault-audit.log`
    - Audit log stored at /var/log
    - viewable via `cat <audit log> | jq`
- Note: The client token value is hashed - this can be computed via the endpoint `/sys/audit-hash`
  - Sample request:
    - `vault print token` - gets the original token in plaintext

        ```go
        curl --header "X-Vault-Token: <vault-token>" --request POST --data @audit.json http://127.0.0.1:8200/v1/sys/audit-hash/<path>
        ```

### Important Pointers

- If there are any audit devices enabled, Vault requires at least one to persist the logs before completing a request.
- If only one device is enabled and is blocking; Vault will be unresponsive until the audit device can write.
  - If more than one audit device is enabled in addition to the blocking one, Vault will be unaffected.

## 5.11 - Vault Enterprise Overview

- Includes a number of features benefitting organizational workflows.
- Features include:
  - Disaster Recovery
  - Namespaces
  - Monitoring
  - Multi-Factor Authentication
  - Auto-Unseal with HSM
- Once Vault Enterprise is acquired - instructions are provided for installation.
- In terms of appearance, there is little difference between Enterprise and Open-Source versions.

## 5.12 - Vault Namespaces

### Background Context

- In organizations, there are typically multiple teams wanting to use services such as Vault for their own particular purposes.
- In the case of Vault, they would need to manage their own secrets, auth methods, etc.
- To allow for this segregation and minimizing impacts teams may have on one another, Namespaces can be used.
- Each Vault namespace can have its own:
  - Policies
  - Auth Methods
  - Secrets Engines
  - Tokens
  - Identity entities and groups.

### Namespaces Example

- When logging into Vault, you can specify the namespace to log into if desired.
- Namespaces are created under `Access` in the Vault GUI.

## 5.13 - Vault Replication

- Having a single Vault cluster can impose various challenges, such as:
  - High latency
  - Connection issues
  - Availability loss
- It is therefore beneficial to have multiple clusters across different regions; allowing users in region 1 to manage their own secrets, etc. in their closer region.
- Replication serves to resolve this. There are multiple types available.

### Performance Replication

- Secondary regions keep track of their own tokens and leases, but share the same underlying configuration, policies, and supporting secrets (K/V values, encryption keys for transit, etc.) with the primary region.

### Disaster Recovery Replication

- Allows for a full restoration of all types of data (including local and cluster data)
  - Service tokens and leases are valid across both clusters.
- The secondary cluster does not handle any client requests, and can be promoted to the new primary in the event of disaster.

## 5.14 - Monitoring Telemetry in Vault

- Telemetry covers any data being output by a particular device.
- Analysis of this can be useful for areas such as:
  - Performance
  - Troubleshooting
- In Vault, there are two data sets to note:
  - Metrics - Output via Telegraf
  - Vault Audit Logs - Output via Fluentd
- These metrics can be output to various tools such as Prometheus.

### Metrics Output

- Further details for each metric are available in the documentation, however metrics covered include:
  - Policy-based
  - Token-based
  - Resource usage

### Configuration

- In the Vault Server config, one can add a config block to the file to point to a particular location for the metrics to be exported to.

```go
telemetry {
  statsite_address = "statsite.company.local:8125"
}
```

- Metrics can also be fetched from the `/sys/metrics` endpoint
  - Sample curl requests are available in the documentation
  - The format of the metrics can be configured e.g. JSON, Prometheus
  - e.g. `curl --header "X-Vault-Token: <token>" 127.0.0.8200:/v1/sys/metrics`
- Additional documentation is available for configuring Vault with various monitoring integrations; including Splunk.

## 5.15 - High-Availability Setup & Implementation in Vault

### Overview of HA

- In general, running a single instance of anything is risky. Vault is no exception.
- Vault supports a multi-server mode for High-Availability. This further protects organisations against outages by running multiple servers.
  - The data will be replicated across each based on the "leader".

- **Note:** High-Availability IS STORAGE BACKEND DEPENDENT - Integrated Storage is also available to support this.

- Out-of the box, Raft is available for use, an integrated storage backend.
- To configure:

```go
storage "raft" {
  path = "/path/to/raft/data" # defines where the data will be stored
  node_id = "raft_node_1"
}
cluster_addr = "http://127.0.0.1:8201"
```

### High Availability Example

- Start three separate instances of Vault with the above config: `vault server -config=/path/to/config.hcl`
- List the raft peers: `vault operator raft list-peers`
  - One will be noted as "leader" under state
- Run a test command in the leader node to store data:
`vault kv put secret/dbcreds admin=password`
- On one of the follower nodes, test access to the secrets: `vault kv get secret/dbcreds`
  - The secret data should be displayed.
- In the event that the leader node goes down, the data will still be accessible AND a new leader node will be assigned.

### Implementing Vault HA

- Raft Storage can be configured by adding the following to the config file:

```go
storage "raft" {
  path = "/path/to/raft/data" # defines where the data will be stored
  node_id = "raft_node_1"
}
cluster_addr = "http://127.0.0.1:8201"
```

- You are advised to set `disable_mlock` to true and disable memory swapping on the system.
- Start the server with `vault server -config=/path/to/config`
  - The vault will be shown to operational with Raft storage ready
- In a separate terminal, initialise the Vault:
  - `vault operator init -key-shares=<value> -key-threshold=<value> > key.txt`
- Unseal: `vault operator unseal <unseal key>`
- Login: `vault login <token>`
- Check the Raft nodes: `vault operator raft list-peers`
- Repeat for each node/vault server as required up until initialisations:
  - `export VAULT_ADDR='address'`
  - Join the node to the server `vault operator raft join <leader IP address>`
- To verify, put a secret to a particular path e.g.:
  - `vault secrets enable -path=secret kv`
  - `vault kv put secret/creds admin=password`
  - On another node: `vault kv get secret/creds` - should return the secret.
- Test the replication and leadership transfer by restarting the leader node and running `vault operator raft list-peers`

- To be highly available, one of the Vault server nodes grabs a lock within the data store.
- The successful server node becomes the "active" node - all others become standby nodes.
- At this point, if the standby nodes receive a request, they will either forward the request or redirect the client depending on the configuration.
- Nodes can be stepped down from active duty by using the `vault operator step-down <address>` command.

## 5.16 - Raft Storage - Snapshot and Restore

Snapshot and restore operations can be carried out via raft for the following commands:

`vault operator raft snapshot save <file>.snap`

`vault operator raft snapshot restore <file>.snap`
