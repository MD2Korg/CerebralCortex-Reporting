#!/usr/bin/env bash

# Python3 path
export PYSPARK_PYTHON=/usr/bin/python3

# export CerebralCortex path if CerebralCortex is not installed
export PYTHONPATH="${PYTHONPATH}:/home/ali/IdeaProjects/CerebralCortex-2.0/"

#Spark path
export SPARK_HOME=/home/ali/spark/spark-2.2.0-bin-hadoop2.7/

#set spark home
export PATH=$SPARK_HOME/bin:$PATH

# path of cc configuration path
CC_CONFIG_FILEPATH="/home/ali/IdeaProjects/CerebralCortex-2.0/cerebralcortex/core/resources/cc_configuration.yml"
# data directory where all gz and json files are stored
REPORTS_CONFIG="/home/ali/IdeaProjects/CerebralCortex-Reports/reports_config.yml"
# how often CC-kafka shall check for new messages (in seconds)
STUDY_NAME="mperf"

# spark master
SPARK_MASTER="local[*]"

spark-submit main.py -cc $CC_CONFIG_FILEPATH -cr $REPORTS_CONFIG -sn $STUDY_NAME -spm $SPARK_MASTER