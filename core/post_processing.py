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


import pandas as pd
from glob import glob
import os, shutil
import argparse
from cerebralcortex.core.config_manager.config import Configuration


def post_process(config: dict):
    """
    This will merge all stream quality data to one csv file per participant

    """
    csv_files_path = config["output"]["folder_path"]+"/"+config["reports"]["data_yield_per_day"]+"/"
    all_files = glob(csv_files_path+"*.csv")

    usernames = []
    dfs = []
    ext = ".csv"
    motionsense_left_led = "_motionsense_left_led"+ext
    motionsense_right_led = "_motionsense_right_led"+ext
    motionsense_left_accel = "_motionsense_left_accel"+ext
    motionsense_right_accel = "_motionsense_right_accel"+ext
    autosense_ble = "_autosense_ble_accel"+ext
    autosense_respiration = "_autosense_ble_respiration"+ext

    for file_name in all_files:
        usernames.append(file_name.split("/")[-1].split("_")[0])
    usernames = list(set(usernames))

    merged_file_path = csv_files_path+"/merged/"
    if not os.path.exists(merged_file_path):
        os.mkdir(merged_file_path)
    else:
        shutil.rmtree(merged_file_path)
        os.mkdir(merged_file_path)

    for username in usernames:
        mll = csv_files_path+username+motionsense_left_led
        mrl = csv_files_path+username+motionsense_right_led
        mla = csv_files_path+username+motionsense_left_accel
        mra = csv_files_path+username+motionsense_right_accel
        ab = csv_files_path+username+autosense_ble
        ar = csv_files_path+username+autosense_respiration

        files = [mll, mrl, mla, mra, ab, ar]
        for f in files:
            if os.path.exists(f):
                dfs.append(pd.read_csv(f))

        merged = pd.concat([df for df in dfs],axis=1)


        merged.to_csv(merged_file_path+username+".csv", sep=",")




if __name__ == '__main__':
    # create and load CerebralCortex object and configs
    parser = argparse.ArgumentParser(description='CerebralCortex Kafka Message Handler.')
    parser.add_argument("-cr", "--cr_reporting_config_filepath", help="mDebugger configuration file path", required=True)
    args = vars(parser.parse_args())

    # load data reporting configs
    cr_config_file = args["cr_reporting_config_filepath"]
    cr_config = Configuration(cr_config_file).config

    post_process(cr_config)