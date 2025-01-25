#!/bin/bash

source .env
echo $PROJECT_ID

docker build -t gcr.io/$PROJECT_ID/frontend ./frontend -f ./frontend/Dockerfile.prod
docker push gcr.io/$PROJECT_ID/frontend
gcloud run deploy frontend --image gcr.io/$PROJECT_ID/frontend --project $PROJECT_ID --platform managed --region $REGION --allow-unauthenticated --port 3000

echo "DONE"
