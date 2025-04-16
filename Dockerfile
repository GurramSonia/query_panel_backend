#FROM python:3.9
FROM python:3.13.1-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org -r requirements.txt


# Copy the application files
COPY . /app

# Expose the port and run the Flask app
EXPOSE 5000
CMD ["python", "app.py"]