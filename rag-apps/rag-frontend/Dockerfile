FROM node:18-alpine
RUN apk --no-cache add curl

# Create user
RUN adduser -u 1024 -h /cserve_user -D -s /bin/bash cserve_user \
	&& chown -R cserve_user:cserve_user /cserve_user

# Switch to non-root user by id for Kuberetes pod security standard - restricted
USER 1024

RUN mkdir /cserve_user/app
WORKDIR /cserve_user/app

COPY --chown=cserve_user package.json .
RUN npm install

COPY --chown=cserve_user . .

EXPOSE 3000

CMD [ "npm", "run", "dev"]
