FROM node:latest
COPY ./app .
RUN yarn install
EXPOSE 80
CMD ["node", "server.js"]