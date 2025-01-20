FROM node:14

ENV ENVIRONMENT=dev
ENV PORT=8000
ENV VITE_API_URL=http://localhost:8000

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]