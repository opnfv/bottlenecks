#!/usr/bin/python
# -*- coding: utf8 -*-
# author: wly
# date: 2015-12-25
# see license for license details
__version__ = ''' '''
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from vstf.controller.database import constants as const

Base = declarative_base()


class TblScenarioInfo(Base):
    __tablename__ = "TblScenarioInfo"
    ScenarioID = Column(Integer, primary_key=True)
    ScenarioName = Column(String(const.SCENARIO_NAME_LEN), unique=True)
    FigurePath = Column(String(const.FIGURE_PATH_LEN))
    Description = Column(String(const.DESC_LEN))

    def __init__(self, ScenarioName, FigurePath, Description, **kwargs):
        """
        :param ScenarioName: name of the scenario, like Tn
        :param FigurePath: ??
        :param Description: desc of scenario table
        """
        self.ScenarioName = ScenarioName
        self.FigurePath = FigurePath
        self.Description = Description

    def __repr__(self):
        return "<User(ScenarioName='%s', FigurePath='%s', Description='%s')>" % (
            self.ScenarioName, self.FigurePath, self.Description)


class TblCaseInfo(Base):
    __tablename__ = "TblCaseInfo"
    CaseID = Column(Integer, primary_key=True)
    CaseTag = Column(String(const.CASE_TAG_LEN), unique=True)
    CaseName = Column(String(const.CASE_NAME_LEN), unique=True)
    ScenarioName = Column(String(const.SCENARIO_NAME_LEN))
    FigurePath = Column(String(const.FIGURE_PATH_LEN))
    Direction = Column(String(const.DIRECTION_LEN))
    Directiontag = Column(String(const.DIRECTION_LEN))
    Configure = Column(String(const.CONF_LEN))
    Description = Column(String(const.DESC_LEN))

    def __init__(self, CaseTag, CaseName,
                 ScenarioName, FigurePath, Direction, Directiontag,
                 Configure, Description, **kwargs):
        """
        :param CaseID: 
        :param CaseTag: ??
        :param CaseName: name of case, like tester-vm
        :param ScenarioName: name of scenario, like Tn
        :param FigurePath:
        :param Direction: the test direction, Tx or Rx
        :param Configure:
        :param Description: desc of table case info
        """
        # CaseID will auto builded by db
        self.CaseTag = CaseTag
        self.CaseName = CaseName
        self.ScenarioName = ScenarioName
        self.FigurePath = FigurePath
        self.Direction = Direction
        self.Directiontag = Directiontag
        self.Configure = Configure
        self.Description = Description

    def __repr__(self):
        return "<User(CaseTag='%s', CaseName='%s',ScenarioName='%s',FigurePath='%s', Direction='%s', \
            Directiontag='%s', Configure='%s', Description='%s')>" % (self.CaseTag, self.CaseName,
                                                                      self.ScenarioName, self.FigurePath,
                                                                      self.Direction, self.Directiontag, self.Configure,
                                                                      self.Description)


class TblHostInfo(Base):
    __tablename__ = "TblHostInfo"
    Index = Column(Integer, primary_key=True)
    TaskID = Column(Integer, ForeignKey('TblTaskList.TaskID'))
    HostName = Column(String(const.HOST_NAME_LEN))
    Server = Column(String(const.NORMAL_VAR_LEN1))
    CPU = Column(String(const.CPU_INFO_LEN))
    MEM = Column(String(const.NORMAL_VAR_LEN))
    NIC = Column(String(const.NORMAL_VAR_LEN))
    OS = Column(String(const.NORMAL_VAR_LEN))

    def __init__(self, TaskID, HostName, Server, CPU, MEM, NIC, OS, **kwargs):
        """table of host info
        """
        self.TaskID = TaskID
        self.HostName = HostName
        self.Server = Server
        self.CPU = CPU
        self.MEM = MEM
        self.NIC = NIC
        self.OS = OS

    def __repr__(self):
        return "<User(HostName='%s',  Server='%s', CPU='%s', MEM='%s', NIC='%s',\
         OS='%s')>" % (self.HostName, self.Server, self.CPU, self.MEM, self.NIC, self.OS)


class TblTaskList(Base):
    __tablename__ = "TblTaskList"
    TaskID = Column(Integer, primary_key=True)
    TaskName = Column(String(const.NORMAL_VAR_LEN1))
    Date = Column(String(const.NORMAL_VAR_LEN1))
    EXTInfo = Column(String(const.EXT_INFO_LEN))

    def __init__(self, TaskName, Date, EXTInfo="", **kwargs):
        """Table of task"""
        self.TaskName = TaskName
        self.Date = Date
        self.EXTInfo = EXTInfo

    def __repr__(self):
        return "<User(TaskID='%s', TaskName='%s', Date='%s', EXTInfo='%s')>" % (
            self.TaskID, self.TaskName, self.Date, self.EXTInfo)


class TblTestList(Base):
    __tablename__ = "TblTestList"
    TestID = Column(Integer, primary_key=True)
    TaskID = Column(Integer, ForeignKey('TblTaskList.TaskID'))
    CaseTag = Column(String(const.CASE_TAG_LEN))
    Protocol = Column(String(const.PROTOCOL_LEN))
    Type = Column(String(const.TYPE_LEN))
    Switch = Column(String(const.SWITCH_LEN))
    Provider = Column(String(const.PROVIDER_LEN))
    Tools = Column(String(const.TOOLS_LEN))

    def __init__(self, taskid, casetag, protocol, typ, switch, provider, tools, **kwargs):
        """Table of test"""
        self.TaskID = taskid
        self.CaseTag = casetag
        self.Protocol = protocol
        self.Type = typ
        self.Switch = switch
        self.Provider = provider
        self.Tools = tools

    def __repr__(self):
        return "<User(TaskID='%d', CaseTag='%s', Protocol='%s', Type='%s', Switch=%s, Provider=%s, Tools='%s')>" % (
            self.TaskID, self.CaseTag, self.Protocol, self.Type, self.Switch, self.Provider, self.Tools)


class TblThroughput(Base):
    __tablename__ = "TblThroughput"
    Index = Column(Integer, primary_key=True)
    TestID = Column(Integer, ForeignKey('TblTestList.TestID'))
    AvgFrameSize = Column(Integer)
    OfferedLoad = Column(Float)
    PercentLoss = Column(Float)
    Bandwidth = Column(Float)
    MinimumLatency = Column(Float)
    MaximumLatency = Column(Float)
    AverageLatency = Column(Float)
    TxFrameCount = Column(Float)
    RxFrameCount = Column(Float)
    Duration = Column(Float)
    CPU = Column(Float)
    MppspGhz = Column(Float)

    def __init__(self, TestID, AvgFrameSize,
                 OfferedLoad, PercentLoss, Bandwidth,
                 MinimumLatency, MaximumLatency, AverageLatency,
                 TxFrameCount, RxFrameCount, Duration,
                 CPU, MppspGhz, **kwargs):
        """table of throughput"""
        self.TestID = TestID
        self.AvgFrameSize = AvgFrameSize
        self.OfferedLoad = OfferedLoad
        self.PercentLoss = PercentLoss
        self.Bandwidth = Bandwidth
        self.MinimumLatency = MinimumLatency
        self.MaximumLatency = MaximumLatency
        self.AverageLatency = AverageLatency
        self.TxFrameCount = TxFrameCount
        self.RxFrameCount = RxFrameCount
        self.Duration = Duration
        self.CPU = CPU
        self.MppspGhz = MppspGhz

    def __repr__(self):
        return "<User(TestID='%d', AvgFrameSize='%d', OfferedLoad='%f', \
                      PercentLoss='%f', MinimumLatency='%f', AverageLatency='%f', MaximumLatency='%f',\
                      TxFrameCount='%f', RxFrameCount='%f', Duration='%f', CPU='%f', MppspGhz='%f', \
                      Bandwidth='%f')>" % (self.TestID,
                                           self.AvgFrameSize, self.OfferedLoad, self.PercentLoss,
                                           self.MinimumLatency, self.AverageLatency, self.MaximumLatency,
                                           self.TxFrameCount,
                                           self.RxFrameCount, self.Duration, self.CPU, self.MppspGhz, self.Bandwidth)


class TblFrameloss(Base):
    __tablename__ = "TblFrameloss"
    Index = Column(Integer, primary_key=True)
    TestID = Column(Integer, ForeignKey('TblTestList.TestID'))
    AvgFrameSize = Column(Integer)
    OfferedLoad = Column(Float)
    PercentLoss = Column(Float)
    Bandwidth = Column(Float)
    MinimumLatency = Column(Float)
    MaximumLatency = Column(Float)
    AverageLatency = Column(Float)
    TxFrameCount = Column(Float)
    RxFrameCount = Column(Float)
    Duration = Column(Float)
    CPU = Column(Float)
    MppspGhz = Column(Float)

    def __init__(self, TestID, AvgFrameSize,
                 OfferedLoad, PercentLoss, Bandwidth,
                 MinimumLatency, MaximumLatency, AverageLatency,
                 TxFrameCount, RxFrameCount, Duration,
                 CPU, MppspGhz, **kwargs):
        """table of frameloss"""
        self.TestID = TestID
        self.AvgFrameSize = AvgFrameSize
        self.OfferedLoad = OfferedLoad
        self.PercentLoss = PercentLoss
        self.Bandwidth = Bandwidth
        self.MinimumLatency = MinimumLatency
        self.MaximumLatency = MaximumLatency
        self.AverageLatency = AverageLatency
        self.TxFrameCount = TxFrameCount
        self.RxFrameCount = RxFrameCount
        self.Duration = Duration
        self.CPU = CPU
        self.MppspGhz = MppspGhz

    def __repr__(self):
        return "<User(TestID='%d', AvgFrameSize='%d', OfferedLoad='%f', \
                      PercentLoss='%f', MinimumLatency='%f', AverageLatency='%f', MaximumLatency='%f',\
                      TxFrameCount='%f', RxFrameCount='%f', Duration='%f', CPU='%f', MppspGhz='%f', \
                      Bandwidth='%f')>" % (self.TestID,
                                           self.AvgFrameSize, self.OfferedLoad, self.PercentLoss,
                                           self.MinimumLatency, self.AverageLatency, self.MaximumLatency,
                                           self.TxFrameCount,
                                           self.RxFrameCount, self.Duration, self.CPU, self.MppspGhz, self.Bandwidth)


class TblLatency(Base):
    __tablename__ = "TblLatency"
    Index = Column(Integer, primary_key=True)
    TestID = Column(Integer, ForeignKey('TblTestList.TestID'))
    AvgFrameSize = Column(Integer)
    OfferedLoad = Column(Float)
    MinimumLatency = Column(Float)
    MaximumLatency = Column(Float)
    AverageLatency = Column(Float)

    def __init__(self, TestID, AvgFrameSize, OfferedLoad,
                 MinimumLatency, MaximumLatency, AverageLatency, **kwargs):
        """table of latency"""
        self.TestID = TestID
        self.AvgFrameSize = AvgFrameSize
        self.OfferedLoad = OfferedLoad
        self.MinimumLatency = MinimumLatency
        self.MaximumLatency = MaximumLatency
        self.AverageLatency = AverageLatency

    def __repr__(self):
        return "<User(TestID='%d', AvgFrameSize='%d', OfferedLoad='%f', \
                      MinimumLatency='%f', AverageLatency='%f', MaximumLatency='%f')>" % (self.TestID,
                                                                                          self.AvgFrameSize,
                                                                                          self.OfferedLoad,
                                                                                          self.MinimumLatency,
                                                                                          self.AverageLatency,
                                                                                          self.MaximumLatency)


class TblEXTInfo(Base):
    __tablename__ = "TblEXTInfo"
    Index = Column(Integer, primary_key=True)
    TaskID = Column(Integer)
    EXTName = Column(String(const.NORMAL_VAR_LEN))
    EXTContent = Column(String(const.DESC_LEN))
    Description = Column(String(const.NORMAL_VAR_LEN1))

    def __init__(self, TaskID, EXTName, EXTContent, Description, **kwargs):
        """table extern info"""
        self.TaskID = TaskID
        self.EXTName = EXTName
        self.EXTContent = EXTContent
        self.Description = Description

    def __repr__(self):
        return "<User(TaskID='%d', CodeType='%s', EXTContent='%s',Version='%s')>" % (
            self.TaskID, self.EXTName, self.EXTContent, self.Version)
