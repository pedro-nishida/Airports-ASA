#!/bin/bash

# Definir variáveis
IMAGE_NAME="app"
TAG="latest"
REGISTRY="localhost:5000"  # Ajuste para seu registry se estiver usando um externo

# Limpar imagens anteriores com o mesmo nome (opcional)
echo "Removendo imagens antigas (se existirem)..."
docker rmi $IMAGE_NAME:$TAG 2>/dev/null || true
docker rmi $REGISTRY/$IMAGE_NAME:$TAG 2>/dev/null || true

# Construir a imagem Docker
echo "Construindo a imagem Docker..."
docker build -t $IMAGE_NAME:$TAG .

# Verificar se a construção foi bem-sucedida
if [ $? -ne 0 ]; then
    echo "Falha ao construir a imagem Docker."
    exit 1
fi

# Adicionar tag para publicação
echo "Adicionando tag para o registro..."
docker tag $IMAGE_NAME:$TAG $REGISTRY/$IMAGE_NAME:$TAG

# Publicar imagem no registro (se necessário)
# echo "Publicando imagem no registro..."
# docker push $REGISTRY/$IMAGE_NAME:$TAG

echo "Imagem construída com sucesso"
echo "Para usar no Kubernetes, aplique os manifestos com: kubectl apply -f k8s/deployment.yaml"
echo "Para testar localmente, você pode executar: docker run -p 5000:5000 $IMAGE_NAME:$TAG"

# Lista as imagens criadas
echo "Imagens disponíveis:"
docker images | grep $IMAGE_NAME
