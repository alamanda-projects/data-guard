FROM mongo:7.0.4-jammy

# Create a non-root user
RUN adduser --system --no-create-home --shell /bin/bash --uid 1000 dgr_user

ENV MONGO_INITDB_ROOT_USERNAME=root
ENV MONGO_INITDB_ROOT_PASSWORD=example

WORKDIR /data/db

# Specify the user to run the application
USER dgr_user

CMD ["mongod"]