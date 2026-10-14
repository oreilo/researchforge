FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir ".[server]"
RUN useradd -m researcher && mkdir -p /data && chown researcher:researcher /data
USER researcher
ENV RESEARCHFORGE_DB=/data/researchforge.db
EXPOSE 8000
CMD ["uvicorn","oreilo_researchforge.asgi:app","--host","0.0.0.0","--port","8000"]
