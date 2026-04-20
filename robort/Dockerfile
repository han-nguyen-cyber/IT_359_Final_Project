FROM python:3.11-slim

# Set the working directory within the container
WORKDIR /app

# Copy the local project files into the container's working directory
COPY . .

# Install dependencies using --no-cache-dir to keep the image size small
# Dependencies are listed explicitly to ensure version consistency
RUN pip install --no-cache-dir \
    requests \ # Communicator: Allows us to send requests to a web server, communicate with AI API, and fetch HTML from targeted websites.
    beautifulsoup4 \ # Scraper: Library for parsing HTML and XML documents, extracts data from HTML tags. To find vulnerabilities, we use BS4 to look for specific tags, like <form> or <input>, to identify potential attack vectors.
    colorama \ # Purely for UX: Produces colored terminal text
    tabulate \ # Tables: Takes data and formats it into visually-pleasing, human-readable tables
    python-dotenv # Loads secret API key

# Define the default command to run when the container starts
CMD ["python", "main.py"]