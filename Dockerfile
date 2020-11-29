FROM shubhaguha/retail_base

# Copy workspace files
WORKDIR /workspace
COPY ./ ./

# Install Python dependencies & retail package
RUN python setup.py install

# Run server
EXPOSE 8050
CMD [ "python", "-m", "retail" ]
