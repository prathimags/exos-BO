FROM centos/systemd
RUN mkdir /run/systemd/system
CMD ["/usr/sbin/init"]
RUN yum -y install initscripts && yum clean all
RUN yum -y update
RUN yum install -y python39
RUN yum install -y git

RUN git clone https://github.com/prathimags/exos-blueocean.git /opt/exos/
WORKDIR /opt/exos/

RUN pip3 install -r requirements.txt

RUN pytest --html=./ reports/report-summitlite-arm_435_staging.html --tc-file=". /Config_files/device_summitarm_lite_x435.yaml" --tc-file=". /Config_files/topo.test.staging.yaml" ./test_exos_relsanity.py
