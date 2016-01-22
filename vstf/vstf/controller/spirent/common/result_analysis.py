##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import re


def getResultColumn(data_dict):
    column_string = data_dict['Columns']
    return column_string.strip('{}').split()


def getResult(data_dict):
    result_string = data_dict['Output']
    result_array = result_string.split('} {')
    result = []
    for line in result_array:
        result.append(line.split())
    return result


def restrucData(data_string):
    try:
        data_dict = {}
        p = re.compile('-Columns.*-Output')
        data_dict['Columns'] = p.findall(data_string)[0].strip('-Columns {} -Output')
        p = re.compile('-Output.*-State')
        data_dict['Output'] = p.findall(data_string)[0].strip('-Output {} -State')
        if data_dict['Columns'] is not None or data_dict['Output'] is not None:
            return False, None
        return True, data_dict
    except:
        print("[ERROR]Find the column name or the output result failed.")


def framelossData(column, perfdata):
    column_name_dict = {
        'TrialNumber': 0,
        'Id': 1,
        'FrameSize': 3,
        'TxFrameCount': 9,
        'RxFrameCount': 10,
        'PercentLoss(%s)': 12,
        'MinimumLatency(us)': 17,
        'MaximumLatency(us)': 18,
        'AverageLatency(us)': 19,
        'MinimumJitter(us)': 20,
        'MaximumJitter(us)': 21,
        'AverageJitter(us)': 22,
    }
    # get the column array
    column_array = [
        column[column_name_dict['FrameSize']],
        'ForwardingRate(Mpps)',
        column[column_name_dict['TxFrameCount']],
        column[column_name_dict['RxFrameCount']],
        column[column_name_dict['PercentLoss(%s)']],
        column[column_name_dict['AverageLatency(us)']],
        column[column_name_dict['MinimumLatency(us)']],
        column[column_name_dict['MaximumLatency(us)']],
        column[column_name_dict['AverageJitter(us)']],
        column[column_name_dict['MinimumJitter(us)']],
        column[column_name_dict['MaximumJitter(us)']]
    ]
    data_array = []
    for line in perfdata:
        line_options = [
            #                             line[column_name_dict['TrialNumber']],
            #                             line[column_name_dict['Id']],
            line[column_name_dict['FrameSize']],
            str(float(line[column_name_dict['RxFrameCount']]) / 60 / 1000000),
            line[column_name_dict['TxFrameCount']],
            line[column_name_dict['RxFrameCount']],
            line[column_name_dict['PercentLoss(%s)']],
            line[column_name_dict['AverageLatency(us)']],
            line[column_name_dict['MinimumLatency(us)']],
            line[column_name_dict['MaximumLatency(us)']],
            line[column_name_dict['AverageJitter(us)']],
            line[column_name_dict['MinimumJitter(us)']],
            line[column_name_dict['MaximumJitter(us)']]
        ]
        data_array.append(line_options)
    return [column_array, data_array]


class analysis(object):
    def __init__(self):
        pass

    def analyseResult(self, suite, column, perfdata):
        """
        :type self: object
        """
        global data_array, column_array
        if suite == 'throughput':
            [column_array, data_array] = self.throughputData(column, perfdata)
        elif suite == 'frameloss':
            [column_array, data_array] = self.framelossData(column, perfdata)
        elif suite == 'latency':
            self.latencyData(column, perfdata)
        else:
            return None
        for line in data_array:
            print line
        return [column_array, data_array]

    def throughputData(self, column, perfdata):
        column_name_dict = {
            'TrialNumber': 0,
            'Id': 1,
            'FrameSize': 3,
            'Load(%)': 6,
            'Result': 8,
            'TxFrameCount': 12,
            'RxFrameCount': 13,
            'ForwardingRate(mpps)': 17,
            'MinimumLatency(us)': 18,
            'MaximumLatency(us)': 19,
            'AverageLatency(us)': 20,
            'MinimumJitter(us)': 21,
            'MaximumJitter(us)': 22,
            'AverageJitter(us)': 23
        }
        column_array = {column[column_name_dict['FrameSize']],
                        column[column_name_dict['Load(%)']],
                        column[column_name_dict['Result']],
                        'ForwardingRate(mpps)',
                        column[column_name_dict['TxFrameCount']],
                        column[column_name_dict['RxFrameCount']],
                        column[column_name_dict['AverageLatency(us)']],
                        column[column_name_dict['MinimumLatency(us)']],
                        column[column_name_dict['MaximumLatency(us)']],
                        column[column_name_dict['AverageJitter(us)']],
                        column[column_name_dict['MinimumJitter(us)']],
                        column[column_name_dict['MaximumJitter(us)']]}
        data_array = []
        for line in perfdata:
            if line[column_name_dict['Result']] == 'Passed':
                line_options = [
                    #                                 line[column_name_dict['TrialNumber']],
                    #                                 line[column_name_dict['Id']],
                    line[column_name_dict['FrameSize']],
                    line[column_name_dict['Load(%)']],
                    line[column_name_dict['Result']],
                    str(float(line[column_name_dict['ForwardingRate(mpps)']]) / 1000000),
                    line[column_name_dict['TxFrameCount']],
                    line[column_name_dict['RxFrameCount']],
                    line[column_name_dict['AverageLatency(us)']],
                    line[column_name_dict['MinimumLatency(us)']],
                    line[column_name_dict['MaximumLatency(us)']],
                    line[column_name_dict['AverageJitter(us)']],
                    line[column_name_dict['MinimumJitter(us)']],
                    line[column_name_dict['MaximumJitter(us)']]]
            else:
                continue
            data_array.append(line_options)
        # delete the redundant test data
        delete_index = []
        new_data_array = []
        for ele in range(len(data_array) - 1):
            if data_array[ele][0] == data_array[ele + 1][0]:
                delete_index.append(ele)

        for num in len(data_array):
            if num not in delete_index:
                new_data_array.append(data_array[num])

        return column_array, new_data_array

    def latencyData(self, column, perfdata):
        pass


analysis_instance = analysis()
