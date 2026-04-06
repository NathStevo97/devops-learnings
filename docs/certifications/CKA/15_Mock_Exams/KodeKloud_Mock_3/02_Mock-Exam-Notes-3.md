# 15.2 - Mock Exam 3

## PVViewer

- `kubectl create serviceaccount`
- `kubectl create clusterrole -<name> --resource=persistentvolumes --verb=list`
- `kubectl create clusterrolebinding pvviewer-role-binding --clusterrole=<clusterrole> --serviceaccount=namespace.serviceaccount`

## Multi-Pod

- `Name: name`
- `Value: alpha/beta`
- `Beta command = sleep 4800`

## Kubeconfig

- Run `kubectl cluster-info --kubeconfig=/path/to/file`
- Analyse output
- Edit API Server port to 6443

## Replicas

- Edit kube-controller yaml file and edit typos
