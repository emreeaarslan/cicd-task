# References

Projeyi geliştirirken mümkün olduğunca kullanılan araçların resmi dokümantasyonları referans alındı.

## Flask

### Flask Quickstart

https://flask.palletsprojects.com/en/stable/quickstart/

Backend ve frontend Flask servislerinin oluşturulması, route tanımları ve temel uygulama yapısı için kullanıldı.

### Flask Testing

https://flask.palletsprojects.com/en/stable/testing/

Flask `test_client()` kullanımı ve endpoint testlerinin hazırlanması için kullanıldı.

## pytest

### Getting Started

https://docs.pytest.org/en/stable/getting-started.html

Backend ve frontend testlerinin `pytest` ile yazılması ve çalıştırılması için kullanıldı.

## Python Mock

### unittest.mock

https://docs.python.org/3/library/unittest.mock.html

Frontend testlerinde gerçek backend servisini çalıştırmadan HTTP cevabını mocklamak için kullanıldı.

## Requests

### Requests Quickstart

https://requests.readthedocs.io/en/stable/user/quickstart/

Frontend servisinden backend API'ye HTTP isteği gönderme, response okuma ve timeout kullanımı için kullanıldı.

## Psycopg

### Psycopg 3 Documentation

https://www.psycopg.org/psycopg3/docs/

Backend'in PostgreSQL'e bağlanması, SQL sorgularının çalıştırılması ve uygulama verisinin kalıcı olarak okunup yazılması için kullanıldı.

## Python Logging

### logging — Logging facility for Python

https://docs.python.org/3/library/logging.html

Frontend ve backend için `Logger`, `StreamHandler` ve custom `Formatter` kullanarak JSON structured logging oluşturmak için kullanıldı.

## Gunicorn

### Gunicorn Documentation

https://gunicorn.org/

Flask development server yerine frontend ve backend uygulamalarını Gunicorn ile serve etmek için kullanıldı.

### Gunicorn Settings

https://gunicorn.org/settings.html

Bind adresi, worker davranışı ve Gunicorn runtime ayarlarını anlamak için kullanıldı.

## Docker

### Dockerfile Reference

https://docs.docker.com/reference/dockerfile/

Backend ve frontend Dockerfile'larının hazırlanması için kullanıldı.

### Build Context

https://docs.docker.com/build/concepts/context/

Docker build context ve `.dockerignore` dosyalarının düzenlenmesi için kullanıldı.

### Docker Compose Networking

https://docs.docker.com/compose/how-tos/networking/

Servislerin Docker Compose ortamındaki servis isimleri üzerinden birbirine erişme mantığını anlamak için kullanıldı.

### Multi-platform Builds

https://docs.docker.com/build/building/multi-platform/

AMD64 ve ARM64 image'ların aynı image tag'i altında oluşturulması için kullanıldı.

### Multi-platform Images with GitHub Actions

https://docs.docker.com/build/ci/github-actions/multi-platform/

GitHub Actions pipeline'ına QEMU, Docker Buildx ve `linux/amd64,linux/arm64` desteği eklemek için kullanıldı.

## GitHub Actions

### Workflow Syntax

https://docs.github.com/actions/reference/workflows-and-actions/workflow-syntax

Branch, pull request ve tag trigger'ları; job yapısı; `needs`, `if` ve permission ayarları için kullanıldı.

### Building and Testing Python

https://docs.github.com/actions/automating-builds-and-tests/building-and-testing-python

GitHub Actions üzerinde Python kurulumu, dependency installation ve pytest çalıştırılması için kullanıldı.

### Publishing Docker Images

https://docs.github.com/actions/guides/publishing-docker-images

Docker image'larının GitHub Actions üzerinden build edilmesi ve registry'ye gönderilmesi için kullanıldı.

### GITHUB_TOKEN

https://docs.github.com/actions/concepts/security/github_token

Release workflow'unda GHCR publish, GitHub Release ve repository üzerinde manifest commit işlemlerinde kullanılan token davranışını anlamak için kullanıldı.

## GitHub Container Registry

### Working with the Container Registry

https://docs.github.com/packages/working-with-a-github-packages-registry/working-with-the-container-registry

Backend ve frontend Docker image'larının GHCR üzerinde tutulması ve GitHub Actions tarafından publish edilmesi için kullanıldı.

## GitHub Releases

### Managing Releases

https://docs.github.com/repositories/releasing-projects-on-github/managing-releases-in-a-repository

`vX.Y.Z` Git tag'lerinden GitHub Release oluşturma süreci için kullanıldı.

## Kubernetes

### Deployments

https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

Frontend, backend, Prometheus ve OpenTelemetry Collector gibi container workload'larının Deployment resource'ları ile yönetilmesi için kullanıldı.

### Services

https://kubernetes.io/docs/concepts/services-networking/service/

Cluster içi servis keşfi ve frontend/backend/Prometheus/OTel Collector erişimi için kullanıldı.

### Liveness, Readiness and Startup Probes

https://kubernetes.io/docs/concepts/workloads/pods/probes/

Frontend ve backend için startup, readiness ve liveness healthcheck tasarımı için kullanıldı.

### Persistent Volumes

https://kubernetes.io/docs/concepts/storage/persistent-volumes/

PostgreSQL ve Prometheus persistence için PVC/PV davranışını anlamak için kullanıldı.

### RBAC

https://kubernetes.io/docs/reference/access-authn-authz/rbac/

Prometheus'un Kubernetes API üzerinden PostgreSQL pod'larını keşfetmesi için kullanılan ServiceAccount, ClusterRole ve ClusterRoleBinding kaynakları için kullanıldı.

### Images

https://kubernetes.io/docs/concepts/containers/images/

Kubernetes image tag ve image platform davranışını anlamak için kullanıldı.

## k3d

### Using Config Files

https://k3d.io/stable/usage/configfile/

`k3d/cluster.yaml` ile 1 server ve 2 agent node içeren local Kubernetes cluster tanımlamak için kullanıldı.

### k3d Command Documentation

https://k3d.io/stable/usage/commands/

Cluster oluşturma, image import ve k3d komutlarını kullanmak için referans alındı.

### Exposing Services

https://k3d.io/stable/usage/exposing_services/

k3d içindeki Kubernetes servislerinin local makineden erişilebilir hale getirilmesi ve NodePort/port mapping yaklaşımını anlamak için referans alındı.

## CloudNativePG

### Installation and Upgrades — 1.30

https://cloudnative-pg.io/docs/1.30/installation_upgrade/

CloudNativePG operator'ünü Kubernetes cluster'a kurmak için kullanıldı.

### Quickstart — Deploy a PostgreSQL Cluster

https://cloudnative-pg.io/docs/1.30/quickstart/

CloudNativePG `Cluster` resource'u, `instances: 3` ile üç instance PostgreSQL cluster kurulumu ve local Kubernetes üzerinde cluster doğrulaması için kullanıldı.

### Storage

https://cloudnative-pg.io/docs/1.30/storage/

PostgreSQL instance'larının persistent volume kullanımı için referans alındı.

### Connecting from an Application

https://cloudnative-pg.io/docs/1.30/applications/

Backend'in CloudNativePG tarafından oluşturulan application secret ve read-write Service bilgileriyle PostgreSQL cluster'a bağlanması için referans alındı.

### Failover

https://cloudnative-pg.io/docs/1.30/failover/

Primary kaybı sonrası replica promotion ve automatic failover davranışını anlamak için kullanıldı.

### Monitoring

https://cloudnative-pg.io/docs/1.30/monitoring/

CloudNativePG'nin PostgreSQL instance'ları üzerinde expose ettiği Prometheus metrics ve built-in monitoring yapısı için kullanıldı.

## Prometheus

### Overview

https://prometheus.io/docs/introduction/overview/

Prometheus'un pull-based metric toplama modeli ve temel mimarisi için kullanıldı.

### Getting Started

https://prometheus.io/docs/prometheus/latest/getting_started/

Prometheus Server ve Web UI kullanımını anlamak için kullanıldı.

### Configuration

https://prometheus.io/docs/prometheus/latest/configuration/configuration/

`scrape_configs`, static target'lar, Kubernetes service discovery ve relabeling ayarları için kullanıldı.

### Querying Basics

https://prometheus.io/docs/prometheus/latest/querying/basics/

PromQL sorgularını kullanmak için referans alındı.

### Prometheus Python Client

https://prometheus.github.io/client_python/

Flask servislerinde Counter, Histogram ve `/metrics` endpoint'i oluşturmak için kullanıldı.

## OpenTelemetry

### Traces

https://opentelemetry.io/docs/concepts/signals/traces/

Trace, span, parent-child ilişkisi ve distributed tracing kavramlarını anlamak için kullanıldı.

### Context Propagation

https://opentelemetry.io/docs/concepts/context-propagation/

Frontend → backend çağrısında aynı distributed trace context'inin servisler arasında taşınması için referans alındı.

### OpenTelemetry Collector

https://opentelemetry.io/docs/collector/

OpenTelemetry Collector'ın receiver, processor ve exporter mimarisini anlamak için kullanıldı.

### Collector Configuration

https://opentelemetry.io/docs/collector/configuration/

OTLP receiver, batch processor ve debug exporter pipeline'ını yapılandırmak için kullanıldı.

### OTLP Specification

https://opentelemetry.io/docs/specs/otlp/

Uygulama trace'lerinin OTLP/HTTP ile Collector'a gönderilmesi için kullanılan protokolü anlamak için referans alındı.

### OpenTelemetry Python

https://opentelemetry.io/docs/languages/python/

Python OpenTelemetry API/SDK yapısı için kullanıldı.

### Python Instrumentation

https://opentelemetry.io/docs/languages/python/instrumentation/

`TracerProvider`, span processor ve Python tracing setup'ını anlamak için kullanıldı.

### Flask Instrumentation

https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/flask/flask.html

Flask server request'lerinin otomatik trace edilmesi için kullanıldı.

### Requests Instrumentation

https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/requests/requests.html

Frontend'in backend'e yaptığı `requests` HTTP çağrısının distributed trace'e dahil edilmesi için kullanıldı.

### Psycopg Instrumentation

https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/psycopg/psycopg.html

Backend'in PostgreSQL sorgularının trace span'ları olarak üretilmesi için kullanıldı.

## Argo CD

### Getting Started

https://argo-cd.readthedocs.io/en/stable/getting_started/

Argo CD'nin Kubernetes cluster'a kurulması ve temel çalışma yapısı için kullanıldı.

### Application Specification

https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/

`argocd/application.yaml` içerisinde repository, `main` branch, `k8s/` path, destination ve sync policy ayarlarını tanımlamak için kullanıldı.

### Automated Sync Policy

https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/

Automated sync, `prune` ve `selfHeal` davranışlarını yapılandırmak için kullanıldı.

### Automation from CI Pipelines

https://argo-cd.readthedocs.io/en/stable/user-guide/ci_automation/

Release pipeline'ın yeni image'ı registry'ye gönderdikten sonra Git'teki Kubernetes manifestini güncellemesi ve deployment işleminin Argo CD tarafından devralınması için kullanıldı.

Projede GitHub Actions release sırasında image'ları GHCR'ye publish eder ve Kubernetes manifestlerindeki image tag'lerini `main` branch'inde günceller. Argo CD ise `main/k8s` desired state'ini takip ederek Kubernetes deployment'ını gerçekleştirir.

## Git

### Git Documentation

https://git-scm.com/docs

Feature, `dev` ve `main` branch akışı; commit, merge ve manuel semantic version tag işlemleri için kullanıldı.
