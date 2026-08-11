# References

Bu projede uygulama, test, container, CI/CD, Kubernetes ve GitOps konularında ağırlıklı olarak resmi dokümantasyonlar kullanılmıştır.

## Flask

**Flask Quickstart**  
https://flask.palletsprojects.com/en/stable/quickstart/

Backend ve frontend Flask uygulamalarının route yapısı ve temel uygulama davranışları için kullanıldı.

**Flask Testing**  
https://flask.palletsprojects.com/en/stable/testing/

Flask test client kullanımı ve endpoint testlerinin oluşturulması için kullanıldı.

## pytest

**pytest Getting Started**  
https://docs.pytest.org/en/stable/getting-started.html

Backend ve frontend testlerinin pytest ile çalıştırılması için kullanıldı.

## Python Mock

**unittest.mock**  
https://docs.python.org/3/library/unittest.mock.html

Frontend testinde gerçek backend servisini çalıştırmadan HTTP çağrısının mocklanması için kullanıldı.

## Docker

**Dockerfile Reference**  
https://docs.docker.com/reference/dockerfile/

Backend ve frontend servislerinin Dockerfile'larının hazırlanması için kullanıldı.

**Docker Build Context and .dockerignore**  
https://docs.docker.com/build/concepts/context/

Docker build context ve `.dockerignore` dosyalarının hazırlanması için kullanıldı.

**Docker Compose Networking**  
https://docs.docker.com/compose/how-tos/networking/

Frontend servisinin Compose ortamında backend servisine `backend` servis adı üzerinden erişmesi için kullanıldı.

**Docker Multi-platform Builds**  
https://docs.docker.com/build/building/multi-platform/

AMD64 ve ARM64 platformları için aynı Docker image tag'i altında multi-platform image üretimini anlamak için kullanıldı.

**Docker GitHub Actions Multi-platform Build**  
https://docs.docker.com/build/ci/github-actions/multi-platform/

GitHub Actions pipeline'ına QEMU, Buildx ve `linux/amd64,linux/arm64` platformlarının eklenmesi için kullanıldı.

## GitHub Actions

**GitHub Actions Workflow Syntax**  
https://docs.github.com/actions/reference/workflows-and-actions/workflow-syntax

Branch, pull request ve tag trigger'larının tanımlanması ve job bağımlılıklarının oluşturulması için kullanıldı.

**Building and Testing Python**  
https://docs.github.com/actions/automating-builds-and-tests/building-and-testing-python

GitHub Actions üzerinde Python kurulumu, dependency installation ve pytest çalıştırılması için kullanıldı.

**Publishing Docker Images**  
https://docs.github.com/actions/guides/publishing-docker-images

GitHub Actions üzerinden Docker image build ve publish işlemleri için kullanıldı.

## GitHub Container Registry

**Working with the Container Registry**  
https://docs.github.com/packages/working-with-a-github-packages-registry/working-with-the-container-registry

Docker image'larının GHCR üzerinde saklanması, `GITHUB_TOKEN` kullanımı ve package publishing için kullanıldı.

## GitHub Releases

**Managing Releases in a Repository**  
https://docs.github.com/repositories/releasing-projects-on-github/managing-releases-in-a-repository

Version tag üzerinden GitHub Release oluşturulması için kullanıldı.

## Kubernetes

**Deployments**  
https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

Backend ve frontend Pod'larının Deployment kaynakları üzerinden yönetilmesi için kullanıldı.

**Services**  
https://kubernetes.io/docs/concepts/services-networking/service/

Backend için ClusterIP, frontend için NodePort Service oluşturulması ve Service selector mantığının anlaşılması için kullanıldı.

**Images**  
https://kubernetes.io/docs/concepts/containers/images/

Kubernetes node mimarisi ile Docker image platform uyumluluğunun değerlendirilmesi için kullanıldı.

## Minikube

**Minikube Start**  
https://minikube.sigs.k8s.io/docs/start/

Local Kubernetes cluster'ın Docker driver ile oluşturulması için kullanıldı.

## Argo CD

**Argo CD Getting Started**  
https://argo-cd.readthedocs.io/en/stable/getting_started/

Argo CD'nin Kubernetes cluster'a kurulması ve temel kullanım modeli için kullanıldı.

**Application Specification**  
https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/

`argocd/application.yaml` içerisinde repository, branch, path, destination ve sync policy alanlarının tanımlanması için kullanıldı.

**Automated Sync Policy**  
https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/

Automated sync, `prune` ve `selfHeal` davranışlarının yapılandırılması için kullanıldı.

## Git

**Git Documentation**  
https://git-scm.com/docs

Feature, dev ve main branch akışları, commit, merge ve version tag işlemleri için referans olarak kullanıldı.