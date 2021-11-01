# Credit to OpenWPM

FROM krallin/ubuntu-tini:bionic

SHELL ["/bin/bash", "-c"]

# Update ubuntu and setup conda
# adapted from: https://hub.docker.com/r/conda/miniconda3/dockerfile
RUN sed -i'' 's/archive\.ubuntu\.com/us\.archive\.ubuntu\.com/' /etc/apt/sources.list
RUN apt-get clean -qq \
    && apt-get clean -qq \
    && apt-get update -qq \
    && apt-get upgrade -qq \
    # git and make for `npm install`, wget for `install-miniconda`
    && apt-get install wget git make -qq libgtk-3-0 libx11-xcb1 libdbus-glib-1-2 libxt6 xvfb postgresql-client -y -qq \
    && rm -r /var/lib/apt/lists/* -vf

ENV HOME /opt
WORKDIR /opt
RUN git clone https://github.com/mozilla/OpenWPM
WORKDIR /opt/OpenWPM
RUN ./scripts/install-miniconda.sh
ENV PATH $HOME/miniconda/bin:$PATH

# Install OpenWPM -> OpenWPM needs this way for git stuff

RUN ./install.sh
ENV PATH $HOME/miniconda/envs/openwpm/bin:$PATH
RUN conda install pip pandas -y && pip3 install tranco psycopg2-binary SQLAlchemy

# Move the firefox binary away from the /opt/OpenWPM root so that it is available if
# we mount a local source code directory as /opt/OpenWPM
RUN mv firefox-bin /opt/firefox-bin
ENV FIREFOX_BINARY /opt/firefox-bin/firefox-bin

COPY run.sh .
COPY main.py .
COPY webs.py .
COPY top-1m.csv .

COPY sql/insert.py .

# Our work starts here
# Setting demo.py as the default command
CMD [ "bash", "run.sh" ]

# TODO Create volumen on SSD for /opt/data