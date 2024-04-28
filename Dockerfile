FROM python:3.10
WORKDIR /app

COPY requirements.txt requirements.txt

# Upgrade pip and set a mirror source for pip installations
RUN pip install --upgrade pip && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]
