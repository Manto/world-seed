FROM node:20-slim

WORKDIR /app

COPY . .

RUN npm install --include=dev

CMD ["npm", "run", "dev", "--", "--host"]
