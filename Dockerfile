# 1. Use the official lightweight Python image from the web registry.
FROM python:3.11-slim

# 2. Configure internal background system environment variables.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 3. Establish the operational directory path inside the container.
WORKDIR /app

# 4. Expose Streamlit's default network port to the outside world
EXPOSE 8501

# 5. Transfer the dependency manifest record from your Mac.
COPY requirements.txt /app/

# 6. Execute an automated system package download pipeline
RUN pip install --no-cache-dir  --upgrade pip && \
    pip install --no-cache-dir  -r requirements.txt

# 7. Copy the rest of your local file architecture into the workspace.
COPY . /app/

# 8. Configure the container to launch the Streamlit server automatically.
# Streamlit Cloud will ignore this line and boot app.py independently on the web panel.
# CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
CMD ["python", "main.py"]
