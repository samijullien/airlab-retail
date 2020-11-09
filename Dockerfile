FROM python:3.7

# Install R system dependencies
RUN apt-get update \
&& apt-get install -y r-base r-base-dev libgsl-dev

# Copy workspace files
WORKDIR /workspace
COPY ./ ./

# Install R dependencies
RUN wget -P /tmp \
    https://cran.r-project.org/src/contrib/colorspace_1.4-1.tar.gz \
    https://cran.r-project.org/src/contrib/gsl_2.1-6.tar.gz \
    https://cran.r-project.org/src/contrib/ADGofTest_0.3.tar.gz \
    https://cran.r-project.org/src/contrib/stabledist_0.7-1.tar.gz \
    https://cran.r-project.org/src/contrib/mvtnorm_1.1-1.tar.gz \
    https://cran.r-project.org/src/contrib/pcaPP_1.9-73.tar.gz \
    https://cran.r-project.org/src/contrib/pspline_1.0-18.tar.gz \
    https://cran.r-project.org/src/contrib/numDeriv_2016.8-1.1.tar.gz \
    https://cran.r-project.org/src/contrib/copula_1.0-0.tar.gz \
&& R CMD INSTALL \
    /tmp/colorspace_1.4-1.tar.gz \
    /tmp/gsl_2.1-6.tar.gz \
    /tmp/ADGofTest_0.3.tar.gz \
    /tmp/stabledist_0.7-1.tar.gz \
    /tmp/mvtnorm_1.1-1.tar.gz \
    /tmp/pcaPP_1.9-73.tar.gz \
    /tmp/pspline_1.0-18.tar.gz \
    /tmp/numDeriv_2016.8-1.1.tar.gz \
    /tmp/copula_1.0-0.tar.gz

# Install Python dependencies
RUN python setup.py develop

# Run server
EXPOSE 8050
CMD [ "python", "app.py" ]
