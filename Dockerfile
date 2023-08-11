# app/Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

# Expose ports for both Streamlit and Flask
EXPOSE 8501
EXPOSE 5001

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Copy and set the start script as executable
COPY start.sh .
RUN chmod +x start.sh

# Use the start script as the default command to run
CMD ["./start.sh"]
