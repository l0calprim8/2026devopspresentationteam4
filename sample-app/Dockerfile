FROM python
WORKDIR /
RUN python -m pip install --no-cache-dir flask mysql-connector-python
RUN python -m pip install --no-cache-dir --progress-bar off flask
RUN python -m pip install --no-cache-dir --progress-bar off pytest
COPY . .  
COPY  sample_app.py ./
RUN mkdir -p ./uploads
EXPOSE 8080
CMD ["python3","sample_app.py"] 
