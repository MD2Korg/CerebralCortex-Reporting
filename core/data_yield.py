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
import os
from collections import OrderedDict
from util.util import seconds_to_hours
from cerebralcortex.cerebralcortex import CerebralCortex
from cerebralcortex.core.util.streams import get_stream_days
from cerebralcortex.core.data_manager.raw.stream_handler import DataSet

def compute_data_yield(stream_id: uuid, username:str, wrist:str, CC: CerebralCortex, config: dict):
    """
    This uses LED quality stream to calculate total good quality data for each data
    LED quality stream has data quality available for 3 second windows

    """
    data_dir = config["output"]["folder_path"]+"/"+config["reports"]["data_yield_per_day"]+"/"
    data_yield_report = data_dir+username+"_"+wrist+".csv"
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
        os.mknod(data_yield_report)

    stream_days = get_stream_days(stream_id, CC)

    with open(data_yield_report, "w") as report:
        report.write("day, good hours, total hours \n")
        for day in stream_days:
            # load stream data
            raw_stream = CC.get_stream(stream_id, day=day, data_type=DataSet.COMPLETE)

            if len(raw_stream.data) > 0:
                results = process_stream(raw_stream.data)
                results = str(day)+","+results
                report.write(results)


def process_stream(data: OrderedDict) -> OrderedDict:
    """
    :param data:
    :param config:
    :return:
    """
    good = 0
    noise = 0
    bad = 0
    band_off = 0
    missing = 0
    not_worn = 0
    band_loose = 0

    for dp in data:
        if dp.sample==0.0:
            good += 1
        elif dp.sample==1.0:
            noise += 1
        elif dp.sample==2.0:
            bad += 1
        elif dp.sample==3.0:
            band_off += 1
        elif dp.sample==4.0:
            missing += 1
        elif dp.sample==5.0:
            not_worn += 1
        elif dp.sample==6.0:
            band_loose += 1
    total_hours = good+noise+bad+band_off+missing+not_worn+band_loose

    return str(seconds_to_hours(good, 3))+","+ \
           str(seconds_to_hours(total_hours, 3))+"\n"

    # return str(seconds_to_hours(good, 3))+","+ \
    #        str(seconds_to_hours(total_hours, 3))+","+ \
    #        str(seconds_to_hours(bad, 3))+","+ \
    #        str(seconds_to_hours(band_off, 3))+","+ \
    #        str(seconds_to_hours(missing, 3))+","+ \
    #        str(seconds_to_hours(not_worn, 3))+","+ \
    #        str(seconds_to_hours(band_loose, 3))+"\n"

