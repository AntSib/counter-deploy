# Stage 1: build frontend
FROM node:20-alpine AS nodebuild
WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./
COPY frontend/index.html ./
COPY frontend/vite.config.ts ./
COPY frontend/tsconfig.json ./
COPY frontend/src ./src

RUN npm ci
RUN npm run build


# Stage 2: build backend
FROM python:3.12-slim
WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend .

COPY --from=nodebuild /app/dist ./static

ENV FLASK_ENV=production
ENV PORT=8000

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app", "--workers", "2"]
