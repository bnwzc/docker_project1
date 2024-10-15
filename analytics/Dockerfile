FROM node:current
WORKDIR /app
COPY package.json .
RUN npm install
RUN apt-get update
RUN apt-get install -y default-mysql-client
COPY . .
EXPOSE 5002
CMD ["node", "app.js"]
