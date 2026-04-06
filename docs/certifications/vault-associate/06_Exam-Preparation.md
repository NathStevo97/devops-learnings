# 6.0 - Exam Preparation

## 6.1 - Important Pointers for the Exam

### Official Certification Guide

[https://developer.hashicorp.com/vault/tutorials/associate-cert](https://developer.hashicorp.com/vault/tutorials/associate-cert)

### Dynamic Secrets

- Dynamic secrets allow on-demand credential generation dynamically. They are automatically revoked after a particular amount of time (lease).
- Not all secrets engines support dynamic credentials. Primary engines that can utilise it include:
  - AWS
  - Database
  - Google Cloud
  - Azure
- Dynamic secrets do not provide any stroger cryptographic key generation.

### Lease Management

- With every dynamic secret and service type authentication token, Vault will create a lease.
  - Lease - Metadata containing information regarding a secret or service type authentication. Contains information such as time duration, renewability, etc.
- Once the lease expires, Vault can automatically revoke the data, preventing future access.
- When working with Leases, Vault has two main operations that can be achieved via the CLI or UI:
  - Renew - renews the lease on a secret, extending its usage time before automatic revocation
  - Revoke - Force-invalidates a secret with immediate effect, preventing any further renewals.
- Example commands:
- `vault lease renew -increment=3600 <lease id>` - Requests an adjustment of a lease's TTL to 1 hour
- `vault lease revoke <lease id>` - Revokes a lease
- `vault lease revoke -prefix aws/` - Revokes all secrets under the path aws

### Transit Secret Engine

- Handles cryptographic functions on data in-transit.
- All plaintext data must be base64-encoded.
- This is because Vault does not require that the plaintext is "text" it could be a binary file, such as a PDF or image.
- Encryption keys can be rotated at regular intervals to ensure that not all data is encrypted with one static encryption key.

#### Key Version

- Transit engine supports versioning of keys
- Key versions earlier than a key's specified `min_decryption_version` will be archived. Any later belong to the working set.
  - This facilitates enhanced performance and security.
- By disallowing decryption of old versions, any found ciphertext associated with obsolete data cannot be decrypted. The only way that this could be achieved would be if `min_decryption_version` was manually lowered.

---

### Vault Policies

- Used to govern access to Vault for users and roles (authorization)
- When first initialized, the root and default policies are created by default.
- Policies operate on a "deny by default" manner, so an empty policy grants no permissions

#### Default Policy

- A built-in policy that cannot be removed.
- Attached to all tokens by default, but may be explicitly be excluded at token creation time by particular authentication methods.
- Covers basic functionality such as the ability for a token to look up data about itself and use its cubbyhole data.
- Vault is not prescriptive about its contents - it can be modified to suit.

#### Root Policy

- A root user can do ANYTHING within Vault. Therefore, it is highly recommended that any root tokens are revoked before running Vault in production.
- When a Vault server is first initialized, one root user always exists. This user is primarily used to do the initial configuration and setup of Vault.
- After configuration, the initial root token should be revoked and more strictly controlled users and authentication should be used.
  - E.g. have an administrator user as the primary usage point.

### Token Accessor

- The accessor is a value that acts as a reference to a token - used to perform limited actions such as:
  - Lookup a token's properties
  - Lookup a tokens capabilities for a particular path
  - Renew and revoke the token

### Policy Association

- During token creation, a policy will be associated with the token.
- If a new policy is attached to a user or role, it will not affect the existing tokens. New tokens must be created.
- For any policies that are updated and attached to a token, the rules will be reflected accordingly as part of the token's permission.

### Token Capabilities

- To check a token's capabilities for a particular path, use the following sample command:
`vault token capabilities secret`
- Note: the same operation can be achieved using token accessor.

### Authentication Methods

- There are multiple authentication methods available
- Upon successful authentication, a token will be generated for the user to interact with Vault.
- Note: GitHub auth method is user-oriented and easiest to use for developer machines.
- For servers/applications, AppRole is recommended.
- To enable an authentication method, utilise the following example command for userpass method:
`vault auth enable -path=my-login userpass`
- To disable an auth method: `vault auth disable <method name>`
  - This will auto-logout any users logged in via that method.

---

### Storage Backend

- Multiple storage backends are available for Vault depending on the use cases
- The backend determines the location for storage of Vault information and data.
- Note: not all storage backends support high-availability. Typically this is cloud-only.

### Disabling a Secrets Engine

- To disable a secrets engine at a particular path: `vault secrets disable <path prefix>`
- Once disabled, any secrets associated are immediately revoked.

### UserPass Auth Method

- Login achievable via `vault login -method=userpass username=user`
- Passwords should not be used directly in the CLI - it will auto hide it if not included.

### Vault Unseal

- Vault starts in a sealed state any time it is started
- Unsealing involves constructing the master key necessary to read the decryption key to decrypt the data; allowing access to Vault.

### Vault Agent

- The agent doesn't persist anything to storage - all data is stored in memory
- The agent looks to utilise two main functionalities:
  - **Auto-Auth:** Facilitates automatic authentication to Vault and management of token renewal processes
  - **Caching**: Allows client-side caching of responses containing newly-created tokens.
    - If configured with `use_auto_auth_token`, clients will not be required to provide a Vault token to the requests made to the agent.

### Response Wrapping Token

- When response wrapping is requested, Vault creates a temporary single-use token (Wrapping Token) and the response is inserted into the token's cubbyhole with a short TTL
- If the wrapping token is compromised, the application will not be able to access the secret, and security actions can be taken accordingly.

---

### Shamir Secret Sharing for Unsealing Vault

- Vault considers all storage backends untrusted by default. Vault therefore uses an encryption key to protect all data; which is then protected by a master key.
- Vault utilises Shamirs secret sharing algorithm to split the master key into 5 shares. Any 3 of the 5 shares are required to reconstruct the master key.
- In terms of best practices - the key shares that need to be entered should be done from different workstations by different users; each with their own individual keys.

### Seal Stanza

- The seal stanza configures the seal type used for additional data protection e.g. HSM or Cloud-based KMS solutions to encrypt and decrypt the master key.
- This is OPTIONAL. In the case of the master key, Vault will by default use the Shamir algorithm to cryptographically split the master key if not provided.

### Vault Replication

- For performance replication - secondary clusters will service reads locally
  - Some data is also stored locally and not replicated from the primary cluster
- For DR Replication - ALL data is replicated, but the secondary cluster cannot accept client requests.

### Entities and Aliases

- Each client is internally termed as an entity - entities can have multiple aliases.
- Policies defined at entity-level will be associated with all aliases associated with the entities.
  - E.g. users under the  "dev team" entity

### Identity Groups

- A group can contain multiple entities as its members
- Any policies applied to a group will be applied to all entities within the group.

### Vault Output

- Vault data output can be configured for a variety of output formats, including:
  - Table
  - JSON
  - YAML
- Table is the default output format.
- Output can be specified when running vault commands e.g. `vault secrets list -format table`

### Multiple Encryption Keys

- For transit engine - it is good practice to regularly rotate the encryption key
- This limits the number of data encrypted via a single key
- All data should NEVER be encrypted via a single encryption key - this is heavily risky

### Reading Output from KV Path

- Suppose you want to read a secret at a particular path, what capability is needed?
  - LIST - Allows for listing values at the particular paths
  - READ - Allows reading of data at a particular path

### Audit

- Audit devices are the components in Vault that keep a log of all requests and response to Vault
- When Vault servers are first initialized, no auditing is enabled
- Any audit devices must be enabled by a root user using `vault audit enable`

### Vault Browser CLI

- Allows the running of basic CLI commands e.g read/write/delete/list
- More advanced tasks e.g creating new authentication methods are not available via this.

### Vault Token Lookup

- Via the `vault token lookup <command>`, the following parameters are output:
  - Creation_TTL - How long is the token valid for upon first creation?
  - Orphan - True/False - Does the token have a parent token?
  - TTL - How long is the token valid for at the moment in time?

### Orphan Tokens

- Orphan tokens aren't the children of their parents - they therefore do not expire when their "parent" does.
- They are the root of their own token tree
- Orphan tokens still expire when their own max TTL is reached.

### Create Token with Explicit TTL

- TTL = Initial TTL to associate with the token
- Explicit Max TTL = Maximum lifetime for the token - a hard limit that cannot be exceeded
- The systems max TTL is 32 days by default, but this can be adjusted in the Vault config file
- To create a token with an explicit TTL, use the following example command: `vault token create --ttl=<time> --explicit-max-ttl=<time>`

### Renewing a Token

- `vault token renew` is used to extend the validity of a renewable token
- `vault token renew -increment=<time> <token>`

### Basic Environment Variables

- VAULT_ADDR defines the Vault server's address and port e.g. [https://127.0.0.1:8200](https://127.0.0.1:8200)

### GUI Related Questions

- Should need to understand how to do particular actions within the GUI e.g. delete a particular version of a secret.

### Secrets Engines

- Multiple secrets engine of the same type can be enabled ata given time
- They can be distinguished uniquely be separating them via path
  - Example:
    - Key-Value engine at /secret
    - Key-value engine at /kv

---

### Supported Backend - HashiCorp Support

- The following backends are officially supported by HashiCorp:
  - In-Memory
  - Filesystem
  - Consul
  - Raft
- Technical support is available from HashiCorp community and technical team.

### Vault Enterprise Features

- Vault Enterprise includes features to utilise particular workflows such as:
  - Disaster recovery
  - Namespaces
  - Monitoring
  - Multi-Factor Authentication
  - Auto-unseal with HSM

### Vault Namespace

- Namespaces are isolated environments that act as "vaults within Vault"
- Each namespace has separate login paths and supports creating and managing data isolated to their namespace
- Each namespace can have its own:
  - Policies
  - Authentication methods
  - Secrets engines
  - tokens
  - identify entities and groups

### Vault Replication 2

- When replication is enabled, all of the secondary clusters existing data will be destroyed
- Vault does not support an automatic failover/promotion of a DR secondary cluster
- Vault replication is an Enterprise-only feature
- DR replicated clusters will replicate all data from the primary cluster, including tokens.
- Performance-replicated clusters will not replicated tokens from the primary

### Auto-Completion Feature

- Allows automatic completion for flags, subcommands and arguments
- Note: Requires shell restart after install
- Installation via: `vault -autocomplete-install`

### Vault CLI Commands

| Use Case | Example Command |
| --- | --- |
| Enable Secrets Engine | vault secrets enable kv-2 |
| Store Data | vault kv put secret/my-secret admin=password |
| List Key Names in Secrets | vault kv list secret/my-app/ |
| Delete Version of Secret | vault kv delete secret/my-app/ |
| Delete all version & metadata | vault kv metadata delete secret/my-app/ |

### Auto-Unseal

- Auto unseal delegates the responsibility of securing the unseal key from users to a trusted device or service
- Following are some of the supported services:
  - AWS KMS
  - Transit Secret Engine
  - Azure Key Vault
  - HSM
  - GCP Cloud KMS
- For private connectivity, VPC endpoints can be used

### Identify Output of Transit Engine

- `vault write encryption/encrypt/demo plaintext=$(base64 <<< "Sample Data")`
- Output: `vault:v3<stuff>`
- V3 Indicates the key version used to encrypt the plain text
- Name of the keyring is demo
- Transit secret engine is mounted at `/encryption`

### PKI Secrets Engine

- Allows generation of dynamic X509 certificates
- Benefits include:
  - Allows vault to act as an intermediate Certificate Authority
  - Reduces or eliminates the amount of certificate revocations required

### TOTP Secrets Engine

- TOTP = Time-based one-time passwords
- These are temporary passcodes and typically expires after 30, 60, 120 seconds etc
- The TOTP secrets engine can act as both a generator (e.g. Google Authenticator) and a providr (e.g. google sign-on)
- To view: `vault read totp/code/zeal`

### Vault Plugins

- All Vault Auth and secret backends are plugins
- This allows for easier customisation and extensability of Vault

### Telemetry in Vault

- All telemetry related metrics are available at `/sys/metrics` endpoint
- The primary metrics analysed are:
  - Metrics
  - Vault Audit Logs

### Security Best Practices - Root Tokens

- It's best practice to not persist root tokens
- Root tokens should be generated using vault's `operator generate-root` command only when absolutely necessary
- For day-to-day operations, the root token should be deleted after configuring other auth methods or configuration settings etc

### Enabling Versioning in KV - Version 1

- When enabling Key-Value secret engine version 1, the versioning feature is not enabled by default.
- Versioning can be enabled by using the `kv enable-versioning` for an existing non-versioned key/value secrets engine at its path.

### Response Wrapping from UI

- The feature under Vault Tools → Wrap allows response wrapping functionality

---

### Path Templating

- Allows variable replacement based on information of the entity.
- Example entity policy:

```go
path "secret/data/{{identity.entity.name}}/" {
  capabilities = ["create", "update"]
}
```

- Example alias policy based on entity policy with path templating:

```go
path "secret/data/alice/" {
  capabilities = ["create", "update"]
}
```

### Service Tokens vs Batch Tokens

| Feature | Service Token | Batch Token |
| --- | --- | --- |
| Can be root tokens | Yes | No |
| Can create child tokens | Yes | No |
| Renewable | Yes | No |
| Periodic | Yes | No |
| Can have particular max TTL | Yes | No (fixed TTL always) |
| Has Accessors | Yes | No |
| Has CubbyHole | Yes | No |
| Revoked with Parent if not orphan | Yes | Stops Working |
| Dynamic Secrets Lease Assignment | Self | Parent (if not orphan) |
| Can be used across performance replication clusters | No | Yes (if orphan) |
| Creation scales with performance standby node count | No | Yes |
| Cost | Heavy Weight - Multiple Storage Writes per token creation | Lightweight - No storage cost for token creation |

- Key points to note are:
  - Can be root tokens
  - Cost

### Vault Tools

- Vault contains certain tools for particular functions at the `/sys/tools` endpoint

| Endpoints | Description |
| --- | --- |
| /sys/tools/random/164 | Generate a random 164-byte value |
| /sys/tools/hash/sha2-512 | Hash some input data using SHA2 algorithm |

### Miscellaneous Pointers

- Root and Default are two default policies available in Vault.
- When a lease is revoked, it invalidates that secret immediately, preventing further renewals
- To remove all secrets under a particular path: `vault lease revoke -prefix <path>`
- Userpass auth method cannot read usernames and passwords from an external source
- The `/sys/leader` endpoint is used to check HA status and current leader of vault
- `vault operator init` initializes a vault server
- Vault config files can be used to configure various settings e.g.:
  - Cluster name
  - Storage backends
  - seal settings
- Configuration for setup like namespaces and auth methods are handled directly within Vault itself.
- Identity secrets engine is mounted by default in Vault
- Storage backends are not trusted by default in Vault.
- Port Numbers:
  - 8200 - Vault API and UI
  - 8201 - Cluster-cluster communication
- Root tokens in Vault are not associated with TTLs - non-root tokens are
- The default max TTL is 32 days for tokens, but this can be modified.
- Transit secret engine stores no data
- VAULT_ADDR needs to be set to allow for any commands to be ran.
  - Post-authentication,  the CLI and UI automatically assumes the token used in authentication for subsequent requests.
  - For the API, the token must be provided for all subsequent requests.
- Vault Secrets engines supports multiple cloud providers e.g. AWS, Azure, GCP
- Cubbyhole is a default secrets engine enabled for all users.
- When generating dynamic secrets, Vault returns the `lease_id`
  - This can be used with commands for lease renew, revoke, etc
- Vault login command is used for CLI authentication
- After initializing, Vault provides the root token to the user. This is the only way to login to Vault to configure additional auth methods
  - `+` and `*` are associated with wildcard path in policies.
- Config files for Vault can be done in either JSON or HCL.
- When data is decrypted via the transit engine, the output is base64 format
  - To get the original data, it must be decoded via base64
- Vault UI needs to be enabled from the configuration file ONLY and not the CLI
- For token renewal, `vault token renew <token>` can be utilised to extend the TTL.
- When the Vault is sealed, users can only:
  - View the vault status
  - Attempt to unseal the Vault
- If the Vault CLI can access a specific path but a user cannot access it via the GUI, the issue is that the user is missing the LIST capability against that path.
- If a secret has been manually removed, `vault lease revoke` will result in an error (which can be avoided by appending the `-force` flag.
- Storage backend and HTTP API are outside of the security barrier and cannot be pretected
- WAL = Write-Ahead Logging
  - Changes are first recorded in the log (which has to be written to stable storage) before changes are written/applied to any data stores.
  - This is commonly noted in HA setups.

---

### Dealing with Large Data Sizes - Transit Engine

- When data size is large, it is not advised to send it over the network to the Vault
- Via Vault, one can generate a data key, encrypt the data locally, and use it to decrypt the data when required.

### Vault Policy Rules - Transit Engine

- Common / Sample Rules associated with the Transit engine are:

```go
## encrypt particular key
path "transit/encrypt/demo-key" {
  capabiltities = [ "update" ]
}

## decrypt particular key
path "transit/decrypt/demo-key" {
  capabiltities = [ "update" ]
}

## list values under /tranist/keys
path "transit/keys" {
  capabiltities = [ "list" ]
}

#view values associated with particular keys
path "transit/keys/demo-key" {
  capabiltities = [ "read" ]
}
```

### Key Rotation in Vault

- It's ill-advised to encrypt all data with one encryption key
- Transit engine allows encryption key rotation.
- Vault maintains the versioned "keyring" and the operator can configure the minimum allowed version for decryption tasks

### Periodic Tokens

- Never expire so long as they're renewed
- Aside from root tokens, these are the only way for unlimited lifetime tokens to exist in Vault
- Created via `vault token create -period=<time> -policy=<policy>`

### Vault HA

- Vault supports multi-server mode for High-Availability.
- This protects against outages by running multiple Vault servers.
- Vault servers/nodes can be force-removed from active duty using `vault operator step-down` whilst within the server.
- When utilising HA, Consul and Integrated Storage (Raft) are advised for use as storage backends.

### Guide in Vault GUI

- Note that Vault's GUI provides guidance for various operations e.g. restart, secrets, authentication, etc.
- It will provide links to the related documentation involved e.g. auth method documentation.

### Vault Policy Format

- HCL Policy files can be auto-formatted by `vault policy fmt <filename>.hcl`

### Misc Pointers

- Kubernetes authentication is required for any kubernetes-based workloads
- For kubernetes-based authentication, passing JWT token is required for all API requests.
- `/sys/seal` endpoints are used to seal the Vault. It requires a token with root policy or sudo capability on the path.
- For EC2-based workloads, AWS Authentication method can be used.
  - It is not mandatory, AppRole can also be used.
