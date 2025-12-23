 # 🚀 Kubernetes Microservice Project

This repository contains a **small but realistic 3-tier microservice application** that you can use for:

- ✅ Learning **Docker + Kubernetes** end-to-end  
- ✅ Showcasing **production-style manifests and CI** in interviews  
- ✅ Adding **solid DevOps / Kubernetes bullet points** to your resume  

---

## 🧱 The Stack

- **Frontend:** Static HTML/CSS served by **Nginx**, calling the backend via `/api`  
- **Backend:** **Python Flask REST API** exposing `/health` and `/users`  
- **Database:** **PostgreSQL** with a simple `users` table  
- **Platform:** **Kubernetes** (namespace, deployments, services, ingress, HPA)  
- **CI:** **GitHub Actions** building Docker images on each push to `main`  

---

## 🧭 How to Use This Repo

- Clone the repo and run everything locally with **Docker Compose**  
- Once comfortable, apply the manifests to a **Kubernetes cluster** (kind, minikube, k3s, managed cloud)  
- Use the code and YAML files as **interview talking points**  

---

## 📁 Folder Structure (High Level)

- `app/frontend/` — static site, Nginx config, and Dockerfile  
- `app/backend/` — Flask API, requirements, and Dockerfile  
- `k8s/` — Kubernetes manifests (namespace, deployments, services, ingress, HPA, config, secrets)  
- `.github/workflows/` — CI pipeline building Docker images  
- `docker-compose.yml` — local multi-container test  

---

## 🗂️ Project Structure (Detailed)

```text
k8s-3tier-microservice-app/
├── app/
│   ├── frontend/
│   │   ├── index.html
│   │   ├── styles.css
│   │   ├── nginx.conf
│   │   └── Dockerfile
│   └── backend/
│       ├── app.py
│       ├── requirements.txt
│       └── Dockerfile
├── k8s/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── postgres-deployment.yaml
│   ├── postgres-service.yaml
│   ├── ingress.yaml
│   └── hpa.yaml
├── .github/
│   └── workflows/
│       └── docker-ci.yml
├── docker-compose.yml
└── README.md



---

## 🐳 Run Locally with Docker Compose

**Requirements:** Docker + Docker Compose

```bash
docker compose up --build

-Frontend: http://localhost:8080
-Backend Health: http://localhost:5000/health
-Users API: http://localhost:5000/users

🔄 What Happens Locally

-postgres-service starts first with the usersdb database
-backend-service (Flask) connects to Postgres and exposes the REST API on port 5000
-frontend-service (Nginx) serves index.html on port 8080 and proxies /api/* to the backend

☸️ Deploy to Kubernetes (Quick Start)

You need a running Kubernetes cluster and kubectl configured (kind, minikube, etc.).
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/postgres-deployment.yaml -f k8s/postgres-service.yaml
kubectl apply -f k8s/backend-deployment.yaml -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml -f k8s/frontend-service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml

🌐 Accessing the Application

Ensure an nginx Ingress controller is installed in the cluster  
Map k8s.local to the cluster IP using the hosts file  

Linux or Mac  
/etc/hosts  

Windows  
C:\Windows\System32\drivers\etc\hosts  

Open in browser  
http://k8s.local

⚙️ What Kubernetes Is Managing

Deployments  
Frontend backend and Postgres  
Frontend and backend run with multiple replicas  

Services  
ClusterIP services for backend and Postgres used for internal communication  
Ingress used to expose frontend and backend API externally  

Configuration  
ConfigMap used for non sensitive application configuration  
Secret used for database credentials  

Ingress Routing  
Requests to /api are routed to the backend service  
All other requests are routed to the frontend service  

Horizontal Pod Autoscaler  
Backend automatically scales from 2 to 5 replicas based on CPU utilization

---

🔁 ## GitHub Actions CI (What It Does)

- Triggers on **push to `main`**.
- Builds **frontend** and **backend** Docker images using `docker/build-push-action`.
- Runs on **GitHub-hosted runners**; it **does not deploy** or push images (CI only).

You can extend this with:

- Image pushes to Docker Hub or GHCR.
- A separate CD pipeline that applies the Kubernetes manifests.

---

🎯 ## Interview Talking Points

- **What Kubernetes manages:** Pods for frontend/back-end/DB, Services for stable networking, ConfigMap/Secret for configuration, and Ingress for external routing.
- **Why Services and Ingress:** Services provide internal discovery and stable virtual IPs; Ingress exposes a single entrypoint with path-based routing to frontend and API.
- **Auto-scaling:** HPA monitors CPU and scales backend replicas between 2–5 pods to handle load.
- **CI role:** GitHub Actions validates Docker builds on every push to prevent broken images.
- **Security/config:** Separate ConfigMap for non-sensitive settings and Secret for credentials; images use slim base images.
---


