# Two-Service CI/CD Pipeline with Argo CD

İki Flask servisinden oluşan örnek uygulama için branch bazlı CI/CD, Kubernetes üzerinde PostgreSQL ve Redis HA, observability ve Argo CD ile GitOps deployment akışı.

## Quick Start

Gereksinimler:

- Git
- Docker Desktop
- Python 3
- kubectl
- k3d
- Helm

Repository:

```bash
git clone https://github.com/emreeaarslan/cicd-task.git
cd cicd-task
```

k3d cluster:

```bash
k3d cluster create --config k3d/cluster.yaml
kubectl get nodes
```

CloudNativePG operator:

```bash
kubectl apply --server-side -f \
  https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-1.30/releases/cnpg-1.30.0.yaml

kubectl rollout status deployment \
  -n cnpg-system cnpg-controller-manager
```

Redis Operator:

```bash
helm repo add ot-helm https://ot-container-kit.github.io/helm-charts/
helm repo update

helm upgrade --install redis-operator ot-helm/redis-operator \
  --version 0.26.1 \
  --namespace ot-operators \
  --create-namespace
```

Redis Secret:

```bash
REDIS_PASSWORD="$(openssl rand -base64 24)"

kubectl create secret generic redis-secret \
  --from-literal=password="$REDIS_PASSWORD" \
  --dry-run=client -o yaml | kubectl apply -f -

unset REDIS_PASSWORD
```

Argo CD:

```bash
kubectl create namespace argocd

kubectl apply -n argocd --server-side --force-conflicts \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Argo CD Application:

```bash
kubectl apply -f argocd/application.yaml
kubectl apply -f argocd/grafana-application.yaml
```

Durum kontrolü:

```bash
kubectl get pods
kubectl get cluster postgres-cluster
kubectl get redisreplication,redissentinel
kubectl get applications.argoproj.io -n argocd
```

Frontend:

```bash
kubectl port-forward svc/frontend 5002:5002
```

Tarayıcı:

```text
http://localhost:5002
```

Prometheus, Grafana ve Mailpit:

```bash
kubectl port-forward svc/prometheus 9090:9090
kubectl port-forward svc/grafana-helm 3000:80
kubectl port-forward svc/mailpit 8025:8025
```

Port-forward komutları ayrı terminallerde çalıştırılır.

```text
Prometheus: http://localhost:9090
Grafana:    http://localhost:3000
Mailpit:    http://localhost:8025
```

## Mimari

```text
GitHub
  │
  ├─ feature/* / PR / dev / main
  │        │
  │        ▼
  │   GitHub Actions
  │   ├─ tests
  │   ├─ multi-platform Docker build
  │   ├─ GHCR publish
  │   └─ release sırasında image tag update
  │
  ▼
Argo CD
  ├─ cicd-task    → main/k8s
  └─ grafana-helm → grafana-community/grafana Helm chart
          │
          ▼
     k3d Kubernetes
          │
          ├─ Frontend (Gunicorn)
          ├─ Backend (Gunicorn)
          ├─ PostgreSQL HA (CloudNativePG)
          ├─ Redis Replication + Sentinel
          ├─ OpenTelemetry Collector
          ├─ Prometheus
          ├─ Tempo
          ├─ Mailpit
          └─ Grafana (Helm)
```

Uygulama akışı:

```text
Browser
  ↓
Frontend :5002
  ↓
Backend :5001
  ↓
PostgreSQL HA cluster
```

Observability:

```text
Frontend / Backend
  ├─ JSON logs ─────────────> stdout / kubectl logs
  ├─ Prometheus metrics ────> Prometheus ──> Grafana
  └─ OpenTelemetry traces ──> OTel Collector ──> Tempo ──> Grafana

CloudNativePG PostgreSQL
  └─ built-in metrics :9187 ─> Prometheus ──> Grafana

Grafana Alerting
  └─ email notification ────> Mailpit
```

## Görev Kapsamı

| İstenen | Projedeki karşılığı |
| --- | --- |
| En az iki servis | Flask frontend + backend |
| Branch bazlı pipeline | feature / PR / dev / main davranışları |
| Test ve paketleme | pytest + Docker build |
| Release | Semantic version tag + GHCR + GitHub Release |
| Deployment Argo CD'ye devredilsin | GitHub Actions manifesti günceller, Argo CD deploy eder |
| PostgreSQL persistence | Backend veriyi PostgreSQL'e yazar/okur |
| PostgreSQL HA | CloudNativePG, 3 instance |
| Frontend/backend healthcheck | startup, readiness, liveness probe'ları |
| Gunicorn | İki servis de `--workers 1` ile serve edilir |
| Minikube yerine k3d | 1 server + 2 agent k3d cluster |
| Structured logging | JSON request logları |
| OTel traces | Flask/Requests/Psycopg → OTel Collector |
| Prometheus metrics | Frontend, backend ve PostgreSQL |
| StatefulSet/operator incelemesi | Redis StatefulSet üretir; CNPG PostgreSQL için StatefulSet kullanmaz |
| DB primary/secondary Service yapısı | CNPG `rw`, `ro`, `r` Service'leri |
| Grafana Helm installation | Grafana Community Helm chart + Argo CD Application |
| Grafana datasource as code | Prometheus ve Tempo datasource'ları ConfigMap ile |
| Grafana dashboard as code | Dashboard JSON'ları ConfigMap ile |
| Grafana alert as code | Alert rule, contact point ve notification policy ConfigMap ile |
| Mailpit | Grafana email alert'lerini alan SMTP + Web UI container'ı |
| DB dashboard | CloudNativePG dashboard'u |
| Uygulama dashboard'u | `Application Overview` |
| Tempo tracing | OTel Collector → Tempo → Grafana Explore |
| Head sampling | `/sampling/head`, SDK tarafında %50 sampling |
| Tail sampling | `/sampling/tail`, Collector trace tamamlandıktan sonra karar verir |
| Redis Operator | OpsTree Redis Operator |
| Redis storage | 3 x 1 Gi PVC |
| Redis HA/failover | 1 primary + 2 replica + 3 Sentinel |
| Sentinel vs Cluster seçimi | Sharding gerekmediği için Sentinel |

## Proje Yapısı

```text
.
├── backend-service/
├── frontend-service/
├── grafana/
│   └── dashboards/
│       ├── application-overview.json
│       └── cloudnativepg.json
├── k3d/
│   └── cluster.yaml
├── k8s/
│   ├── backend.yaml
│   ├── frontend.yaml
│   ├── postgres.yaml
│   ├── redis.yaml
│   ├── prometheus.yaml
│   ├── otel-collector.yaml
│   ├── tempo.yaml
│   ├── mailpit.yaml
│   ├── grafana-helm-datasource.yaml
│   ├── grafana-dashboards.yaml
│   ├── grafana-helm-alerts.yaml
│   └── grafana-helm-notifications.yaml
├── argocd/
│   ├── application.yaml
│   └── grafana-application.yaml
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   └── references.md
└── docker-compose.yaml
```

## Local Testler

Backend:

```bash
cd backend-service
python -m pip install -r requirements-dev.txt
python -m pytest -v
cd ..
```

Frontend:

```bash
cd frontend-service
python -m pip install -r requirements-dev.txt
python -m pytest -v
cd ..
```

Docker build:

```bash
docker build -t cicd-backend:check ./backend-service
docker build -t cicd-frontend:check ./frontend-service
```

## PostgreSQL HA ve Persistence

CloudNativePG cluster:

```text
3 PostgreSQL instance
1 primary
2 replica
3 x 1 Gi persistent PVC
```

Durum:

```bash
kubectl get cluster postgres-cluster
kubectl get pods -l cnpg.io/cluster=postgres-cluster
kubectl get pvc | grep postgres-cluster
```

### StatefulSet ve Operator Yapısı

CloudNativePG bu projede PostgreSQL'i Kubernetes `StatefulSet` resource'u ile yönetmez.

PostgreSQL Pod ve PVC'lerinin owner'ı:

```text
Cluster/postgres-cluster
```

CNPG kendi `Cluster` custom resource'u üzerinden Pod, PVC ve Service'leri reconcile eder.

Redis Operator ise `RedisReplication` custom resource'undan StatefulSet üretir. Böylece iki operator'ın stateful workload yönetimindeki yaklaşımı karşılaştırılmıştır.

### Primary / Replica Service'leri

CloudNativePG tarafından yönetilen Service'ler:

```text
postgres-cluster-rw → primary
postgres-cluster-ro → replica'lar
postgres-cluster-r  → okunabilir tüm instance'lar
```

Selector'lar:

```text
-rw → cnpg.io/instanceRole=primary
-ro → cnpg.io/instanceRole=replica
-r  → cnpg.io/podRole=instance
```

Backend primary Pod IP'sini bilmez.

`DATABASE_URL`, CloudNativePG'nin oluşturduğu `postgres-cluster-app` Secret içindeki `uri` key'inden alınır. Bu bağlantının host'u `postgres-cluster-rw` Service'idir.

Primary değiştiğinde backend configuration değişmez; Service yeni primary role sahip Pod'a yönelir.

## Redis HA

Redis, OpsTree Redis Operator ile yönetilir.

Topoloji:

```text
RedisReplication
  ├─ 1 primary
  ├─ 2 replica
  └─ 3 x 1 Gi PVC

RedisSentinel
  └─ 3 Sentinel
```

Operator tarafından oluşturulan StatefulSet'ler:

```text
redis-replication
redis-sentinel-sentinel
```

### Neden Sentinel?

Redis Cluster'ın temel amacı veriyi birden fazla primary arasında shard ederek horizontal scaling sağlamaktır.

Bu projede sharding ihtiyacı yoktur. Gereksinim replication, persistent storage, HA ve automatic failover olduğu için Redis Replication + Sentinel seçilmiştir.

### Failover Doğrulaması

Failover testi sırasında:

- primary'nin bulunduğu node scheduling dışına alındı,
- primary Pod silindi,
- Sentinel bir replica'yı yeni primary'ye promote etti,
- `redis-replication-master` Service yeni primary'ye geçti,
- önceden yazılmış test verisi erişilebilir kaldı,
- eski primary geri geldiğinde replica olarak yeni primary'ye bağlandı.

Bu test replication, Sentinel failover, Service yönlendirmesi ve recovery akışını doğruladı.

## Health Checks ve Gunicorn

Backend:

```text
GET /health
GET /health/ready
```

Backend readiness PostgreSQL bağlantısını da kontrol eder. Liveness DB'den bağımsızdır.

Frontend:

```text
GET /health
```

Kubernetes manifestlerinde startup, readiness ve liveness probe'ları bulunur.

İki servis de Flask development server yerine Gunicorn ile çalışır:

```text
backend:  gunicorn --workers 1 --bind 0.0.0.0:5001 app:app
frontend: gunicorn --workers 1 --bind 0.0.0.0:5002 app:app
```

## Observability

### Structured Logging

Frontend ve backend HTTP request loglarını JSON olarak stdout'a yazar.

Temel alanlar:

```text
timestamp
level
service
message
method
path
status
duration_ms
```

```bash
kubectl logs deployment/frontend
kubectl logs deployment/backend
```

### OpenTelemetry Tracing

Distributed tracing zinciri:

```text
Frontend Flask span
  ↓
Frontend HTTP client span
  ↓
Backend Flask span
  ↓
PostgreSQL client spans
  ↓
OTel Collector
  ↓
Tempo
  ↓
Grafana Explore
```

Uygulamalar trace'leri OTLP/HTTP ile Collector'a gönderir:

```text
http://otel-collector:4318/v1/traces
```

Collector trace'leri Tempo'nun OTLP gRPC endpoint'ine iletir:

```text
tempo:4317
```

Tempo, Grafana'da provision edilmiş datasource olarak kullanılır.

Sampling örnekleri:

```text
GET /sampling/head
GET /sampling/tail?outcome=ok
GET /sampling/tail?outcome=error
```

`/sampling/head` için karar backend OpenTelemetry SDK'sında trace başlarken verilir. Sample edilmeyen trace Collector'a ulaşmaz.

`/sampling/tail` trace'leri Collector'a ulaşır. Tail sampling processor trace'i bekleyip attribute'lara göre karar verir; demo politikasında `ok` trace drop edilir, `error` trace tutulur.

### Prometheus

Frontend ve backend:

```text
GET /metrics
```

Custom application metrics:

```text
http_requests_total
http_request_duration_seconds
```

PostgreSQL metrics CloudNativePG built-in exporter tarafından `9187` portunda expose edilir.

Örnek PromQL:

```promql
up
```

```promql
sum by(job, status) (rate(http_requests_total[5m]))
```

```promql
cnpg_collector_up
```

### Grafana

Grafana, `argocd/grafana-application.yaml` üzerinden Grafana Community Helm chart ile deploy edilir.

Provision edilen datasource'lar:

```text
Prometheus → http://prometheus:9090
Tempo      → http://tempo:3200
```

Datasource configuration:

```text
k8s/grafana-helm-datasource.yaml
```

Dashboard'lar:

```text
grafana/dashboards/application-overview.json
grafana/dashboards/cloudnativepg.json
```

`Application Overview`:

- Request Rate
- Requests by Status
- Average Request Duration
- Application Targets
- 5xx Error Rate
- Requests Last 5 Minutes

Dashboard JSON'ları `k8s/grafana-dashboards.yaml` ConfigMap'i ile provision edilir.

Alerting de configuration-as-code olarak tutulur:

```text
k8s/grafana-helm-alerts.yaml
k8s/grafana-helm-notifications.yaml
```

Alert rule, email contact point ve notification policy provisioning ile yüklenir.

SMTP hedefi:

```text
mailpit:1025
```

Mailpit Web UI:

```text
http://localhost:8025
```

CloudNativePG dashboard ConfigMap'i büyük olduğu için Argo CD Server-Side Apply kullanılır:

```text
argocd.argoproj.io/sync-options: ServerSideApply=true
```

## CI/CD

Workflow:

```text
.github/workflows/ci.yml
```

| Trigger | Tests | Docker Build | GHCR Push | Release |
| --- | --- | --- | --- | --- |
| `feature/**` push | Evet | Evet | Hayır | Hayır |
| PR → `dev` / `main` | Evet | Evet | Hayır | Hayır |
| `dev` push | Evet | Evet | `dev-<commit-sha>` | Hayır |
| `main` push | Evet | Evet | Hayır | Hayır |
| `v*.*.*` tag | Evet | Release build | `vX.Y.Z` | Evet |

Docker image'ları QEMU + Buildx ile:

```text
linux/amd64
linux/arm64
```

platformları için build edilir.

## Release ve Argo CD

Release semantic version tag ile başlatılır:

```bash
git tag -a vX.Y.Z -m "release: vX.Y.Z"
git push origin vX.Y.Z
```

Release workflow:

```text
tests
  ↓
release Docker images
  ↓
GHCR
  ↓
main/k8s image tag update
  ↓
GitHub Release
  ↓
Argo CD
  ↓
k3d Kubernetes
```

GitHub Actions Kubernetes'e doğrudan deploy etmez.

Argo CD:

- `main/k8s` desired state'ini takip eder,
- automated sync yapar,
- `selfHeal` ile manual drift'i geri alır,
- `prune` ile Git'ten kaldırılan managed resource'ları temizler.

## Branch Stratejisi

```text
feature/*
   ↓
  dev
   ↓
 main
   ↓
vX.Y.Z
```

`dev` integration branch'idir.

`main`, Argo CD'nin takip ettiği release edilebilir desired state'i tutar.

## Hızlı Doğrulama

```bash
kubectl get nodes
kubectl get pods
kubectl get pvc
kubectl get cluster postgres-cluster
kubectl get redisreplication,redissentinel
kubectl get applications.argoproj.io -n argocd
```

PostgreSQL Service'leri:

```bash
kubectl get svc | grep postgres-cluster
```

Redis:

```bash
kubectl get statefulset | grep redis
kubectl get svc | grep redis
```

Observability:

```bash
kubectl get deployment prometheus otel-collector tempo mailpit
kubectl get deployment grafana-helm
kubectl -n argocd get application cicd-task grafana-helm
```

## Kaynaklar

Projede kullanılan resmi dokümantasyonlar:

```text
docs/references.md
```