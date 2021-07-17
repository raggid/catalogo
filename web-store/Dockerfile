FROM node:latest
COPY ./app ./app
WORKDIR /app
RUN yarn install
RUN yarn add fs
RUN yarn build
EXPOSE 3000
CMD ["yarn", "start"]