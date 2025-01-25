#!/bin/bash

source .env
echo $PROJECT_ID

docker build -t gcr.io/$PROJECT_ID/backend ./backend -f ./backend/Dockerfile.prod
docker push gcr.io/$PROJECT_ID/backend
gcloud run deploy backend --image gcr.io/$PROJECT_ID/backend --project $PROJECT_ID --platform managed --region $REGION --allow-unauthenticated --set-env-vars "PROJECT_ID=$PROJECT_ID" --set-secrets="FIRESTORE_CREDENTIALS=firestore-key:latest" --port 8080

echo "DONE"
