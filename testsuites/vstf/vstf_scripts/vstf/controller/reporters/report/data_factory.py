##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from vstf.controller.database.dbinterface import DbManage
import vstf.common.constants as cst


class DataProvider(object):

    def __init__(self, taskid, dbase):
        self._dbase = dbase
        self._taskid = taskid


class CommonData(DataProvider):

    def get_taskname(self):
        return self._dbase.query_taskname(self._taskid)

    def get_systeminfo(self):
        systable = [
            ['Host', 'Server', 'CPU', 'MEM', 'NIC', 'OS'],
        ]
        query = self._dbase.query_task_host_list(self._taskid)
        query = map(lambda x: list(x), query)
        #    rows = len(query)
        #    cols = len(zip(*query))
        #    for i in range(rows):
        #        for j in range(cols):
        #            query[i][j] = query[i][j].replace('\",','\"\n')
        systable += query
        systable = map(lambda x: list(x), zip(*systable))
        return systable

    def get_introduct_tabledata(self):
        result = [
            ["Type", "Case", "Name", "Direction", "Configure"]
        ]
        query = self._dbase.query_caseinfo()
        result += map(lambda x: list(x), query)
        return result

    def get_scenariolist(self):
        query = self._dbase.query_scenariolist(self._taskid)
        result = map(lambda x: list(x), zip(*query))
        if result:
            return result[0]
        else:
            return result

    def is_scenario_start(self):
        scenarioList = self.get_scenariolist()
        print "scenarioList: ", scenarioList
        if scenarioList:
            return True
        return False

    def get_casename(self, case):
        return self._dbase.query_casename(case)

    def get_casefigure(self, case, tools):
        return self._dbase.query_casefigure(case, tools)


class ScenarioData(DataProvider):

    def __init__(self, taskid, dbase, scenario):
        print "ScenarioData in"
        DataProvider.__init__(self, taskid, dbase)
        self._scenario = scenario

    def get_test_tools(self, case):
        query = self._dbase.query_casetools(self._taskid, case)
        result = map(lambda x: list(x), query)
        if result:
            return result[0][0]
        else:
            return result

    def get_caselist(self):
        query = self._dbase.query_caselist(self._taskid, self._scenario)
        result = map(lambda x: list(x), zip(*query))
        if result:
            return result[0]
        else:
            return result

    def get_testlist(self):
        query = self._dbase.query_testlist(self._taskid, self._scenario)
        result = []
        for item in query:
            result.append(item.__dict__)
        return query

    def is_provider_start(self, case, provider):
        count = self._dbase.query_case_provider_count(
            self._taskid, case, provider)
        if count:
            return True
        return False

    def is_type_provider_start(self, case, provider, ptype):
        count = self._dbase.query_case_type_provider_count(
            self._taskid, case, provider, ptype)
        if count:
            return True
        return False

    def is_type_start(self, case, ptype):
        count = self._dbase.query_case_type_count(self._taskid, case, ptype)
        if count:
            return True
        return False

    def is_throughput_start(self, case):
        test_type = "throughput"
        return self.is_type_start(case, test_type)

    def is_frameloss_start(self, case):
        test_type = "frameloss"
        return self.is_type_start(case, test_type)

    def is_latency_start(self, case):
        test_type = "latency"
        return self.is_type_start(case, test_type)

    def get_summary_throughput_data(self, case, provider):
        test_type = "throughput"
        return self.get_summary_tabledata(case, provider, test_type)

    def get_summary_frameLoss_data(self, case, provider):
        test_type = "frameloss"
        return self.get_summary_tabledata(case, provider, test_type)

    def get_summary_tabledata(
            self,
            case,
            provider,
            test_type,
            table_type='pdf'):
        table_head = []
        table_body = []
        type_title = {
            "frameloss": "Load",
            "throughput": "Load"
        }
        tools = self.get_test_tools(case)
        if "spirent" in tools:
            table_body = self._dbase.query_summary_table(
                self._taskid, case, provider, test_type)
            if 'pdf' == table_type:
                table_head = [["FrameSize (byte)",
                               test_type,
                               "",
                               "",
                               "",
                               "Latency(uSec)",
                               "",
                               ""],
                              ["",
                               "    Mpps    ",
                               "   " + type_title[test_type] + " (%)   ",
                               "CPU Used (%)",
                               " Mpps/Ghz ",
                               " Min ",
                               " Max ",
                               " Avg "]]
            else:
                table_head = [["FrameSize (byte)",
                               "    Mpps    ",
                               "   " + type_title[test_type] + " (%)   ",
                               "CPU Used (%)",
                               " Mpps/Ghz ",
                               "MinLatency(uSec)",
                               "MaxLatency(uSec)",
                               "AvgLatency(uSec)"],
                              ]
        else:
            table_body = self._dbase.query_summary_simpletable(
                self._taskid, case, provider, test_type)
            if 'pdf' == table_type:
                table_head = [["FrameSize (byte)",
                               test_type,
                               "",
                               "",
                               "",
                               "Latency(uSec)"],
                              ["",
                               "    Mpps    ",
                               "   " + type_title[test_type] + " (%)",
                               "CPU Used (%)",
                               " Mpps/Ghz ",
                               "  Avg  "]]
            else:
                table_head = [["FrameSize (byte)",
                               "    Mpps    ",
                               "   " + type_title[test_type] + " (%)   ",
                               "CPU Used (%)",
                               " Mpps/Ghz ",
                               "AvgLatency(uSec)"],
                              ]
        return table_head + table_body

    def get_ratedata(self, testid, test_type):
        table_head = [["FrameSize (bytes)",
                       "Bandwidth(Mpps)",
                       "Load (%)",
                       "CPU Usage(%)",
                       "Mpps/Ghz",
                       "AvgLatency(uSec)"],
                      ]
        query = self._dbase.query_testdata(testid, test_type)
        table_body = []
        for item in query:
            table_body.append([item.AvgFrameSize,
                               item.Bandwidth,
                               item.OfferedLoad,
                               item.CPU,
                               item.MppspGhz,
                               item.AverageLatency])
        result = []
        if table_body:
            result = table_head + table_body
        return result

    def get_tabledata(self, case, test_type, item):
        type_dict = {
            "FrameSize": "FrameSize (byte)",
            "fastlink": "fastlink",
            "l2switch": "l2switch",
            "rdp": "kernel rdp",
            None: "ovs",
            "line": "line speed"
        }
        item_dict = {
            "Percent": "  ",
            "Mpps": "   ",
            "Avg": "   ",
        }
        table = []
        line_speed = 20.0 if case in ["Tn-2v", "Tn-2"] else 10.0

        for provider in cst.PROVIDERS:
            if self.is_provider_start(case, provider):
                if item == 'Percent':
                    query = self._dbase.query_load(
                        self._taskid, case, provider, test_type)
                elif item == 'Mpps':
                    query = self._dbase.query_bandwidth(
                        self._taskid, case, provider, test_type)
                else:
                    query = self._dbase.query_avglatency(
                        self._taskid, case, provider, test_type)
                query = map(lambda x: list(x), zip(*query))
                if query:
                    table_head = [[type_dict["FrameSize"]] +
                                  map(lambda x: "  %4d  " % (x), query[0])]
                    if item == "Avg":
                        data = map(
                            lambda x: item_dict[item] + "%.1f" %
                            x + item_dict[item], query[1])
                    else:
                        data = map(
                            lambda x: item_dict[item] + "%.2f" %
                            x + item_dict[item], query[1])
                    if item == "Mpps":
                        line_table = map(lambda x: "%.2f" % (
                            line_speed * 1000 / (8 * (x + 20))), query[0])
                    table.append([type_dict[provider]] + data)
        if table:
            if item == "Mpps":
                table.append([type_dict["line"]] + line_table)
            table = table_head + table
        return table

    def get_frameloss_tabledata(self, case, test_type):
        item = "Percent"
        table = self.get_tabledata(case, test_type, item)
        return table

    def get_frameloss_chartdata(self, case, test_type):
        result = self.get_frameloss_tabledata(case, test_type)
        result = map(list, zip(*result))
        return result

    def get_framerate_tabledata(self, case, test_type):
        item = "Mpps"
        table = self.get_tabledata(case, test_type, item)
        return table

    def get_framerate_chartdata(self, case, test_type):
        result = self.get_framerate_tabledata(case, test_type)
        result = map(list, zip(*result))
        return result

    def get_latency_tabledata(self, case):
        test_type = "latency"
        item = "Avg"
        table = self.get_tabledata(case, test_type, item)
        return table

    def get_latency_chartdata(self, case):
        result = self.get_latency_tabledata(case)
        result = map(list, zip(*result))
        return result

    def get_latency_bardata(self, case):
        table_data = self.get_latency_tabledata(case)
        result = []
        if table_data:
            ytitle = "Average Latency (uSec)"
            category_names = map(lambda x: "FS:%4d" %
                                 int(float(x)) + "LOAD:50", table_data[0][1:])
            bar_ = map(lambda x: x[0], table_data[1:])
            data = map(lambda x: x[1:], table_data[1:])
            result = [ytitle, category_names, bar_, data]
        return result

    def get_bardata(self, case, provider, test_type):
        if test_type == "latency":
            query = self._dbase.query_avglatency(
                self._taskid, case, provider, test_type)
            item = "Avg"
        else:
            query = self._dbase.query_load(
                self._taskid, case, provider, test_type)
            item = "Percent"

        title_dict = {
            "Avg": "Latency (uSec)",
            "Percent": test_type + " (%)"
        }
        name_dict = {
            "Avg": " LOAD:50",
            "Percent": " OF:100 "
        }
        color_dict = {
            "Avg": "latency",
            "Percent": "loss"
        }
        ytitle = title_dict[item]
        query = map(lambda x: list(x), zip(*query))
        result = []
        if query:
            category_names = map(
                lambda x: "FS:%4d" %
                x + name_dict[item], query[0])
            data = query[1:]
            bar_ = [color_dict[item]]
            result = [ytitle, category_names, bar_, data]
        return result


class TaskData(object):

    def __init__(self, taskid, dbase):
        self.__common = CommonData(taskid, dbase)
        scenario_list = self.__common.get_scenariolist()
        scenario_dic = {}
        for scenario in scenario_list:
            scenario_dic[scenario] = ScenarioData(taskid, dbase, scenario)
        self.__dict__.update(scenario_dic)

    @property
    def common(self):
        return self.__common


class HistoryData(DataProvider):

    def get_data(self, task_list, case, provider, ttype, item):
        """
        @provider  in ["fastlink", "rdp", "l2switch", ""]
        @ttype in ["throughput", "frameloss", "latency"]
        @item in ["avg", "ratep", "load"]
        """
        table = []
        table_head = []
        datas = []
        sizes = []
        for taskid in task_list:
            if item == 'ratep':
                query = self._dbase.query_bandwidth(
                    taskid, case, provider, ttype)
            else:
                query = self._dbase.query_avglatency(
                    taskid, case, provider, ttype)

            if query:
                data = {}
                for size, value in query:
                    data[size] = value
                sizes.extend(data.keys())
                sizes = sorted({}.fromkeys(sizes).keys())
                datas.append({taskid: data})

        result = []
        for data in datas:
            print data
            taskid = data.keys()[0]
            data_th = self._dbase.query_taskdate(taskid)
            testdata = data[taskid]
            item = [data_th]
            for size in sizes:
                item.append(str(testdata.get(size, '')))
            result.append(item)

        if result:
            head_th = "FrameSize (byte)"
            table_head = [[head_th] + map(lambda x: "  %4d  " % (x), sizes)]
            table = table_head + result

        return table

    def get_tasklist(self, count=5):
        task_list = []
        query = self._dbase.query_tasklist()
        if query:
            for item in query:
                if item.TaskID <= self._taskid:
                    task_list.append(item.TaskID)

        task_list = task_list[-count:]
        return task_list

    def get_history_info(self, case):
        provider_dict = {
            "fastlink": "Fast Link ",
            "l2switch": "L2Switch ",
            "rdp": "Kernel RDP "}
        ttype_dict = {
            "throughput": "Throughput Testing ",
            "frameloss": "Frame Loss Testing ",
            "latency": "Latency Testing "
        }

        items_dict = {
            "ratep": "RX Frame Rate(Mpps) ",
            "avg": "Average Latency (uSec) "
        }

        task_list = self.get_tasklist()
        result = []

        for ttype in cst.TTYPES:
            content = {}
            if ttype == "latency":
                item = "avg"
            else:
                item = "ratep"

            for provider in cst.PROVIDERS:
                table_data = self.get_data(
                    task_list, case, provider, ttype, item)
                if table_data:
                    data = {
                        "title": provider_dict[provider] + items_dict[item],
                        "data": table_data
                    }
                    content["title"] = ttype_dict[ttype]
                    content.setdefault("data", [])
                    content["data"].append(data)
            if content:
                result.append(content)
        print result
        return result


def unit_test():
    dbase = DbManage()
    taskid = dbase.get_last_taskid()
    hdata = HistoryData(taskid, dbase)
    task_list = hdata.get_tasklist()

    cdata = CommonData(taskid, dbase)
    scenario_list = cdata.get_scenariolist()
    print scenario_list

    scenario = "Tn"
    sdata = ScenarioData(taskid, dbase, scenario)

    case_list = sdata.get_caselist()
    print case_list

    case = "Tn-1"

    ttypes = ["throughput", "frameloss"]
    items = ["ratep", "load"]

    for provider in cst.PROVIDERS:
        for ttype in ttypes:
            for item in items:
                print provider
                print ttype
                print item
                print hdata.get_data(task_list, case, provider, ttype, item)

    hdata.get_history_info(case)


if __name__ == '__main__':
    unit_test()
