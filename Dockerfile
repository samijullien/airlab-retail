FROM shubhaguha/retail_base

# Copy workspace files
WORKDIR /workspace
COPY ./ ./

# Install Python dependencies & retail package
RUN python setup.py install \
&& pip install gunicorn

# Run server
EXPOSE 80
CMD [ "gunicorn", "retail.__main__:server", "-b", ":80", "-w", "5" ]
