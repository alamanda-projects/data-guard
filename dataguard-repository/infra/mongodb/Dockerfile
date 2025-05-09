FROM mongo:7.0.4-jammy

ARG MONGODB_USER
ARG MONGODB_PASS
ENV MONGO_INITDB_ROOT_USERNAME=${MONGODB_USER}
ENV MONGO_INITDB_ROOT_PASSWORD=${MONGODB_PASS}

# Create a non-root user
RUN adduser --system --no-create-home --shell /bin/bash --uid 1000 yellow

WORKDIR /data/db
RUN chown -R yellow /data/db

# Specify the user to run the application
USER yellow

CMD ["mongod"]