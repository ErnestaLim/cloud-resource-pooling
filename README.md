# K8s set up for Website and Database

## Prerequisite:
- Docker Desktop Installed (Kubernetes enabled)
- Minikube Installed

## Setting up pods
1. Run the following in CLI terminal in VS code
      - *kubectl apply -f <_insert the following files_>*
          - web-deployment.yml
          - statefulset-sql.txt
          - web-service.yml
          - mysql-service.yml
2. Check that web and sql pods are running
      - *kubectl get all*
3. Open tunnel in terminal
      - *minikube tunnel*
4. Access web in browser
      - 127.0.0.1:80
