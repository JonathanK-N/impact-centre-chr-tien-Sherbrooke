FROM node:18-alpine

WORKDIR /app

# Copier les fichiers du backend
COPY impact-centre-mobile/backend/package*.json ./
RUN npm install --production

COPY impact-centre-mobile/backend/ ./
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]