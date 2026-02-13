# Envoy Gateway test

A way to test the [Envoy Gateway](https://gateway.envoyproxy.io/) controller completely locally.
Uses a [KinD Kubernetes cluster](https://kind.sigs.k8s.io/), [cloud-provider-kind](https://github.com/kubernetes-sigs/cloud-provider-kind) for creating local `LoadBalancer` services, and [a few stdlib-only Python servers](apps/).

## Pre-reqs

No matter how you install the other dependencies, you need these already installed on your machine:

* Docker
* `curl`

If you want to automatically use compatible verisons of dependencies and manage the `cloud-provider-kind` daemon, you need these installed:

* [mise](https://mise.jdx.dev/) for dependency installation and isolation
* [pitchform](https://pitchfork.jdx.dev/) for daemon management

If you don't want to use those tools, make sure you have installed the tools and version in [mise.lock](mise.lock).
Any time this README says to run `mise run whatever`, you can find the matching script in the [mise-tasks](mise-tasks) directory.

## Starting all the things

```console
$ mise run start
```

This will create a KinD cluster with one node that mounds the [apps directory](apps/) onto that node so that it can be accessed by pods via `hostPath` volumes.
It will write the config to a local kube config file in `.config` so that it won't step on the toes of any other Kubernetes cluster config that you're using.
The [mise config](mise.toml) in this repo sets the `KUBECONFIG` env var to point to this file so, if you're using mise, any `kubectl` commands run in this directory will run against this KinD cluster.
It will also start the `cloud-prodider-kind` daemon so that LoadBalancer services can be exposed locally.


## Stopping all the things

```console
$ mise run stop
```

## Refreshing all the things

Run this when you change the server code or the Kubernetes resources.
This will apply any changes to the Kubernetes resources and restart the app and auth server deployments.

```console
$ mise run refresh
```
