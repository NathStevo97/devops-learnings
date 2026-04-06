# 10.3 - Mock Exam 3

## Q1

A kube-bench report is available at the Kube-bench assessment report tab. Fix the tests with FAIL status for 4 Worker Node Security Configuration .
Make changes to the `/var/lib/kubelet/config.yaml`

After you have fixed the issues, you can update the published report in the Kube-bench assessment report tab by running `/root/publish_kubebench.sh` to validate results.

## Q2

Enable auditing in this kubernetes cluster. Create a new policy file that will only log events based on the below specifications:

- Namespace: `prod`
- Level: `metadata`
- Operations: `delete`
- Resources: `secrets`
- Log Path: `/var/log/prod-secrets.log`
- Audit file location: `/etc/kubernetes/prod-audit.yaml`
- Maximum days to keep the logs: 30

Once the policy is created it, enable and make sure that it works.

## Q3

Enable PodSecurityPolicy in the Kubernetes API server.

Create a PSP with below conditions:

1. PSP name : `pod-psp`
2. Privilege to run as root on host: `false`
3. Allowed volumes to mount on pod: configMap,secret,emptyDir,hostPath
4. seLinux, runAsUser, supplementalGroups, fsGroup: RunAsAny

Fix the pod definition `/root/pod.yaml` based on this PSP and deploy the pod. Ensure that the pod is running after applying the above pod security policy.

## Q4

We have a pod definition template `/root/kubesec-pod.yaml` on
controlplane host. Scan this template using the kubesec tool and you will
notice some failures.

Fix the failures in this file and save the success report in
`/root/kubesec_success_report.json`.

Make sure that the final kubesec scan status is passed.

## Q5

In the dev namespace create below resources:

- A role `dev-write` with access to `get`, `watch`, `list` and `create` pods in the same namespace.
- A Service account called `developer` and then bind `dev-write` role to it with a rolebinding called `dev-write-binding`.
- Finally, create a pod using the template `/root/dev-pod.yaml`. The pod Wshould run with the service account developer. Update `/root/dev-pod.yaml` as necessary

## Q6

Try to create a pod using the template defined in `/root/beta-pod.yaml` in the namespace `beta`. This should result in a failure.

Troubleshoot and fix the OPA validation issue while creating the pod.

You can update `/root/beta-pod.yaml` as necessary.

The Rego configuration map for OPA is in untrusted-registry under `opa` namespace.

NOTE: In the end pod need not to be successfully running but make sure that it passed the OPA validation and gets created.

## Q7

We want to deploy an ImagePolicyWebhook admission controller to secure the deployments in our cluster.

Fix the error in `/etc/kubernetes/pki/admission_configuration.yaml` which will be used by ImagePolicyWebhook

Make sure that the policy is set to implicit deny. If the webhook service is not reachable, the configuration file should automatically reject all the images.

Enable the plugin on API server.

The kubeconfig file for already created imagepolicywebhook resources is under `/etc/kubernetes/pki/admission_kube_config.yaml`

## Q8

Delete pods from alpha namespace which are not immutable.

**Note:** Any pod which uses elevated privileges and can store state inside the container is considered to be non-immutable.
