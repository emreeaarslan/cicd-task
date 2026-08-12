# Two-Service CI/CD Pipeline with Argo CD

İki Flask servisinden oluşan basit bir uygulama için branch bazlı CI/CD pipeline ve Argo CD ile GitOps deployment akışı.

## Proje Yapısı

* `backend-service/` — Flask API servisi
* `frontend-service/` — Backend ile HTTP üzerinden haberleşen Flask frontend
* `k8s/` — Backend ve frontend Kubernetes manifestleri
* `argocd/` — Argo CD Application tanımı
* `.github/workflows/ci.yml` — GitHub Actions pipeline
* `docker-compose.yaml` — Servislerin local ortamda birlikte çalıştırılması
* `docs/references.md` — Kullanılan kaynaklar

## Uygulama

Backend `5001`, frontend `5002` portunda çalışır.

Backend endpointleri:

* `GET /health`
* `GET /api/message`

Frontend, backend adresini `BACKEND_URL` environment variable üzerinden alır.

Docker Compose ve Kubernetes ortamında backend'e `http://backend:5001` adresi üzerinden erişilir.

## Testler

Testler `pytest` ile çalıştırılıyor.

Backend tarafında:

* `/health` endpoint'inin başarılı cevap verdiği
* `/api/message` endpoint'inin frontend'in beklediği response yapısını koruduğu

kontrol ediliyor.

Frontend tarafında backend isteği mocklanarak gelen mesajın HTML içerisinde gösterildiği doğrulanıyor.

GitHub Actions üzerinde backend ve frontend testleri ayrı job'larda paralel çalışıyor. Docker build ve release job'ları testlerin başarılı olmasına bağlı.

## Branch Akışı

| Trigger      | Test | Docker Build   | GHCR Push          | Release |
| ------------ | ---- | -------------- | ------------------ | ------- |
| `feature/*`  | Evet | Build kontrolü | Hayır              | Hayır   |
| Pull Request | Evet | Build kontrolü | Hayır              | Hayır   |
| `dev`        | Evet | Evet           | `dev-<commit-sha>` | Hayır   |
| `main`       | Evet | Build kontrolü | Hayır              | Hayır   |
| `v*.*.*` tag | Evet | Evet           | Version tag        | Evet    |

Feature branch'lerinde değişikliklerin test ve build kontrolleri yapılıyor.

`dev` branch'ine giren kod için multi-platform Docker image'ları oluşturulup GHCR'ye `dev-<commit-sha>` etiketiyle gönderiliyor.

`main` release edilebilir kodu tutuyor. Normal bir main push'u release oluşturmuyor.

Release işlemi manuel olarak oluşturulan `v1.0.0`, `v1.0.1`, `v1.0.2` gibi Git tag'leriyle başlatılıyor.

## Docker ve GHCR

Backend ve frontend ayrı Docker image'ları olarak paketleniyor.

* `ghcr.io/emreeaarslan/cicd-backend`
* `ghcr.io/emreeaarslan/cicd-frontend`

Güncel release örneği:

* `ghcr.io/emreeaarslan/cicd-backend:v1.0.2`
* `ghcr.io/emreeaarslan/cicd-frontend:v1.0.2`

İlk release image'ları yalnızca `linux/amd64` platformunda oluşturulmuştu.

Minikube node'unun `arm64` olduğu görüldükten sonra pipeline'a QEMU ve Docker Buildx multi-platform desteği eklendi.

Image'lar artık:

* `linux/amd64`
* `linux/arm64`

platformları için oluşturuluyor.

## Kubernetes

Local Kubernetes ortamı olarak Minikube kullanılıyor.

Uygulama için dört temel resource bulunuyor:

* Backend Deployment
* Backend ClusterIP Service
* Frontend Deployment
* Frontend NodePort Service

Backend yalnızca cluster içinden erişilebilir durumda.

Frontend NodePort üzerinden local tarayıcıdan açılabiliyor.

Frontend'in Kubernetes içerisindeki backend Service'e bağlanarak backend mesajını alabildiği ayrıca kontrol edildi.

## Argo CD

Argo CD Minikube cluster'ında `argocd` namespace'i içerisinde çalışıyor.

`argocd/application.yaml`, Argo CD'ye şu kaynağı takip etmesini söylüyor:

* Repository: `cicd-task`
* Branch: `main`
* Path: `k8s/`
* Destination namespace: `default`

Automated sync açık. Ayrıca `prune` ve `selfHeal` aktif.

Argo CD Application durumu çalışır durumda `Synced` ve `Healthy` olarak doğrulandı.

## Release ve Argo CD Akışı

Release pipeline'ın son hali:

**Git tag → GitHub Actions → Test → Docker Build → GHCR → Kubernetes manifest update → Git main → Argo CD → Kubernetes**

Örneğin `v1.0.2` tag'i oluşturulduğunda GitHub Actions:

1. Backend ve frontend testlerini çalıştırdı.
2. İki servis için `v1.0.2` multi-platform image'larını oluşturdu.
3. Image'ları GHCR'ye gönderdi.
4. `k8s/backend.yaml` ve `k8s/frontend.yaml` içerisindeki image tag'lerini `v1.0.1` değerinden `v1.0.2` değerine güncelledi.
5. Manifest değişikliklerini `main` branch'ine commit ve push etti.
6. GitHub Release oluşturdu.

GitHub Actions Kubernetes'e doğrudan deploy etmiyor. Workflow içerisinde `kubectl apply` veya manuel Argo CD sync işlemi bulunmuyor.

Manifest `main` branch'inde değiştikten sonra Argo CD yeni desired state'i algılayıp Kubernetes Deployment'larını `v1.0.2` image'larına geçirdi.

Argo CD arayüzünde backend Live Manifest içerisinde `ghcr.io/emreeaarslan/cicd-backend:v1.0.2` image'ı görüldü ve uygulama `Synced / Healthy` durumuna geldi.

Son olarak frontend üzerinden backend çağrısı yapıldığında yeni release içerisindeki `Backend service is running - v1.0.2` mesajı alındı.

## GitOps Kontrolü

Argo CD'nin yalnızca `main` branch'ini takip ettiği ayrıca replica değişikliğiyle test edildi.

Backend replica sayısı feature ve `dev` branch'lerinde `2` yapılmasına rağmen cluster `1/1` olarak kaldı.

Değişiklik `main` branch'ine girdikten sonra herhangi bir manuel `kubectl apply` kullanılmadan backend Deployment otomatik olarak `2/2` durumuna geçti.

Bu kontrolle Git'teki desired state ile Kubernetes cluster'ın Argo CD tarafından senkronize edildiği doğrulandı.

## Sorumluluk Ayrımı

**GitHub Actions**

* Testleri çalıştırır.
* Docker image'larını oluşturur.
* Image'ları GHCR'ye gönderir.
* GitHub Release oluşturur.
* Release edilen image version'ını Kubernetes manifestlerine yazar.

**Argo CD**

* `main/k8s` içerisindeki desired state'i takip eder.
* Git değişikliklerini Kubernetes'e uygular.
* Cluster'ı Git repository ile senkronize tutar.

Bu yapıda CI ve release hazırlığı GitHub Actions tarafında, Kubernetes deployment ise Argo CD tarafında yönetiliyor.