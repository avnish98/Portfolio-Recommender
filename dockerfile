FROM puckel/docker-airflow
RUN pip3 install pyportfolioopt pandas numpy
RUN pip3 install alpha_vantage
ADD keyfile.txt keyfile.txt
ADD fetcher.py fetcher.py
CMD ["python", "fetcher.py", "MSFT", "GOOG", "FB", "TWTR", "TSLA"]