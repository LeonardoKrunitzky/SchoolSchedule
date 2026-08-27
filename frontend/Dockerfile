FROM node:20-alpine

WORKDIR /app

# Copia os arquivos de dependência primeiro (otimiza o cache do Docker)
COPY package.json package-lock.json ./
RUN npm install

# Copia o restante do projeto
COPY . .

# Faz o build de produção do Next.js
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]