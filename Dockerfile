# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the source code from the local volume into the container
COPY src /app/src

# Navigate inside the source code directory
WORKDIR /app/src

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run report_builder.py
CMD ["python", "build_reports.py"]
