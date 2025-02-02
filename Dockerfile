FROM postgres:latest

ENV POSTGRES_PASSWORD="22Gjvbljhf@@"

VOLUME ["/var/lib/postgresql/data"]

CMD ["postgres"]
