# Copyright (c) 2017, MD2K Center of Excellence
# - Nasir Ali <nasir.ali08@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import uuid
import argparse

from cerebralcortex.cerebralcortex import CerebralCortex
from cerebralcortex.core.util.spark_helper import get_or_create_sc
from cerebralcortex.core.config_manager.config import Configuration
from core.data_yield import compute_data_yield

def all_users_data_test(study_name: str, reporting_config, CC):
    """
    Generate report for all participants
    :param study_name:
    """
    # get all participants' name-ids
    all_users = CC.get_all_users(study_name)

    if all_users:
        for user in all_users:
            generate_report(user["identifier"], user["username"], CC, reporting_config)
    else:
        print(study_name, "- study has 0 users.")

def one_user_data(user_id: uuid, reporting_config, CC, spark_context):
    # get all streams for a participant
    """
    Generate report for one participant only
    :param user_id: list containing only one
    """
    if user_id:
        rdd = spark_context.parallelize([user_id])
        results = rdd.map(
            lambda user: generate_report(user, CC, reporting_config))
        results.count()
    else:
        print("User id cannot be empty.")


def all_users_data(study_name: str, reporting_config, CC, spark_context):
    """
    Generate report for all participants
    :param study_name:
    """
    # get all participants' name-ids
    all_users = CC.get_all_users(study_name)

    if all_users:
        rdd = spark_context.parallelize(all_users)
        results = rdd.map(
            lambda user: generate_report(user["identifier"], CC, reporting_config))
        results.count()
    else:
        print(study_name, "- study has 0 users.")


def generate_report(user_id: uuid, username: str, CC: CerebralCortex, config: dict):
    """
    Contains pipeline execution of all the reports
    :param user_id:
    :param CC:
    :param config:
    """

    # get all the streams belong to a participant
    streams = CC.get_user_streams(user_id)
    if streams and len(streams) > 0:

        # Data Yield
        if config["input_stream"]["motionsense_hrv_led_quality_left"] in streams:
            compute_data_yield(streams[config["input_stream"]["motionsense_hrv_led_quality_left"]]["identifier"], username,"left", CC, config)

        if config["input_stream"]["motionsense_hrv_led_quality_right"] in streams:
            compute_data_yield(streams[config["input_stream"]["motionsense_hrv_led_quality_right"]]["identifier"], username, "right", CC, config)



if __name__ == '__main__':
    # create and load CerebralCortex object and configs
    parser = argparse.ArgumentParser(description='CerebralCortex Kafka Message Handler.')
    parser.add_argument("-cc", "--cc_config_filepath", help="Configuration file path", required=True)
    parser.add_argument("-cr", "--cc_reporting_config_filepath", help="mDebugger configuration file path", required=True)
    parser.add_argument("-sn", "--study_name", help="mDebugger configuration file path", required=True)
    args = vars(parser.parse_args())

    CC = CerebralCortex(args["cc_config_filepath"])

    # load data reporting configs
    cr_config = Configuration(args["cc_reporting_config_filepath"]).config

    # get/create spark context
    #spark_context = get_or_create_sc(type="sparkContext")

    # run for all the participants in a study
    #all_users_data("mperf", md_config, CC, spark_context)

    #TESTING
    all_users_data_test(args["study_name"], cr_config, CC)
