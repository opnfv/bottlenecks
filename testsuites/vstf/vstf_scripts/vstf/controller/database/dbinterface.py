##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
import vstf.controller.database.tables as table
from vstf.controller.database import constants as const

LOG = logging.getLogger(__name__)

"""
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement,
    parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())
    logging.debug("Start Query: %s", statement)
@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement,
    parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop(-1)
    logging.debug("Query Complete!")
    logging.debug("Total Time: %f", total)"""


class DbManage(object):

    def __init__(self, db_name=const.DBPATH):
        db_exists = os.path.exists(db_name)
        try:
            self._engine = create_engine('sqlite:///%s' % db_name, echo=False)
            db_session = sessionmaker(bind=self._engine)
            self._session = db_session()
        except Exception as e:
            raise e

        # if the db is new , create all tables and init static tables
        if not db_exists:
            self.create_tables()
            self.init_tables()

    def __delete__(self):
        self._engine.close_all()

    def create_tables(self):
        table.Base.metadata.create_all(self._engine)
        self._session.commit()

    def drop_tables(self):
        table.Base.metadata.drop_all(self._engine)
        self._session.commit()

    def init_tables(self):
        self.init_casetable()
        self.init_scenario_table()
        self._session.commit()

    def init_scenario_table(self):
        items = []
        for values in const.SCENARIO_INFO_LIST:
            item = table.TblScenarioInfo(ScenarioName=values[0],
                                         FigurePath=values[1],
                                         Description=values[2])
            items.append(item)
        self._session.add_all(items)

    # Single TblCaseInfo API
    def init_casetable(self):
        items = []
        for values in const.CASE_INFO_LIST:
            item = table.TblCaseInfo(CaseTag=values[0],
                                     ScenarioName=values[1],
                                     CaseName=values[2],
                                     FigurePath=values[3],
                                     Description=values[4],
                                     Direction=values[5],
                                     Directiontag=values[6],
                                     Configure=values[7])
            items.append(item)
        self._session.add_all(items)

    def query_caseinfo(self):
        query = self._session.query(table.TblCaseInfo.ScenarioName,
                                    table.TblCaseInfo.CaseTag,
                                    table.TblCaseInfo.CaseName,
                                    table.TblCaseInfo.Direction,
                                    table.TblCaseInfo.Configure)
        return query.all()

    def query_case(self, casetag):
        query = self._session.query(table.TblCaseInfo.ScenarioName,
                                    table.TblCaseInfo.Directiontag)
        return query.first()

    # Single TblTaskList API
    def get_last_taskid(self):
        query = self._session.query(table.TblTaskList.TaskID)
        if query:
            return query.all()[-1][0]
        else:
            return 0

    def query_tasklist(self):
        query = self._session.query(table.TblTaskList)
        return query.all()

    def query_taskdate(self, taskid):
        query = self._session.query(table.TblTaskList.Date).filter(and_(
            table.TblTaskList.TaskID == taskid))
        result = ""
        if query:
            result += query.first()[0]
        return result

    def query_taskname(self, taskid):
        query = self._session.query(table.TblTaskList.TaskName).filter(and_(
            table.TblTaskList.TaskID == taskid))
        result = ""
        if query:
            result += query.first()[0]
        return result

    def create_task(self, name, date, desc):
        try:
            item = table.TblTaskList(name, date, desc)
            self._session.add(item)
            self._session.commit()
        except Exception:
            return -1

        return self.get_last_taskid()

    # Single TblHostInfo API
    def add_host_2task(self, taskid, name, machine, cpu, men, nic, os):
        """All var except task must be string"""
        item = table.TblHostInfo(taskid, name, machine, cpu, men, nic, os)

        self._session.add(item)
        self._session.commit()

    def query_task_host_list(self, taskid):
        query = self._session.query(table.TblHostInfo.HostName,
                                    table.TblHostInfo.Server,
                                    table.TblHostInfo.CPU,
                                    table.TblHostInfo.MEM,
                                    table.TblHostInfo.NIC,
                                    table.TblHostInfo.OS).filter(
            table.TblHostInfo.TaskID == taskid)
        return query.all()

    # Single TblTestList API
    def get_last_testid(self):
        query = self._session.query(table.TblTestList.TestID)
        print query.all()
        if query:
            return query.all()[-1][0]
        else:
            return 0

    def add_test_2task(
            self,
            task,
            case,
            protocol,
            typ,
            switch,
            provider,
            tool):
        try:
            item = table.TblTestList(
                task, case, protocol, typ, switch, provider, tool)
            self._session.add(item)
            self._session.commit()
        except Exception:
            return -1

        return self.get_last_testid()

    def get_test_type(self, testid):
        query = self._session.query(table.TblTestList.Type).filter(
            table.TblTestList.TestID == testid)
        return query.first()

    def add_extent_2task(self, task, name, content, description):
        item = table.TblEXTInfo(task, name, content, description)
        self._session.add(item)
        self._session.commit()

    def add_data_2test(self, testid, data):
        """
        :data example {'64':{
                            'AvgFrameSize':0
                            'OfferedLoad':0
                            'PercentLoss':0
                            'Bandwidth':0
                            'MinimumLatency':0
                            'MaximumLatency':0
                            'AverageLatency':0
                            'TxFrameCount':0
                            'RxFrameCount':0
                            'Duration':0
                            'CPU':0
                            'MppspGhz':0
                            }}
        """
        ptype = self.get_test_type(testid)
        instance_map = {
            'throughput': table.TblThroughput,
            'frameloss': table.TblFrameloss,
            'latency': table.TblLatency
        }

        if ptype and ptype[0] not in instance_map:
            print "cant find this test(id=%d)" % (testid)
            return False

        test_table_instance = instance_map[ptype[0]]
        for pktlen in data.iterkeys():
            args = data.get(pktlen)
            query = self._session.query(test_table_instance).filter(and_(
                test_table_instance.TestID == testid,
                test_table_instance.AvgFrameSize == pktlen))
            if query.all():
                data_dict = {}
                for key, value in data.items():
                    if key in test_table_instance.__dict__:
                        data_dict[test_table_instance.__dict__[key]] = value
                query.update(data_dict)
            else:
                print args
                tester = test_table_instance(testid, pktlen, **args)
                self._session.add(tester)
        self._session.commit()

    def query_tasks(self):
        result = []
        ret = self._session.query(table.TblTaskList)
        if ret:
            for tmp in ret.all():
                result.append(
                    [tmp.TaskID, tmp.TaskName, tmp.Date, tmp.EXTInfo])
        return result

    def query_all_task_id(self):
        query = self._session.query(table.TblTaskList.TaskID)
        if query:
            return query.all()
        else:
            return []

    def get_caseinfo(self):
        query = self._session.query(table.TblCaseInfo.ScenarioName,
                                    table.TblCaseInfo.CaseTag,
                                    table.TblCaseInfo.CaseName,
                                    table.TblCaseInfo.Direction,
                                    table.TblCaseInfo.Configure)
        return query.all()

    def query_scenario(self, casetag):
        query = self._session.query(
            table.TblCaseInfo.ScenarioName).filter(
            table.TblCaseInfo.CaseTag == casetag)
        ret = ""
        if query and query.first():
            ret = query.first()[0]
        return ret

    def query_casefigure(self, casetag, tools):
        query = self._session.query(table.TblCaseInfo.FigurePath).filter(and_(
            table.TblCaseInfo.CaseTag == casetag))
        result = ""
        if query:
            result += query.first()[0]
        print tools, casetag
        result += tools + '/' + casetag + '.jpg'
        return result

    def query_casename(self, casetag):
        query = self._session.query(table.TblCaseInfo.CaseName).filter(and_(
            table.TblCaseInfo.CaseTag == casetag))
        result = ""
        if query:
            result += query.first()[0]
        return result

    # Single TblTestList API

    def query_caselist(self, taskid, scenario):
        query = self._session.query(
            table.TblTestList.CaseTag).filter(
            and_(
                table.TblTestList.CaseTag == table.TblCaseInfo.CaseTag,
                table.TblCaseInfo.ScenarioName == scenario,
                table.TblTestList.TaskID == taskid)).group_by(
                table.TblCaseInfo.CaseTag)
        return query.all()

    def query_testlist(self, taskid, scenario):
        """

        :rtype : object
        """
        query = self._session.query(table.TblTestList).filter(and_(
            table.TblTestList.CaseTag == table.TblCaseInfo.CaseTag,
            table.TblCaseInfo.ScenarioName == scenario,
            table.TblTestList.TaskID == taskid))
        return query.all()

    def query_casetool(self, taskid, casetag, provider, ptype):
        query = self._session.query(table.TblTestList.Tools).filter(and_(
            table.TblTestList.TaskID == taskid,
            table.TblTestList.CaseTag == casetag,
            table.TblTestList.Provider == provider,
            table.TblTestList.Type == ptype))
        return query.all()

    def query_casetools(self, taskid, casetag):
        query = self._session.query(
            table.TblTestList.Tools).filter(
            and_(
                table.TblTestList.CaseTag == casetag,
                table.TblTestList.TaskID == taskid)).group_by(
                table.TblTestList.Tools)
        return query.all()

    def query_scenariolist(self, taskid):
        query = self._session.query(
            table.TblCaseInfo.ScenarioName).filter(
            and_(
                table.TblTestList.CaseTag == table.TblCaseInfo.CaseTag,
                table.TblTestList.TaskID == taskid)).group_by(
                table.TblCaseInfo.ScenarioName)
        return query.all()

    def query_throughput_load(self, taskid, casetag, provider):
        ptype = 'throughput'
        query = self._session.query(
            table.TblThroughput.AvgFrameSize,
            table.TblThroughput.OfferedLoad).filter(
            and_(
                table.TblTestList.TaskID == taskid,
                table.TblTestList.CaseTag == casetag,
                table.TblTestList.Provider == provider,
                table.TblTestList.Type == ptype,
                table.TblTestList.TestID == table.TblThroughput.TestID))
        return query.all()

    def query_throughput_bandwidth(self, taskid, casetag, provider):
        ptype = 'throughput'
        query = self._session.query(
            table.TblThroughput.AvgFrameSize,
            table.TblThroughput.Bandwidth).filter(
            and_(
                table.TblTestList.TaskID == taskid,
                table.TblTestList.CaseTag == casetag,
                table.TblTestList.Provider == provider,
                table.TblTestList.Type == ptype,
                table.TblTestList.TestID == table.TblThroughput.TestID))
        return query.all()

    def query_throughput_table(self, taskid, casetag, provider):
        ptype = 'throughput'
        query = self._session.query(
            table.TblThroughput.AvgFrameSize,
            table.TblThroughput.Bandwidth,
            table.TblThroughput.OfferedLoad,
            table.TblThroughput.CPU,
            table.TblThroughput.MppspGhz,
            table.TblThroughput.MinimumLatency,
            table.TblThroughput.MaximumLatency,
            table.TblThroughput.AverageLatency,
        ).filter(
            and_(
                table.TblTestList.TaskID == taskid,
                table.TblTestList.CaseTag == casetag,
                table.TblTestList.Provider == provider,
                table.TblTestList.Type == ptype,
                table.TblTestList.TestID == table.TblThroughput.TestID))
        return query.all()

    def query_throughput_simpletable(self, taskid, casetag, provider):
        ptype = 'throughput'
        query = self._session.query(
            table.TblThroughput.AvgFrameSize,
            table.TblThroughput.Bandwidth,
            table.TblThroughput.OfferedLoad,
            table.TblThroughput.CPU,
            table.TblThroughput.MppspGhz,
            table.TblThroughput.AverageLatency,
        ).filter(
            and_(
                table.TblTestList.TaskID == taskid,
                table.TblTestList.CaseTag == casetag,
                table.TblTestList.Provider == provider,
                table.TblTestList.Type == ptype,
                table.TblTestList.TestID == table.TblThroughput.TestID))
        return query.all()

    def query_testdata(self, testid, ptype):
        obj = getattr(table, "Tbl%s" % (ptype.title()))
        query = self._session.query(obj).filter(obj.TestID == testid)
        return query.all()

    def query_throughput_avg(self, taskid, casetag, provider):
        ptype = 'throughput'
        query = self._session.query(
            table.TblThroughput.AvgFrameSize,
            table.TblThroughput.AverageLatency).filter(
            and_(
                table.TblTestList.TaskID == taskid,
                table.TblTestList.CaseTag == casetag,
                table.TblTestList.Provider == provider,
                table.TblTestList.Type == ptype,
                table.TblTestList.TestID == table.TblThroughput.TestID))
        return query.all()

    def query_frameloss_bandwidth(self, taskid, casetag, provider):
        ptype = 'frameloss'
        query = self._session.query(
            table.TblFrameloss.AvgFrameSize,
            table.TblFrameloss.Bandwidth).filter(
            and_(
                table.TblTestList.TaskID == taskid,
                table.TblTestList.CaseTag == casetag,
                table.TblTestList.Provider == provider,
                table.TblTestList.Type == ptype,
                table.TblTestList.TestID == table.TblFrameloss.TestID))
        return query.all()

    def query_frameloss_load(self, taskid, casetag, provider):
        ptype = 'frameloss'
        query = self._session.query(
            table.TblFrameloss.AvgFrameSize,
            table.TblFrameloss.OfferedLoad).filter(
            and_(
                table.TblTestList.TaskID == taskid,
                table.TblTestList.CaseTag == casetag,
                table.TblTestList.Provider == provider,
                table.TblTestList.Type == ptype,
                table.TblTestList.TestID == table.TblFrameloss.TestID))
        return query.all()

    def query_frameloss_table(self, taskid, casetag, provider):
        ptype = 'frameloss'
        query = self._session.query(
            table.TblFrameloss.AvgFrameSize,
            table.TblFrameloss.Bandwidth,
            table.TblFrameloss.OfferedLoad,
            table.TblFrameloss.CPU,
            table.TblFrameloss.MppspGhz,
            table.TblFrameloss.MinimumLatency,
            table.TblFrameloss.MaximumLatency,
            table.TblFrameloss.AverageLatency).filter(
            and_(
                table.TblTestList.TaskID == taskid,
                table.TblTestList.CaseTag == casetag,
                table.TblTestList.Provider == provider,
                table.TblTestList.Type == ptype,
                table.TblTestList.TestID == table.TblFrameloss.TestID))
        return query.all()

    def query_frameloss_simpletable(self, taskid, casetag, provider):
        ptype = 'frameloss'
        query = self._session.query(
            table.TblFrameloss.AvgFrameSize,
            table.TblFrameloss.Bandwidth,
            table.TblFrameloss.OfferedLoad,
            table.TblFrameloss.CPU,
            table.TblFrameloss.MppspGhz,
            table.TblFrameloss.AverageLatency).filter(
            and_(
                table.TblTestList.TaskID == taskid,
                table.TblTestList.CaseTag == casetag,
                table.TblTestList.Provider == provider,
                table.TblTestList.Type == ptype,
                table.TblTestList.TestID == table.TblFrameloss.TestID))
        return query.all()

    def query_frameloss_avg(self, taskid, casetag, provider):
        ptype = 'frameloss'
        query = self._session.query(
            table.TblFrameloss.AvgFrameSize,
            table.TblFrameloss.AverageLatency).filter(
            and_(
                table.TblTestList.TaskID == taskid,
                table.TblTestList.CaseTag == casetag,
                table.TblTestList.Provider == provider,
                table.TblTestList.Type == ptype,
                table.TblTestList.TestID == table.TblFrameloss.TestID))
        return query.all()

    def query_latency_avg(self, taskid, casetag, provider):
        ptype = 'latency'
        query = self._session.query(
            table.TblLatency.AvgFrameSize,
            table.TblLatency.AverageLatency).filter(
            and_(
                table.TblTestList.TaskID == taskid,
                table.TblTestList.CaseTag == casetag,
                table.TblTestList.Provider == provider,
                table.TblTestList.Type == ptype,
                table.TblTestList.TestID == table.TblLatency.TestID))
        return query.all()

    def query_summary_table(self, taskid, casetag, provider, ptype):
        if ptype in ['throughput', 'frameloss']:
            qfunc = getattr(self, "query_%s_table" % (ptype))
            return qfunc(taskid, casetag, provider)
        return []

    def query_summary_simpletable(self, taskid, casetag, provider, ptype):
        if ptype in ['throughput', 'frameloss']:
            qfunc = getattr(self, "query_%s_simpletable" % (ptype))
            return qfunc(taskid, casetag, provider)
        return []

    def query_bandwidth(self, taskid, casetag, provider, ptype):
        if ptype in ['throughput', 'frameloss']:
            qfunc = getattr(self, "query_%s_bandwidth" % (ptype))
            return qfunc(taskid, casetag, provider)
        return []

    def query_load(self, taskid, casetag, provider, ptype):
        if ptype in ['throughput', 'frameloss']:
            qfunc = getattr(self, "query_%s_load" % (ptype))
            return qfunc(taskid, casetag, provider)
        return []

    def query_avglatency(self, taskid, casetag, provider, ptype):
        if ptype in ['throughput', 'frameloss', 'latency']:
            qfunc = getattr(self, "query_%s_avg" % (ptype))
            return qfunc(taskid, casetag, provider)
        return []

    def query_throughput_provider(self, taskid, casetag, provider):
        query = self._session.query(
            table.TblThroughput).filter(
            and_(
                table.TblTestList.CaseTag == casetag,
                table.TblTestList.Provider == provider,
                table.TblTestList.TaskID == taskid,
                table.TblTestList.TestID == table.TblThroughput.TestID))
        return query.all()

    def query_frameloss_provider(self, taskid, casetag, provider):
        query = self._session.query(
            table.TblFrameloss).filter(
            and_(
                table.TblTestList.CaseTag == casetag,
                table.TblTestList.Provider == provider,
                table.TblTestList.TaskID == taskid,
                table.TblTestList.TestID == table.TblFrameloss.TestID))
        return query.all()

    def query_latency_provider(self, taskid, casetag, provider):
        query = self._session.query(
            table.TblLatency).filter(
            and_(
                table.TblTestList.CaseTag == casetag,
                table.TblTestList.Provider == provider,
                table.TblTestList.TaskID == taskid,
                table.TblTestList.TestID == table.TblLatency.TestID))
        return query.all()

    def query_case_type_count(self, taskid, casetag, ptype):
        query = self._session.query(
            table.TblTestList).filter(
            and_(
                table.TblTestList.CaseTag == casetag,
                table.TblTestList.Type == ptype,
                table.TblTestList.TaskID == taskid))

        return query.count()

    def query_case_provider_count(self, taskid, casetag, provider):
        query = self._session.query(
            table.TblTestList).filter(
            and_(
                table.TblTestList.CaseTag == casetag,
                table.TblTestList.Provider == provider,
                table.TblTestList.TaskID == taskid))
        return query.count()

    def query_case_type_provider_count(self, taskid, casetag, provider, ptype):
        query = self._session.query(
            table.TblTestList).filter(
            and_(
                table.TblTestList.CaseTag == casetag,
                table.TblTestList.Type == ptype,
                table.TblTestList.Provider == provider,
                table.TblTestList.TaskID == taskid))

        return query.count()

    def query_exten_info(self, taskid):
        query = self._session.query(
            table.TblEXTInfo.EXTName,
            table.TblEXTInfo.EXTContent,
            table.TblEXTInfo.Description).filter(
            table.TblEXTInfo.TaskID == taskid)
        return query.all()


def unit_test():
    import time
    dbase = DbManage()

    taskid = dbase.create_task("test", str(
        time.ctime()), "this is a unit test")
    dbase.add_host_2task(
        taskid,
        "hosta",
        "hw82576",
        "xxx",
        "x",
        "82599",
        "ubuntu")
    dbase.add_extent_2task(taskid, "CETH", "driver", "version 2.0")
    dbase.add_extent_2task(taskid, "EVS", "switch", "version 3.0")

    testid = dbase.add_test_2task(
        taskid,
        "Tn-1",
        'udp',
        "throughput",
        "ovs",
        None,
        "netperf")
    data = {
        '64': {
            'OfferedLoad': 2,
            'PercentLoss': 3,
            'Bandwidth': 4,
            'MinimumLatency': 5,
            'MaximumLatency': 6,
            'AverageLatency': 7,
            'TxFrameCount': 8,
            'RxFrameCount': 9,
            'Duration': 10,
            'CPU': 11,
            'MppspGhz': 12,
        }
    }
    dbase.add_data_2test(testid, data)

    testid = dbase.add_test_2task(
        taskid,
        "Tn-1",
        'udp',
        "frameloss",
        "ovs",
        None,
        "netperf")
    data = {
        '64': {
            'OfferedLoad': 2,
            'PercentLoss': 3,
            'Bandwidth': 4,
            'MinimumLatency': 5,
            'MaximumLatency': 6,
            'AverageLatency': 7,
            'TxFrameCount': 8,
            'RxFrameCount': 9,
            'Duration': 10,
            'CPU': 11,
            'MppspGhz': 12,
        }
    }
    dbase.add_data_2test(testid, data)

    testid = dbase.add_test_2task(
        taskid,
        "Tn-1",
        'udp',
        "latency",
        "ovs",
        None,
        "netperf")
    data = {
        64: {
            'MaximumLatency': 0.0,
            'AverageLatency': 0.0,
            'MinimumLatency': 0.0,
            'OfferedLoad': 0.0},
        128: {
            'MaximumLatency': 0.0,
            'AverageLatency': 0.0,
            'MinimumLatency': 0.0,
            'OfferedLoad': 0.0},
        512: {
            'MaximumLatency': 0.0,
            'AverageLatency': 0.0,
            'MinimumLatency': 0.0,
            'OfferedLoad': 0.0},
        1024: {
            'MaximumLatency': 0.0,
            'AverageLatency': 0.0,
            'MinimumLatency': 0.0,
            'OfferedLoad': 0.0}}
    dbase.add_data_2test(testid, data)
    query = dbase.query_testlist(1, "Tn")
    for item in query:
        print item.Protocol

    query = dbase.query_testdata(1, "throughput")
    print query

if __name__ == '__main__':
    unit_test()
