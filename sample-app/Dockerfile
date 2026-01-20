FROM python
WORKDIR /
RUN python -m pip install --no-cache-dir --progress-bar off flask
COPY static  ./static 
COPY templates ./templates 
COPY  sample_app.py ./
RUN mkdir -p static/uploads
EXPOSE 8080
CMD ["python3","sample_app.py"] 
