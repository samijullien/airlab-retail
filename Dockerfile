FROM shubhaguha/retail_base

# Copy workspace files
WORKDIR /workspace
COPY ./ ./

# Install Python dependencies & retail package
RUN python setup.py install \
&& pip install gunicorn

# Run server
EXPOSE 80
ENTRYPOINT [ "gunicorn", "retail.__main__:server", "--bind", ":80", "--workers", "5", "--log-level", "info" ]
