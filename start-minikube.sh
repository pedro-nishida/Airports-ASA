#!/bin/bash

# Verificar se o Minikube está instalado
if ! command -v minikube &> /dev/null; then
    echo "Minikube não encontrado. Instalando Minikube..."
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube
    rm minikube-linux-amd64
fi

# Verificar se o kubectl está instalado
if ! command -v kubectl &> /dev/null; then
    echo "kubectl não encontrado. Instalando kubectl..."
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    rm kubectl
fi

# Iniciar Minikube com o driver Docker
echo "Iniciando Minikube com o driver Docker..."
minikube start --driver=docker

# Configurar o contexto do kubectl
echo "Configurando o kubectl para usar o Minikube..."
kubectl config use-context minikube

# Construir a imagem Docker localmente
echo "Construindo imagem Docker localmente..."
docker build -t app:latest .

# Configurar Docker para usar o registro do Minikube
echo "Configurando Docker para usar o ambiente do Minikube..."
eval $(minikube -p minikube docker-env)

# Reconstruir a imagem dentro do Minikube para que esteja disponível no cluster
echo "Reconstruindo imagem no registro interno do Minikube..."
docker build -t app:latest .
docker tag app:latest localhost:5000/app:latest

# Verificar se há imagens criadas
echo "Verificando imagens Docker criadas:"
docker images | grep app

# Aplicar os manifestos Kubernetes
echo "Aplicando manifestos Kubernetes..."
kubectl apply -f k8s/deployment.yaml

# Aguardar até que todos os pods estejam prontos
echo "Aguardando os pods ficarem prontos..."
kubectl wait --for=condition=ready pod --all --timeout=120s

# Expor o serviço app-service
echo "Expondo o serviço app-service..."
minikube service app-service --url

echo "Configuração concluída! Você pode acessar o aplicativo pela URL acima."
echo "Para acessar o RabbitMQ management, execute: minikube service rabbitmq --url"
echo "Para verificar os pods em execução, execute: kubectl get pods"
