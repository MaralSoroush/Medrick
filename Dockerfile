FROM python:alpine3.18 AS runner 
RUN sed -isq 's/https/http/g' /etc/apk/repositories
RUN apk add libpq --no-cache

FROM runner as builder
RUN apk add build-base libpq-dev --no-cache

WORKDIR /app
COPY  requirements.txt .
RUN python -m venv .venvDocker && .venvDocker/bin/pip --timeout=10000 install -r requirements.txt  --no-cache-dir \
    && find /app/.venvDocker \( -type d -a -name test -o -name tests \) -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' \+

FROM runner
WORKDIR /app
COPY --from=builder /app /app
COPY . .
ENV PATH="/app/.venvDocker/bin:$PATH"
EXPOSE 8000
RUN chmod +x entrypoint*
ENTRYPOINT ["./entrypoint.sh" ]