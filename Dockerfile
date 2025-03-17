# Step 1: Use official Python image as the base image
FROM python:3.9-slim

# Step 2: Set environment variables (for your API keys and app configurations)
# Replace with the actual variable names from your .env file or Docker secrets
ENV APIFY_API_TOKEN=<your_apify_api_token>
ENV OPENAI_API_KEY=<your_openai_api_key>

# Step 3: Set the working directory inside the container
WORKDIR /usr/src/app

# Step 4: Copy the requirements file into the container
# If you have a requirements.txt, use this to install dependencies
COPY requirements.txt ./

# Step 5: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the rest of your project files into the container
COPY main.py ./

# Step 7: Install additional system dependencies (if any)
# For example, if you need libraries like curl or others, you can install them here
RUN apt-get update && apt-get install -y curl

# Step 8: Expose the port (if your agent exposes any ports for API or web)
# EXPOSE 8080  # Uncomment if you're running a web service

# Step 9: Define the command to run the job search agent
CMD ["python", "main.py"]