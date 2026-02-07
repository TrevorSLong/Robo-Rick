FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY RoboRickFull.py .
COPY adminchannels.JSON .
COPY welcomechannels.JSON .

# Run the bot
CMD ["python", "RoboRickFull.py"]
