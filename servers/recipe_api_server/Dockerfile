# Recipe API MCP Server Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy shared utilities first (for better caching)
COPY shared/ ./shared/

# Copy root requirements first
COPY requirements.txt ./root-requirements.txt

# Copy recipe server requirements and install dependencies
COPY servers/recipe_api_server/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r root-requirements.txt && \
    pip install --no-cache-dir beautifulsoup4>=4.12.0 lxml>=4.9.0

# Copy recipe server source code
COPY servers/recipe_api_server/src/ ./src/

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Expose port (though MCP uses stdio, this is for future HTTP interface)
EXPOSE 8000

# Run the MCP server
CMD ["python", "src/main.py"]