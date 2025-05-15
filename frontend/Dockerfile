FROM node:18-alpine

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./

RUN npm install

COPY ./src ./src
COPY ./public ./public

RUN npm run build

# Use an nginx server to serve the built static files
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html

EXPOSE 80
EXPOSE 5000

CMD ["nginx", "-g", "daemon off;"]
