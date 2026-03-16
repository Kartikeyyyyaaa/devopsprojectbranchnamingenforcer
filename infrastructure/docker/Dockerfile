FROM python:3.11-slim

LABEL maintainer="Kartikeya Aryan Mishra <23FE10CSE00736>"
LABEL description="Branch Naming Convention Enforcer"
LABEL version="1.0.0"

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src/ ./src/
COPY tests/ ./tests/

# Make CLI executable
RUN chmod +x src/main/python/branch_enforcer.py

# Default: show help
ENTRYPOINT ["python", "src/main/python/branch_enforcer.py"]
CMD ["--help"]
