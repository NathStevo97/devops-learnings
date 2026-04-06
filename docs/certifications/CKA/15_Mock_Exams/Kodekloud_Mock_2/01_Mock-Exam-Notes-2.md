# 15.1 - Mock Exam 02

## ETCD Backup

- Best bet is to use the Kubernetes [Documentation](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#snapshot-using-etcdctl-options)
- Check the version: `ETCDCTL_API=3 etcdctl version`
- Navigate to `/etc/kubernetes/manifests`
- Check the etcd YAML and find the following values or paths to be used in the command:
  - Endpoints
  - Cacert
  - Cert
  - Key

- Run the command: `ETCDCTL_API=3 etcdctl --endpoints=<> --cacert=<> --cert=<> --key=<> snapshot save <filepath to backup>`

## Use-PV Question

- Create a PersistentVolumeClaim
  - 10Mi
  - Ensure correct access mode
  - No storage class needs to be specified
  - Specify the PVC and VolumeMount as required

## Record Annotations

- `kubectl run <parameters> --record`
- `kubectl set image <parameters> --record`
- Use `kubectl rollout history` and `kubectl rollout status` where appropriate.

## Certificate Signing Request (CSR)

- Use manage TLS certificates task in Kubernetes [documentation](https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/)
- Creatue using spec provided in YAML file
- Encode `.csr` file in base64 as appropriate
- Create the CSR
- Approve the CSR
- Create role with appropriate spec via `kubectl create` - separate the verbs with commas
- Create rolebinding -> developer-role-binding --role=developer --user=john --namespace=developer via `kubectl create`
- Check permissions with `kubectl auth can-i` with appropriate options

## Nginx-Resolver

- Use port 80
- Type=ClusterIP
- Test DNS Lookup with Busybox Pod: `--rm -it --nslookup <service>`
- Record as appropriate
- `kubectl expose pod nginx-resolver --port=80 --target-port=80`
- `kubectl describe svc` -> get IP and endpoing
- `kubectl run test nslookup --image=busybox:1.28 --rm -it -- nslookup nginx-resolver-service > /root/nginx.svc`
- `kubectl run test-nslookup --image=busybox:1.28 --rm-it -- nslookup <pod IP address> > filepath`
