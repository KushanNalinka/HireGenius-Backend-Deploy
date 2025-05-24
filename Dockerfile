# # ---------- Base image ----------
# FROM python:3.12-slim

# # ---------- OS tools we need ----------
# RUN apt-get update \
#  && apt-get install -y --no-install-recommends curl \
#  && rm -rf /var/lib/apt/lists/*

# # ---------- Python flags ----------
# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1

# # ---------- Python packages ----------
# # ---------- Python packages ----------
# COPY requirements.txt /tmp/requirements.txt
# RUN pip install --upgrade pip \
#  && pip install --no-cache-dir -r /tmp/requirements.txt \
#  && pip install --no-cache-dir --upgrade numpy pandas


# # ---------- Copy application ----------
# WORKDIR /code
# COPY app          ./app
# COPY local_model  ./local_model
# COPY startup.sh   .

# RUN chmod +x startup.sh

# EXPOSE 8000
# CMD ["./startup.sh"]


FROM python:3.12-slim

# curl (optional) + cleanup
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# install core deps + transformers
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r /tmp/requirements.txt \
 && pip install --no-cache-dir sentence-transformers transformers

WORKDIR /code
COPY app       ./app
COPY startup.sh .
RUN chmod +x startup.sh

EXPOSE 8000
CMD ["./startup.sh"]
