# install and build
FROM node:16-alpine AS build

WORKDIR /usr/app/src

COPY ./package.json .
RUN npm install --legacy-peer-deps

COPY . .
RUN npm run build

# copy build to serve it later

FROM node:16-alpine

WORKDIR /usr/app/src
COPY --from=build /usr/app/src/build ./build
