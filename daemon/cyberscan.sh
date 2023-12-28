#!/usr/bin/env bash
#
# Daemon principal do projeto CyberScan
# Programmer: Renato Kopke
#
# Pacotes (ubuntu):
#       apt-get install python-virtualenv
#       apt-get install libmysqlclient-dev python-dev cmake cmake-extras
#       apt install -y libsm6 libxext6 libsm6 libxrender1 libfontconfig1
#
# Pacotes (Centos 7 ):
#       yum install epel-release
#       yum install python36 python-pip
#       pip3 install -U pip
#       pip3 install -U virtualenv
#       pip3 install gunicorn
#
# Pacotes (AmazonLinux):
#       amazon-linux-extras install epel
#       yum install supervisor
#       yum install epel-release
#       yum install python36 python-pip python3
#       pip install -U pip
#       pip install -U virtualenv
#       yum install gcc python3-devel mysql-devel
#       yum install gcc
#       pip3 install gunicorn
#       yum install cairo pango -y
#
#   CMD: python3 -m venv $VENV
#
DIR_PROJETO="/opt/CyberScan"
VENV="/opt/venv-cyberscan"

PID=/var/run/cyberscan.pid
LOGFILE=/var/log/cyberscan-gunicorn.log

if [ ! -d "$VENV" ]; then
    echo -e "\033[32m\n[ cyberscan ]\033[m - Criando virtualenv em /opt"
    # (ubuntu buster/sid) apt-get install python3-venv

    cd /opt && virtualenv --python=python3.6 $VENV
fi

# Ativando ambiente virtual e executando o gunicorn para este projeto
source $VENV/bin/activate

# Instala pacotes novos no projeto caso exista
cd $DIR_PROJETO
$VENV/bin/pip install --upgrade pip
$VENV/bin/pip install --no-cache-dir -r ./requirements.txt --upgrade

# Configura o makemigrations/migrate e os statics file do projeto
cd $DIR_PROJETO
$VENV/bin/python manage.py makemigrations
$VENV/bin/python manage.py migrate
$VENV/bin/python manage.py collectstatic --noinput

# Usuario/Grupo que vai rodar o gunicorn
USER=root
GROUP=root

# Endereço local que o gunicorn irá rodar
ADDRESS=127.0.0.1:8080

WORKERS_NUM=$((((2 * $(cat /proc/cpuinfo | grep -i processor | wc -l)))+1))
WORKER_CLASS="gthread"

THREADS=$(((2 * $(cat /proc/cpuinfo | grep -i processor | wc -l))))

TIMEOUT=1200
GRACEFUL_TIMEOUT=1200
KEEPALIVE=1200

TIMEOUTS_CFG="--timeout $TIMEOUT --graceful-timeout $GRACEFUL_TIMEOUT --keep-alive $KEEPALIVE"

[ -f $PID ] && rm $PID

exec $VENV/bin/gunicorn \
    -w $WORKERS_NUM \
    --threads $THREADS \
    -k $WORKER_CLASS $TIMEOUTS_CFG \
    --pid=$PID \
    --bind=$ADDRESS \
    --user=$USER \
    --log-level=debug \
    --log-file=$LOGFILE 2>>$LOGFILE core.wsgi:application