# ── Base image ─────────────────────────────────────────────────────────────
FROM python:3.9-slim

# ── Working directory ───────────────────────────────────────────────────────
WORKDIR /app

# ── Install dependencies ────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy project files ──────────────────────────────────────────────────────
COPY app.py          .
COPY model.pkl       .
COPY similarity.pkl  .
COPY templates/      ./templates/

# ── Expose port ─────────────────────────────────────────────────────────────
EXPOSE 5000

# ── Run the Flask app ───────────────────────────────────────────────────────
CMD ["python", "app.py"]
