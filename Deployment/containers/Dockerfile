FROM centos:centos7
MAINTAINER The CentOS Project <cloud-ops@centos.org>

RUN yum -y update; yum clean all
RUN yum -y install epel-release
RUN yum -y install python-pip
RUN pip install --upgrade pip
RUN pip install Flask oslo_utils webob flask_sqlalchemy oslo_db flask_script flask_migrate flask_restful
RUN yum -y install git
RUN git clone https://github.com/opentechfn/medhavi.git

EXPOSE 8000
CMD ["python", "/medhavi/wsgi.py"]