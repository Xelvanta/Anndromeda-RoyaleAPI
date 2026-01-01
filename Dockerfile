# Use a slim Python base image
FROM python:3.13-slim

# 1. Install System Dependencies for both Node.js and Chrome
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Install Node.js dependencies
COPY package.json package-lock.json .
RUN npm ci

# 4. Tell Puppeteer to download Chrome during build
RUN npx puppeteer browsers install chrome

# 5. Copy rest of application code
COPY . .

# 6. Expose the port
EXPOSE 5000

# 7. Start the application
CMD ["python", "app.py"]
