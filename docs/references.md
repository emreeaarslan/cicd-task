# References

Projeyi geliştirirken kullandığım temel dokümantasyonlar aşağıdadır. Mümkün olduğunca kullandığım araçların resmi kaynaklarını referans aldım.

## Flask

### Flask Quickstart

https://flask.palletsprojects.com/en/stable/quickstart/

Backend ve frontend Flask servislerinin oluşturulması, route tanımları ve temel uygulama yapısı için kullandım.

### Flask Testing

https://flask.palletsprojects.com/en/stable/testing/

Flask `test_client()` kullanımı ve endpoint testlerini hazırlarken kullandım.

## pytest

### Getting Started

https://docs.pytest.org/en/stable/getting-started.html

Backend ve frontend testlerinin yazılması ve `pytest` ile çalıştırılması için kullandım.

## Python Mock

### unittest.mock

https://docs.python.org/3/library/unittest.mock.html

Frontend testinde gerçek backend servisini çalıştırmadan backend HTTP cevabını mocklamak için kullandım.

## Requests

### Requests Quickstart

https://requests.readthedocs.io/en/stable/user/quickstart/

Frontend servisinden backend API'ye HTTP isteği gönderme, response okuma ve timeout kullanımı için kullandım.

## Docker

### Dockerfile Reference

https://docs.docker.com/reference/dockerfile/

Backend ve frontend Dockerfile'larını hazırlarken kullandım.

### Build Context

https://docs.docker.com/build/concepts/context/

Docker build context ve `.dockerignore` dosyalarını düzenlerken kullandım.

### Docker Compose Networking

https://docs.docker.com/compose/how-tos/networking/

Frontend'in Docker Compose ortamında backend servisine `backend` servis adı üzerinden ulaşması için kullandım.

### Multi-platform Builds

https://docs.docker.com/build/building/multi-platform/

AMD64 ve ARM64 image'ların aynı image tag'i altında nasıl oluşturulduğunu anlamak için kullandım.

### Multi-platform Images with GitHub Actions

https://docs.docker.com/build/ci/github-actions/multi-platform/

GitHub Actions pipeline'ına QEMU, Docker Buildx ve `linux/amd64,linux/arm64` platform desteğini eklerken kullandım.

## GitHub Actions

### Workflow Syntax

https://docs.github.com/actions/reference/workflows-and-actions/workflow-syntax

Branch, pull request ve tag trigger'ları; job yapısı; `needs`, `if` ve permission ayarları için kullandım.

### Building and Testing Python

https://docs.github.com/actions/automating-builds-and-tests/building-and-testing-python

GitHub Actions üzerinde Python kurulumu, dependency installation ve pytest çalıştırılması için kullandım.

### Publishing Docker Images

https://docs.github.com/actions/guides/publishing-docker-images

Docker image'larının GitHub Actions üzerinden build edilmesi ve registry'ye gönderilmesi için kullandım.

### GITHUB_TOKEN

https://docs.github.com/actions/concepts/security/github_token

Release workflow'unun Kubernetes manifestlerini `main` branch'ine commit ve push etmesi sırasında kullanılan repository token davranışını anlamak için kullandım.

## GitHub Container Registry

### Working with the Container Registry

https://docs.github.com/packages/working-with-a-github-packages-registry/working-with-the-container-registry

Backend ve frontend Docker image'larının GHCR üzerinde tutulması ve GitHub Actions tarafından publish edilmesi için kullandım.

## GitHub Releases

### Managing Releases

https://docs.github.com/repositories/releasing-projects-on-github/managing-releases-in-a-repository

`v1.0.0`, `v1.0.1` ve `v1.0.2` gibi Git tag'lerinden GitHub Release oluşturma süreci için kullandım.

## Kubernetes

### Deployments

https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

Backend ve frontend container'larının Deployment resource'ları üzerinden çalıştırılması ve replica yönetimi için kullandım.

### Services

https://kubernetes.io/docs/concepts/services-networking/service/

Backend için ClusterIP, frontend için NodePort Service oluşturulması ve Service selector yapısı için kullandım.

### Images

https://kubernetes.io/docs/concepts/containers/images/

Kubernetes node mimarisi ile Docker image platform uyumluluğunu kontrol ederken kullandım.

## Minikube

### Minikube Start

https://minikube.sigs.k8s.io/docs/start/

Docker driver kullanarak local Kubernetes cluster oluşturmak ve Minikube üzerinde uygulamayı çalıştırmak için kullandım.

## Argo CD

### Getting Started

https://argo-cd.readthedocs.io/en/stable/getting_started/

Argo CD'nin Kubernetes cluster'a kurulması ve temel çalışma yapısı için kullandım.

### Application Specification

https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/

`argocd/application.yaml` içerisinde repository, `main` branch, `k8s/` path, destination ve sync policy ayarlarını tanımlarken kullandım.

### Automated Sync Policy

https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/

Automated sync, `prune` ve `selfHeal` davranışlarını yapılandırmak için kullandım.

### Automation from CI Pipelines

https://argo-cd.readthedocs.io/en/stable/user-guide/ci_automation/

Release pipeline'ın yeni image'ı registry'ye gönderdikten sonra Git'teki Kubernetes manifestini güncellemesi ve deployment işleminin Argo CD tarafından yapılması için kullandım.

Projedeki son akışta GitHub Actions release sırasında manifestlerdeki image tag'lerini güncelliyor ve `main` branch'ine push ediyor. Argo CD ise bu değişikliği algılayıp yeni release'i Kubernetes cluster'a uyguluyor.

## Git

### Git Documentation

https://git-scm.com/docs

Feature, `dev` ve `main` branch akışı; commit, merge ve manuel version tag işlemleri için kullandım.