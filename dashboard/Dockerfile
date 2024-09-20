
FROM python:latest

WORKDIR /dashboard
RUN mkdir pages
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY homepage.py .
COPY graphs.py .
COPY pages/about.py ./pages
COPY pages/transaction_analysis.py ./pages
COPY pages/truck_revenue.py ./pages

CMD ["streamlit", "run", "homepage.py"]