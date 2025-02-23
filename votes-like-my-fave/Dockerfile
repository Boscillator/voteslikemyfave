
FROM node:18-alpine

WORKDIR /app

# Install NPM packages
COPY package.json  package-lock.json ./
RUN npm ci

ENV NODE_ENV=production
CMD ["npm", "build"]
