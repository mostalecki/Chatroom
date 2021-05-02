FROM node:15.10.0-alpine as development
RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app
WORKDIR /home/node/app
RUN npm install -g @angular/cli
COPY ./package.json ./package-lock.json ./
RUN npm install
COPY . ./
CMD ["npm", "start"]

FROM node:15.10.0-alpine as builder
WORKDIR /home/node/app
COPY --from=development /home/node/app /home/node/app
RUN node_modules/.bin/ng build --aot --prod --output-hashing none

FROM nginx:latest as production
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /home/node/app/dist /home/node/app/dist
