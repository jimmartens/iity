FROM node:14

ENV PORT=8000
ENV VITE_API_URL=http://localhost:8000
# ENV VITE_API_URL = https://backend-403359582991.us-central1.run.app

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]