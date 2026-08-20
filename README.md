# Two-Service CI/CD Pipeline with Argo CD

İki Flask servisinden oluşan örnek uygulama için branch bazlı CI/CD pipeline, Kubernetes üzerinde PostgreSQL HA/persistence, observability ve Argo CD ile GitOps deployment akışı.

## Genel Mimari

```text
GitHub
  │
  ├─ feature/* / PR / dev / main
  │        │
  │        ▼
  │   GitHub Actions
  │   ├─ Backend tests
  │   ├─ Frontend tests
  │   ├─ Multi-platform Docker build
  │   ├─ GHCR publish
  │   └─ Release sırasında Kubernetes image tag update
  │
  └─ main/k8s
           │
           ▼
        Argo CD
           │
           ▼
      k3d Kubernetes
           │
           ├─ Frontend (Gunicorn)
           ├─ Backend (Gunicorn)
           ├─ CloudNativePG PostgreSQL HA cluster
           ├─ OpenTelemetry Collector
           └─ Prometheus
```

Uygulama akışı:

```text
Browser
  │
  ▼
Frontend :5002
  │
  ▼
Backend :5001
  │
  ▼
PostgreSQL HA cluster
```

Observability akışı:

```text
Frontend / Backend
  ├─ JSON structured logs ──> stdout / kubectl logs
  ├─ Prometheus metrics ────> Prometheus
  └─ OpenTelemetry traces ──> OTel Collector

CloudNativePG PostgreSQL
  └─ built-in metrics :9187 ─> Prometheus
```

## Özellikler

- İki ayrı Flask servis: frontend ve backend
- Backend için PostgreSQL persistence
- CloudNativePG ile 3 instance PostgreSQL HA cluster
- Backend ve frontend için Gunicorn
- Kubernetes startup, readiness ve liveness health probe'ları
- k3d üzerinde 1 server + 2 agent node
- JSON structured logging
- OpenTelemetry distributed tracing
- Frontend ve backend için Prometheus metrics
- PostgreSQL için CloudNativePG built-in Prometheus metrics
- Cluster içinde Prometheus Server ve Web UI
- GitHub Actions ile branch bazlı test/build/release akışı
- GHCR üzerinde multi-platform (`linux/amd64`, `linux/arm64`) image'lar
- Argo CD ile GitOps deployment, automated sync, prune ve self-heal

## Görev Kapsamı Kontrolü

Değerlendirme kapsamında istenen maddelerin projedeki karşılığı:

| İstenen | Projedeki karşılığı |
| --- | --- |
| Backend için PostgreSQL persistence | Backend `DATABASE_URL` ile PostgreSQL'e bağlanır; mesajlar DB'ye yazılır ve DB'den okunur |
| PostgreSQL HA ve cluster içinde çalışma | CloudNativePG `Cluster`, `instances: 3`, Kubernetes `default` namespace |
| Frontend + backend healthcheck | Uygulama health endpoint'leri ve Kubernetes startup/readiness/liveness probe'ları |
| İki uygulamanın Gunicorn ile serve edilmesi | Her iki Dockerfile da `gunicorn ... app:app` ile başlatılır |
| Minikube yerine k3d | Final local Kubernetes ortamı `k3d/cluster.yaml` ile oluşturulan k3d cluster'dır |
| Structured logging | Frontend ve backend JSON request loglarını stdout'a yazar |
| OTel traces | Flask/Requests/Psycopg instrumentation → OTLP/HTTP → OpenTelemetry Collector |
| Prometheus metrics: frontend + backend | Her iki serviste `/metrics`, Counter ve Histogram metrikleri |
| Prometheus metrics: PostgreSQL | CloudNativePG PostgreSQL instance exporter metrikleri Prometheus tarafından scrape edilir |

Minikube final çalışma ortamının parçası değildir. `docker-compose.yaml` yalnızca basit local geliştirme/karşılaştırma için repoda tutulur; final Kubernetes çalıştırma ve değerlendirme ortamı k3d'dir.

## Proje Yapısı

```text
.
├── backend-service/
├── frontend-service/
├── k3d/
│   └── cluster.yaml
├── k8s/
│   ├── backend.yaml
│   ├── frontend.yaml
│   ├── postgres.yaml
│   ├── otel-collector.yaml
│   └── prometheus.yaml
├── argocd/
│   └── application.yaml
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   └── references.md
└── docker-compose.yaml
```

## Gereksinimler

Final Kubernetes ortamı için:

- Git
- Docker Desktop
- Python 3
- kubectl
- k3d

Argo CD ve CloudNativePG operator cluster'a ayrıca kurulur.

## Repository'yi Klonlama

```bash
git clone https://github.com/emreeaarslan/cicd-task.git
cd cicd-task
```

## Local Testler

Virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

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

## k3d Cluster

Cluster repository içindeki config ile oluşturulur:

```bash
k3d cluster create --config k3d/cluster.yaml
```

Config:

```text
1 server
2 agents
```

Kontrol:

```bash
kubectl config current-context
kubectl get nodes
```

Beklenen context:

```text
k3d-cicd-cluster
```

### k3d Üzerindeki Frontend'e Erişim

Final uygulama Kubernetes içinde k3d üzerinde çalışır. Frontend Service'i local tarayıcıya açmak için:

```bash
kubectl port-forward svc/frontend 5002:5002
```

Ardından:

```text
http://localhost:5002
```

adresinden frontend kullanılabilir. Frontend, cluster içinde backend Service'e `http://backend:5001` üzerinden ulaşır.

## CloudNativePG Operator

`k8s/postgres.yaml` bir CloudNativePG `Cluster` resource'u kullandığı için önce operator kurulmalıdır.

Bu projede kullanılan 1.30 serisi için:

```bash
kubectl apply --server-side -f \
  https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-1.30/releases/cnpg-1.30.0.yaml
```

Operator kontrolü:

```bash
kubectl rollout status deployment \
  -n cnpg-system cnpg-controller-manager
```

PostgreSQL cluster, uygulama manifestleri Argo CD tarafından sync edildiğinde oluşturulur.

## Argo CD Kurulumu

Namespace:

```bash
kubectl create namespace argocd
```

Kurulum:

```bash
kubectl apply -n argocd --server-side --force-conflicts \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Kontrol:

```bash
kubectl get pods -n argocd
```

UI için:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Tarayıcı:

```text
https://localhost:8080
```

## Argo CD Application

`argocd/application.yaml` şu desired state'i takip eder:

- Repository: `https://github.com/emreeaarslan/cicd-task.git`
- Branch: `main`
- Path: `k8s`
- Destination: aynı Kubernetes cluster
- Namespace: `default`

Final `main` desired state hazır olduğunda:

```bash
kubectl apply -f argocd/application.yaml
```

Kontrol:

```bash
kubectl get applications.argoproj.io -n argocd
```

Hedef durum:

```text
Synced
Healthy
```

Argo CD automated sync ile Git değişikliklerini cluster'a uygular. `selfHeal` cluster'da yapılan manuel drift'i Git'teki desired state'e geri döndürür. `prune` ise Argo tarafından yönetilen ve daha sonra Git'ten kaldırılan resource'ların temizlenmesini sağlar.

## Kubernetes Uygulaması

Argo CD sync sonrasında:

```bash
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get pvc
```

Backend iki replica olarak çalışır. Frontend backend'e Kubernetes Service DNS üzerinden erişir:

```text
http://backend:5001
```

PostgreSQL, CloudNativePG tarafından üç instance olarak yönetilir.

## Health Checks

Backend:

```text
GET /health
GET /health/ready
```

Backend readiness kontrolü PostgreSQL bağlantısını da doğrular. Liveness kontrolü ise database kesintisinde gereksiz container restart döngüsü oluşturmamak için DB'den bağımsızdır.

Frontend:

```text
GET /health
```

Kubernetes manifestlerinde startup, readiness ve liveness probe'ları tanımlıdır.

## Gunicorn

Frontend ve backend Flask development server ile değil Gunicorn ile serve edilir.

Pod loglarında Gunicorn process'leri görülebilir:

```bash
kubectl logs deployment/backend
kubectl logs deployment/frontend
```

## PostgreSQL Persistence ve HA

Backend uygulama verisini PostgreSQL'e yazar ve PostgreSQL'den okur.

CloudNativePG cluster:

```text
3 PostgreSQL instance
1 primary
2 replica
```

Durum:

```bash
kubectl get cluster
kubectl get pods -l cnpg.io/cluster=postgres-cluster
```

CloudNativePG primary failover işlemini yönetir. Bir PostgreSQL pod'u kaybedildiğinde yeni primary seçilebilir ve cluster tekrar üç instance'a tamamlanır.

Bu repository local k3d ortamı için tasarlandığından persistence local Kubernetes storage class üzerinde çalışır; bu, production seviyesinde çok-node storage altyapısının yerini tutmaz.

## Structured Logging

Frontend ve backend HTTP request loglarını JSON formatında stdout'a yazar.

Örnek alanlar:

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

Logları görmek için:

```bash
kubectl logs deployment/frontend
kubectl logs deployment/backend
```

Bu task kapsamında Loki/Elasticsearch gibi ayrı bir log backend'i kullanılmıyor.

## OpenTelemetry Tracing

Frontend ve backend OpenTelemetry ile instrument edilmiştir.

Tracing zinciri:

```text
Browser
  ↓
Frontend Flask span
  ↓
Frontend HTTP client span
  ↓
Backend Flask span
  ↓
PostgreSQL client spans
```

Bütün zincir aynı Trace ID üzerinden takip edilebilir.

Trace'ler OTLP/HTTP ile cluster içindeki OpenTelemetry Collector'a gönderilir:

```text
http://otel-collector:4318/v1/traces
```

Collector bu task kapsamında `debug` exporter kullanır. Jaeger veya Tempo eklenmemiştir.

Collector logları:

```bash
kubectl logs deployment/otel-collector
```

## Prometheus Metrics

Frontend ve backend:

```text
GET /metrics
```

Custom application metrics:

```text
http_requests_total
http_request_duration_seconds
```

PostgreSQL metrics, CloudNativePG'nin built-in exporter'ı tarafından `9187` portunda expose edilir.

Prometheus:

- frontend `/metrics`
- backend `/metrics`
- kendi `9090` endpoint'i
- CloudNativePG PostgreSQL pod'larının `metrics` portu

target'larını scrape eder.

Prometheus UI:

```bash
kubectl port-forward svc/prometheus 9090:9090
```

Tarayıcı:

```text
http://localhost:9090
```

Örnek PromQL sorguları:

```promql
up
```

```promql
sum by(job, endpoint, status) (http_requests_total)
```

```promql
cnpg_collector_up
```

```promql
cnpg_backends_total
```

Prometheus verisi için 2 GiB PVC kullanılmaktadır. Bu local k3d demo ortamına yönelik bir ayardır.

## CI Pipeline

Workflow:

```text
.github/workflows/ci.yml
```

Branch davranışı:

| Trigger | Tests | Docker Build | GHCR Push | Release |
| --- | --- | --- | --- | --- |
| `feature/**` push | Evet | Evet | Hayır | Hayır |
| PR → `dev` / `main` | Evet | Evet | Hayır | Hayır |
| `dev` push | Evet | Evet | `dev-<commit-sha>` | Hayır |
| `main` push | Evet | Evet | Hayır | Hayır |
| `v*.*.*` tag | Evet | Release build | `vX.Y.Z` | Evet |

Backend ve frontend testleri ayrı job'larda çalışır.

Docker build, test job'larına `needs` ile bağlıdır.

Image'lar QEMU + Docker Buildx ile:

```text
linux/amd64
linux/arm64
```

platformları için oluşturulur.

## Release Akışı

Release manuel Git tag'i ile başlatılır:

```bash
git tag -a vX.Y.Z -m "release: vX.Y.Z"
git push origin vX.Y.Z
```

Tag geldiğinde GitHub Actions:

1. Backend ve frontend testlerini çalıştırır.
2. Backend ve frontend release image'larını build eder.
3. Image'ları GHCR'ye `vX.Y.Z` tag'i ile push eder.
4. `k8s/backend.yaml` ve `k8s/frontend.yaml` image tag'lerini aynı sürüme günceller.
5. Manifest değişikliğini `main` branch'ine commit ve push eder.
6. GitHub Release oluşturur.

Release artifact örneği:

```text
ghcr.io/emreeaarslan/cicd-backend:vX.Y.Z
ghcr.io/emreeaarslan/cicd-frontend:vX.Y.Z
```

## Argo CD ile GitOps Deployment

GitHub Actions Kubernetes'e doğrudan deploy etmez.

Workflow içerisinde release deployment için:

```text
kubectl apply
```

kullanılmaz.

Sorumluluk ayrımı:

```text
GitHub Actions
  ├─ test
  ├─ Docker build
  ├─ GHCR publish
  ├─ GitHub Release
  └─ main/k8s image tag update

Argo CD
  ├─ main/k8s desired state'i takip eder
  ├─ Kubernetes live state ile karşılaştırır
  ├─ sync eder
  ├─ self-heal uygular
  └─ gerektiğinde prune eder
```

Final deployment zinciri:

```text
Git tag
  ↓
GitHub Actions
  ↓
Tests
  ↓
Release Docker images
  ↓
GHCR
  ↓
main/k8s image tag update
  ↓
Argo CD
  ↓
k3d Kubernetes
```

Bu şekilde CI/release hazırlığı GitHub Actions tarafında, Kubernetes deployment ise Argo CD tarafında tutulur.

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

Feature branch'leri geliştirme için kullanılır.

`dev` entegrasyon branch'idir ve başarılı push'larda commit SHA ile etiketlenmiş development image'ları GHCR'ye gönderilir.

`main` release edilebilir kodu ve Argo CD'nin takip ettiği Kubernetes desired state'i tutar.

Version tag release workflow'unu başlatır.

## Kaynaklar

Kullanılan resmi dokümantasyonlar:

```text
docs/references.md
```
