FROM node:22-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y chromium
ENV CHROME_BIN=/usr/bin/chromium

COPY package*.json ./

RUN npm install
RUN npm install -g @angular/cli

COPY . .

EXPOSE 4200

CMD ["ng", "serve", "--host", "0.0.0.0", "--poll", "2000"]