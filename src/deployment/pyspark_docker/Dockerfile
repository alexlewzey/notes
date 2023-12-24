FROM apache/spark:3.4.2-scala2.12-java11-python3-r-ubuntu

COPY pyspark_job.py .

ENV PATH="/opt/spark/bin:${PATH}"

# enter a spark session in the terminal
# ENTRYPOINT ["/opt/spark/bin/pyspark"]

# run the spark job on start up
CMD [ "spark-submit", "pyspark_job.py" ]
