FROM python:3.11-slim

# Set working directory
WORKDIR /sudoku

# Copy app files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (optional, for documentation)
EXPOSE 5000

# Run your app
CMD ["python", "sudoku.py"]