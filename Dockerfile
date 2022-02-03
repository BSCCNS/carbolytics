FROM openwpm/openwpm:0.17.0

WORKDIR /opt/OpenWPM/
ENV OPT /opt/OpenWPM/

COPY *.py ${OPT}
COPY *.txt ${OPT}
COPY sql/*.py ${OPT}
# COPY top-1m.csv .

RUN /opt/miniconda/envs/openwpm/bin/pip install -r requirements.txt

CMD ["/opt/miniconda/envs/openwpm/bin/python", "main.py"]
