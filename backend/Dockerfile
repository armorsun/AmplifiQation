FROM python:3.10-slim-buster AS builder

RUN apt update && \
	apt install -y libpq-dev python3-dev gcc && \
	rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.10-slim-buster

COPY --from=builder /opt/venv /opt/venv

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
 	PATH="/opt/venv/bin:$PATH"

WORKDIR /code
COPY . /code/

CMD ["flask", "run"]
