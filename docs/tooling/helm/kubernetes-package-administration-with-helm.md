---
tags:
  - Tooling
  - Helm
---

# Kubernetes Package Administration with Helm

## 1.0 - Helm Installation and Configuration

### 1.1 - Helm Overview

- Helm: A package manager for Kubernetes.
- Used to define Kubernetes applications in charts.
- Using charts and Helm, one can:
  - Manage complexity
  - Easily update and rollback
  - Share Charts

- Helm v3 includes a number of changes:
  - Tiller removed, one would have to run helm init.
  - Helm search supports local repositories and against helm hub
  - Command overhaul, `helm init` is no longer required for example
  - Releases are scoped to namespaces
  - Chart API and Dependency Managers have been updated.

- Tiller was a server-side component with helm to help deployment. This meant it had extensive advanced permissions, which posed a huge security risk; its removal mitigates this risk.

#### Charts

- Charts are a collection of YAML files that would be typically used to deploy Kubernetes resources.
- By wrapping the desired YAML files e.g. those associated with an application, management and deployment is made significantly easier.

---

### 1.2 - Environment Setup

- Tools required:
  - VS Code
  - Docker
  - Kubernetes (can also use minikube, k3d, etc.)

---

### 1.3 - Installation

- Ensire all prerequisites are installed.
- Installation via any desired method:
  - From binary
  - Script Install
  - Package Managers (apt, chocolatey, homebrew, etc.)

---

### 1.4 - Configuration

- Common commands:
  - `helm version`
  - `helm repo add` - Adds a chart repository to the system
  - `helm search repo` - Search a repo for a desired chart version
  - `helm install` - Deploy all kubernetes objects defined in a particular chart, `--dry-run` flag is also available
  - `helm list` - Get list of any releases (installed charts)
  - Managing releases:
    - `helm upgrade`
    - `helm rollback`
    - `helm history`
  - Creating charts:
    - `helm create` - Creates a chart with default files and structure
    - `helm package` - Create a chart archive from a chart directory, which can be pushed to a repo

---

### 1.5 - Configuration Demo

- Add the stable repository: `helm repo add stable https://charts.helm.sh/stable`
- Verify addition: `helm repo list`
- Search the repo for a chart: `helm search repo <repo name>/chart name`
  - Example: `helm search repo stable/mysql`

## 2.0 - Exploring Helm Releases

### 2.1 - Deploying a Chart to Kubernetes

- Releases = Instance of a chart running in Kubernetes.
- Add a repo via `helm repo add <repo name> <repo link>`
- Search for the chart you want, using mysql as an example from the stable repo:
  `helm search repo <repo name>/<chart name>`
- Install the chart:
  `helm install <release name> <repo name>/<chart name>`
- By default, if no version is provided, the latest version will be used.

### 2.2 - Chart Deployment Demo

- To view chart information in the CLI, use `helm show`:
  `helm show chart stable/mysql`
- Displays information such as sources, keywords, apiVersion, appVersion, and a description of the chart.
- To view the README: `helm show readme <repo name>/<chart name>`
- For ease, the README can be piped to a file for viewing, append `> /path/to/README.txt` for example
  - Displays parameters such as prerequisites and image(s) used

- Chart install general command: `helm install <release name> <repo name>/<chart name>`
  - Append `--dry-run --debug` for a test run and verbose output.

- Verify release via `helm list`

### 2.3 - Retrieving Information on Helm Releases

- Once a release has been deployed, the state of the release can be inspected by `helm list`
- By default, `helm list` will only check in the default namespace
- For releases in other namespaces, use `--namespace <namespace>` or `--all-namespaces`
- To view the status of the objects, use standard `kubectl` commands.

### 2.4 - Helm Release Information Retrieval Demo

- `helm list` to check the release
- Check the status of a release `helm status <release name>`
  - Shows information such as chart version
- Manifest version `helm get manifest <release name> > <filename>`
  - Shows the kubectl manifest YAMLs of all objects created, supplied with default values
- For custom values used during release deployment: `helm get values <release name> > /path/to/file`
- Get the notes associated with a chart: `helm get notes <release name> > /path/to/file`
- To get everything: `helm get all <release name> > /path/to/file`
- Use `kubectl get all` to get all kubernetes resources

- View helm chart release history: `helm history <release name>`
  - Provides details around all versions of a release

- Uninstall release but keep history: `helm uninstall <release name> --keep-history`
- Re-running without the `--keep-history` flag will completely uninstall the chart.

### 2.5 - Upgrading a Release

- To view all versions of a chart: `helm search repo <repo name>/<chart name> --version`
- To install a specific version: `helm install <release name> <repo name>/<chart name> --version <version>`
- Use `helm status` and `kubectl` commands to verify deployment
- To upgrade a release, use `helm upgrade <release name> <repo name>/<chart name> --version <new version>`
  - New resources (where required) will then be created
- Use `helm list` to review the release information and `helm history` to show the changes between revisions.

### 2.6 - Release Upgrade Demo

- Search for the repo `helm search repo <repo name>/<chart name>`
- Get all versions of the chart `helm search repo <repo name>/<chart name> --versions`
- Deploy the desired chart version: `helm install <release name> <repo name>/<chart name> --version <version>`
- Verify deployment with `helm list`
- Check the kubernetes objects `kubectl get all` (or appropriate e.g. use `--namespace`)
- Upgrade the release helm upgrade `<release name> <repo name>/<chart name> --version <new version>`
- Verify upgrade with `helm list`
- View the history of the release `helm history <release name>`

### 2.7 - Rolling Back a Release

- In the event of a rollback, use `helm rollback <release name> <revision number>`
- Use `helm list` and `kubectl` commands to verify deployment again

### 2.9 - Exploring a Chart

- To pull down a chart from a remote repository and view the files: `helm pull <repo>/<chart name> --untar`
- Charts by default contain the following:
  - Chart.yaml - Contains chart description
  - Values.yaml - Contains default values for the chart if not provided
  - Charts folder - Contains other charts that the main chart is dependent upon
  - Templates folder - Contains the primary YAML files used to generate Kubernetes Manifests

- Under templates folder, the manifests used to create Kubernetes objects e.g. deployments, services, etc.
  - `_helpers.tpl` - Used for supporting functions to be referenced by YAML files in the template directories
  - Notes.txt - Contains help text for the charts.

- Template YAMLs use Jinja templating to pass through variables / values set for the Helm chart, such as:
  - `name: {{ .Release.name }}-deployment`
  - `image: {{ .Values.containerImage }}`

- Values can be changed at runtime e.g. you may have specific values for Development and Production environments.

## 3.0 - Configuring Helm Repositories

### 3.1 - Repository Overview

- Chart repository = Any HTTP server that can serve YAML or TAR files. Needs to be able to respond to GET requests.
- Contains an index.yaml file and packaged charts.
- Helm charts are commonly stored in the Helm hub at <https://hub.helm.sh>
- Helm charts can then be stored and managed within the UI.

### 3.2 - Packaging a Helm Chart

- To create a chart: `helm create <chart name>`
- Initializes a chart folder with the default files and structure.
- Default files included:
  - Templates folder:
    - tests folder: To store any tests defined to verify chart functionality
    - _helpers.tpl - Used to define supporting functions for template YAMLs.
    - Example YAML files for Kubernetes resources - deployment, ingress, service account.
    - Notes.txt - Contains chart deployment information e.g. "how to get started with it"

- Add the desired YAML files required for the chart under Templates.

- Install the chart: `helm install <chart name> /path/to/chart`
- Verify deployment with `helm list` and `kubectl` commands as required.
- Packaging the chart: `helm package <path to chart> --destination <path to local charts folder>`

### 3.3 - Packaging a Helm Chart Demo

- Create a chart: `helm create <chart name>`
- Check and make whatever edits are necessary to the chart folder in `./<chart name>` e.g. remove the default YAML folders.
  - Add content to the Notes.txt file under `templates` directory
- Deploy the chart: `helm install <release name> /path/to/chart`
- Verify with `helm list` and `kubectl` commands
- Delete the release: `helm delete <release name>`
- If required, update the Jinja template directives e.g. `{{ .Release.Name }}` or `{{ .Values.containerImage }}`
- Redeploy if required using the commands defined above.
- Use more detailed commands to verify customised values are set accordingly e.g. `-o jsonpath=<path to metadata>`
- To override a value defined in values.yaml, use `--set <value key>=<new value>`.
- Package the chart: `helm package <path to chart> <output path>`

### 3.4 - Creating a Local Helm Repository

- Chart museum - an open-source, cross-platform helm chart repository that supports multiple cloud backends and local usage
- Chart museum itself can be ran as a helm chart.
- Deployment: `helm install chartmuseum stable/chartmuseum --set env.open.DISABLE_API=false`
  - DISABLE_API allows pushing of chart repository.
- To connect, port-forwarding is required:
   `kubectl port-forward $POD_NAME 8080:8080 --namespace default`
  - Pod name can be obtained by
     `$POD_NAME=$(kubectl get pods -l "app=chartmuseum" -o jsonpath="{.items[0].metadata.name}")`

- Add chart museum repository:
  `helm repo add chartmuseum http://127.0.0.1:8080`

- Push to chart to chart museum:
    `curl --data-binary "@<chart tar name>" http://localhost:8080/api/charts`

- Searching chart museum:
  - Run `helm repo update` to update the chart-museum repository to recognize the pushed chart.

- Verify update with `helm search repo chartmuseum/<chart name>`

### 3.6 - Creating a Remote Helm Repository

- A Helm Repository can be any server that can serve YAML and TAR files, as well as responding to get requests.
- Options available include Chart Museum, Github, JFrog Artifactory

#### 3.6.1 - Example: Github Repository

- Create a repository in Github via standard means and clone locally.
- Copy in the packaged chart (the .tgz file created via helm package)
- In the repo, run `helm repo index` - creates index.yaml, the file referenced by `helm search`
- Stage, commit, then push to the repository.
- Add Github repository as a local Helm repository:
  - Copy the RAW URL of the index.yaml file (minus the index.yaml)
  - Run `helm repo add <repo name> <RAW URL>`
- Search for the repo: `helm search repo <repo name>/<chart name>`
  - The index.yaml has been cached locally and is getting picked up by `helm search`.
