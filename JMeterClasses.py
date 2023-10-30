#Robot Framework JMeter Library
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Lesser General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import os
import string
import csv
import time
import datetime
import math
import sqlite3
import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation
from time import gmtime, strftime

class JMeterKeywords(object):
    def runJmeter(self, jmeterPath, testPlanPath, logFilePath, otherParams=""):
        """
        Runs JMeter. Returns None.
        Parameters:
            - jmeterPath - path to JMeter executable file
            - testPlanPath - path to jmx file
            - logFilePath - path to a log file
            - otherParams (optional) - other parameters to be called
        Examples:
        | run jmeter | D:/apache-jmeter-2.12/bin/jmeter.bat | D:/Tests/Test1Thread1Loop.jmx | D:/Tests/output1.jtl |
        | run jmeter | D:/apache-jmeter-2.12/bin/jmeter.bat | D:/Tests/Test1Thread1Loop.jmx | D:/Tests/output1.jtl | -H my.proxy.server -P 8000 |
        """
        JMeterRunner(jmeterPath, testPlanPath, logFilePath, otherParams)

    def runJmeterAnalyseJtlConvert(self, jmeterPath, testPlanPath, logFilePath, otherParams="", disableReports=None):
        """
        Runs JMeter and parses log file. Converts results into HTML and SQLite format.
        Returns list of dictionaries containing summary report of parsed output.
        Parameters:
            - jmeterPath - path to JMeter executable file
            - testPlanPath - path to jmx file
            - logFilePath - path to a log file
            - otherParams (optional) - other parameters to be called
            - disableReports - optional paramter for disabling particular parts of html report.
             It requires integer value which is composed of bits which meaning is
             as follows (binary numebers in Python notation):
    			 0b00000001 -> disable aggregated report and graph;
    			 0b00000010 -> disable aggregated samples;
    			 0b00000100 -> disable response time graph;
    			 0b00001000 -> disable all samples;
              For example disabling aggr samples and resp time graph needs 0b00000110 which is integer 6.
        Examples:
        | run jmeter analyse jtl convert | D:/apache-jmeter-2.12/bin/jmeter.bat | D:/Tests/Test1Thread1Loop.jmx | D:/Tests/output1.jtl |
        | run jmeter analyse jtl convert | D:/apache-jmeter-2.12/bin/jmeter.bat | D:/Tests/Test1Thread1Loop.jmx | D:/Tests/output1.jtl | -H my.proxy.server -P 8000 |
        """
        JMeterRunner(jmeterPath, testPlanPath, logFilePath, otherParams)
        lai = LogAnalysisInitiator(logFilePath, True, True, disableReports=disableReports)
        return lai.getReturnStructure()

    def runJmeterAnalyseJtlConvertToDb(self, jmeterPath, testPlanPath, logFilePath, otherParams=""):
        """
        Runs JMeter and parses log file. Converts results into SQLite format.
        Returns list of dictionaries containing summary report of parsed output.
        Parameters:
            - jmeterPath - path to JMeter executable file
            - testPlanPath - path to jmx file
            - logFilePath - path to a log file
            - otherParams (optional) - other parameters to be called
        Examples:
        | run jmeter analyse jtl convert to db | D:/apache-jmeter-2.12/bin/jmeter.bat | D:/Tests/Test1Thread1Loop.jmx | D:/Tests/output1.jtl |
        | run jmeter analyse jtl convert to db | D:/apache-jmeter-2.12/bin/jmeter.bat | D:/Tests/Test1Thread1Loop.jmx | D:/Tests/output1.jtl | -H my.proxy.server -P 8000 |
        """
        JMeterRunner(jmeterPath, testPlanPath, logFilePath, otherParams)
        lai = LogAnalysisInitiator(logFilePath, True)
        return lai.getReturnStructure()

    def runJmeterAnalyseJtlConvertToHtml(self, jmeterPath, testPlanPath, logFilePath, otherParams="", disableReports=None):
        """
        Runs JMeter and parses log file. Converts results into html format.
        Returns list of dictionaries containing summary report of parsed output.
        Parameters:
            - jmeterPath - path to JMeter executable file
            - testPlanPath - path to jmx file
            - logFilePath - path to a log file
            - otherParams (optional) - other parameters to be called
            - disableReports - optional paramter for disabling particular parts of html report.
             It requires integer value which is composed of bits which meaning is
             as follows (binary numebers in Python notation):
    			 0b00000001 -> disable aggregated report and graph;
    			 0b00000010 -> disable aggregated samples;
    			 0b00000100 -> disable response time graph;
    			 0b00001000 -> disable all samples;
              For example disabling aggr samples and resp time graph needs 0b00000110 which is integer 6.
        Examples:
        | run jmeter analyse jtl convert to html | D:/apache-jmeter-2.12/bin/jmeter.bat | D:/Tests/Test1Thread1Loop.jmx | D:/Tests/output1.jtl |
        | run jmeter analyse jtl convert to html | D:/apache-jmeter-2.12/bin/jmeter.bat | D:/Tests/Test1Thread1Loop.jmx | D:/Tests/output1.jtl | -H my.proxy.server -P 8000 |
        """
        JMeterRunner(jmeterPath, testPlanPath, logFilePath, otherParams)
        lai = LogAnalysisInitiator(logFilePath, createHtmlReport=True, disableReports=disableReports)
        return lai.getReturnStructure()

    def runJmeterAnalyseJtl(self, jmeterPath, testPlanPath, logFilePath, otherParams=""):
        """
        Runs JMeter and parses log file.
        Returns list of dictionaries containing summary report of parsed output.
        Parameters:
            - jmeterPath - path to JMeter executable file
            - testPlanPath - path to jmx file
            - logFilePath - path to a log file
            - otherParams (optional) - other parameters to be called
        Examples:
        | run jmeter analyse jtl | D:/apache-jmeter-2.12/bin/jmeter.bat | D:/Tests/Test1Thread1Loop.jmx | D:/Tests/output1.jtl |
        | run jmeter analyse jtl | D:/apache-jmeter-2.12/bin/jmeter.bat | D:/Tests/Test1Thread1Loop.jmx | D:/Tests/output1.jtl | -H my.proxy.server -P 8000 |
        """
        JMeterRunner(jmeterPath, testPlanPath, logFilePath, otherParams)
        lai = LogAnalysisInitiator(logFilePath)
        return lai.getReturnStructure()

    def analyseJtlConvert(self, logFilePath, disableReports=None):
        """
        Parses JMeter log file. Converts results into HTML and SQLite format.
        Returns list of dictionaries containing summary report of parsed output.
        Parameters:
            - logFilePath - path to a log file
            - disableReports - optional paramter for disabling particular parts of html report.
             It requires integer value which is composed of bits which meaning is
             as follows (binary numebers in Python notation):
    			 0b00000001 -> disable aggregated report and graph;
    			 0b00000010 -> disable aggregated samples;
    			 0b00000100 -> disable response time graph;
    			 0b00001000 -> disable all samples;
              For example disabling aggr samples and resp time graph needs 0b00000110 which is integer 6.
        Examples:
        | analyse jtl convert | D:/Tests/output1.jtl |
        """
        lai = LogAnalysisInitiator(logFilePath, True, True, disableReports=disableReports)
        return lai.getReturnStructure()

    def analyseJtlConvertToDb(self, logFilePath):
        """
        Parses JMeter log file. Converts results into SQLite format.
        Returns list of dictionaries containing summary report of parsed output.
        Parameters:
            - logFilePath - path to a log file
        Examples:
        | analyse jtl convert to db | D:/Tests/output1.jtl |
        """
        lai = LogAnalysisInitiator(logFilePath, True)
        return lai.getReturnStructure()

    def analyseJtlConvertToHtml(self, logFilePath, disableReports=None):
        """
        Parses JMeter log file. Converts results into HTML format.
        Returns list of dictionaries containing summary report of parsed output.
        Parameters:
            - logFilePath - path to a log file
            - disableReports - optional paramter for disabling particular parts of html report.
             It requires integer value which is composed of bits which meaning is
             as follows (binary numebers in Python notation):
    			 0b00000001 -> disable aggregated report and graph;
    			 0b00000010 -> disable aggregated samples;
    			 0b00000100 -> disable response time graph;
    			 0b00001000 -> disable all samples;
              For example disabling aggr samples and resp time graph needs 0b00000110 which is integer 6.
        Examples:
        | analyse jtl convert to html | D:/Tests/output1.jtl |
        """
        lai = LogAnalysisInitiator(logFilePath, createHtmlReport=True, disableReports=disableReports)
        return lai.getReturnStructure()

    def analyseJtl(self, logFilePath):
        """
        Parses JMeter log file.
        Returns list of dictionaries containing summary report of parsed output.
        Parameters:
            - logFilePath - path to a log file
        Examples:
        | analyse jtl | D:/Tests/output1.jtl |
        """
        lai = LogAnalysisInitiator(logFilePath)
        return lai.getReturnStructure()

class JMeterRunner(object):
    def __init__(self, jmeterPath, testPlanPath, logFilePath, otherParams):
        self.jmeter = jmeterPath
        self.jmx = testPlanPath
        self.log = logFilePath
        self.paramsStr = otherParams
        self.validateInput()
        self.listOtherParams()
        print(self)
        jmeterOutput = self.runAndPrintResult()

    def __str__(self):
        runnerPrint = "Starting JMeter with following parameters:\n"
        runnerPrint += " - JMeter path: " + self.jmeter + "\n"
        runnerPrint += " - Test plan path: " + self.jmx + "\n"
        runnerPrint += " - Log file path: " + self.log + "\n"
        runnerPrint += " - Other parameters: " + self.paramsStr + " ."
        return runnerPrint

    def validateInput(self):
        import os.path as op
        if not op.isfile(self.jmeter):
            raise JMeterLibException("Wrong JMeter path.")
        elif not op.isfile(self.jmx):
            raise JMeterLibException("Wrong test plan path.")

    def listOtherParams(self):
        self.params = []
        if not self.paramsStr == "":
            self.params = str.split(self.paramsStr)

    def runAndPrintResult(self):
        import subprocess
        runList = [self.jmeter, "-n", "-t", self.jmx, "-l", self.log]
        if len(self.params) > 0:
            for p in self.params:
                runList.append(p)
        print("subprocess.call input list: " + str(runList))
        retValue = subprocess.call(runList)
        msg = "Value returned by JMeter:"
        if retValue == 0:
            print("%s %s" % (msg, retValue))
        else:
            raise JMeterLibException("%s %s" % (msg, retValue))

class JMeterLibException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
         return repr(self.msg)

class LogAnalysisInitiator(object):
    def __init__(self, filePath, createSqlReport=False, createHtmlReport=False, disableReports=None):
        debugNeeded = False
        self.jtlPath = filePath
        self.timeStamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.analyserObject = self.initiateNewAnalyserObject()
        self.aggrSummary, self.aggrSamples, self.samples = self.analyserObject.analyzeLog()
        if debugNeeded:
            print("aggrSummary")
            print(self.aggrSummary)
            print("aggrSamples")
            print(self.aggrSamples)
            print("samples")
            print(self.samples)
        if createHtmlReport:
            self.convertLogToHtml(disableReports)
        if createSqlReport:
            self.convertLogToSql()

    def recognizeFormat(self, fileLines):
        logFileFormat = ""
        logLength = len(fileLines)
        if logLength > 1:
            if re.search("xml version",fileLines[0]) and re.search("<testResults", fileLines[1]):
                logFileFormat = "xml"
        if logLength > 0 and logFileFormat != "xml":
            #if re.search("\d+,\d+,[^,]+,\d+,\w+,[^,]+,\w+,\w+,\d+,\d+", fileLines[0]):
            if re.search("\d+,\d+,.*", fileLines[0]):
                logFileFormat = "csv"
            if re.search("timeStamp,elapsed,label", fileLines[0]):
                if re.search("\d+,\d+,.*", fileLines[1]):
                    logFileFormat = "csv"
        return logFileFormat

    def initiateNewAnalyserObject(self):
        newObject = None
        newFileLines = []
        print("Opening log file " + self.jtlPath)
        try:
            logFileHandler = open(self.jtlPath, 'r')
            newFileLines = logFileHandler.readlines()
            logFileHandler.close()
        except IOError:
            raise JMeterLibException("File %s couldn't be opened" % self.jtlPath)
        else:
            if self.recognizeFormat(newFileLines) == "csv":
                newObject = CsvLogAnalyser(self.jtlPath)
                print("Log file format: csv")
            elif self.recognizeFormat(newFileLines) == "xml":
                newObject = XmlLogAnalyser(self.jtlPath)
                print("Log file format: xml")
            else:
                raise JMeterLibException("Incorrect log file format")
        return newObject

    def convertLogToHtml(self, disableReports=None):
        self.lc = LogConverterHtml(self, disableReports=disableReports)
        self.lc.createNewHtmlPath()
        self.lc.createHtml(disableReports)

    def convertLogToSql(self):
        self.ls = LogConverterSql(self)
        self.ls.createSql()

    def getReturnStructure(self):
        retStruct = []
        retStruct.append(self.aggrSummary.convertToDictionary())
        for ags in self.aggrSamples:
            retStruct.append(ags.convertToDictionary())
        return retStruct

class LogAnalyser(object):
    def __init__(self, filePath):
        self.filePath = filePath
        self.dbReady = False

    def analyzeLog(self):
        self.getSamples()
        if len(self.samples) > 0:
            self.calculate()
            return (self.aggrSummary, self.aggrSamples, self.samples)
        else:
            return (None, None, None)

    def printSamples(self):
        for s in self.samples:
            print(s)

    def calculate(self):
        print("Calculating statistical values")
        self.aggrSummary = AggregatedSummary()
        self.aggrSamples = []
        self.totalSamples = AggregatedSamples("TOTAL")
        for s in self.samples:
            whichAggr = self.checkWhichAggregated(s.getLabel(), s.getStartTime())
            if self.totalSamples.getStartTime()==None:
                self.totalSamples.setStartTime(s.getStartTime())
            sampleWithAssertOk = False
            self.aggrSummary.addSample()
            self.aggrSummary.addMinTime(s.getSampleTime())
            self.aggrSummary.addMaxTime(s.getSampleTime())
            self.aggrSummary.addAverageTime(s.getSampleTime())
            self.aggrSamples[whichAggr].addSample()
            self.aggrSamples[whichAggr].addTime(s.getSampleTime())
            self.aggrSamples[whichAggr].addMinTime(s.getSampleTime())
            self.aggrSamples[whichAggr].addMaxTime(s.getSampleTime())
            self.aggrSamples[whichAggr].addAverageTime(s.getSampleTime())
            self.aggrSamples[whichAggr].addAverageBytes(s.getBytes())
            self.aggrSamples[whichAggr].setEndTime(s.getStartTime(), s.getSampleTime())
            self.totalSamples.addSample()
            self.totalSamples.addTime(s.getSampleTime())
            self.totalSamples.addMinTime(s.getSampleTime())
            self.totalSamples.addMaxTime(s.getSampleTime())
            self.totalSamples.addAverageTime(s.getSampleTime())
            self.totalSamples.addAverageBytes(s.getBytes())
            self.totalSamples.setEndTime(s.getStartTime(), s.getSampleTime())
            if s.getStatus() == "true":
                self.aggrSummary.addSuccessfullSampleNoAssert()
                self.aggrSamples[whichAggr].addSuccessfullSampleNoAssert()
                self.totalSamples.addSuccessfullSampleNoAssert()
                sampleWithAssertOk = True
            for a in s.assertions:
                self.aggrSummary.addAssertion()
                self.aggrSamples[whichAggr].addAssertion()
                self.totalSamples.addAssertion()
                if a.getFailure() == "False" and a.getError() == "False":
                     self.aggrSummary.addAssertionPassRate()
                     self.aggrSamples[whichAggr].addAssertionPassRate()
                     self.totalSamples.addAssertionPassRate()
                else:
                    sampleWithAssertOk = False
            if sampleWithAssertOk:
                self.aggrSummary.addSuccessfullSampleInclAssert()
                self.aggrSamples[whichAggr].addSuccessfullSampleInclAssert()
                self.totalSamples.addSuccessfullSampleInclAssert()
        self.aggrSummary.calculateAverageTime()
        self.aggrSummary.calculateSampleSuccessRateNoAssert()
        self.aggrSummary.calculateSampleSuccessRateInclAssert()
        self.aggrSummary.calculateAssertionPassRate()
        self.aggrSamples.append(self.totalSamples)
        for agg in self.aggrSamples:
            agg.calculateAverageTime()
            agg.calculateSampleSuccessRateNoAssert()
            agg.calculateSampleSuccessRateInclAssert()
            agg.calculateThroughput()
            agg.calculateAverageBytes()
            agg.calculateKBytesPerSec()
            agg.calculatePercentils()
            agg.calculateStdDev()

    def checkWhichAggregated(self, name, start):
        aggrId = -1
        counter = -1
        startTime = ""
        for a in self.aggrSamples:
            counter += 1
            if name == a.sampleName:
                aggrId = counter
                startTime = a.startTime
                break
        if aggrId < 0:
            aggrId = counter + 1
            self.aggrSamples.append(AggregatedSamples(name, aggrId))
            self.aggrSamples[aggrId].setStartTime(start)
        return aggrId

    def convertLogToHtml(self):
        self.lc = LogConverterHtml(self)
        self.lc.createNewHtmlPath()
        self.lc.createHtml()

    def convertLogToSql(self, dbname, dbReady):
        self.ls = LogConverterSql(self, dbname, dbReady)
        self.ls.createSql()

class CsvLogAnalyser(LogAnalyser):
    def getSamples(self):
        print("Extracting samples and assertions from " + self.filePath)
        self.samples = []
        try:
            with open(self.filePath, "r") as csvfile:
                csvReader = csv.reader(csvfile, delimiter=",", quoting=csv.QUOTE_ALL, quotechar="\"")
                header_found = False
                counter = 0
                for row in csvReader:
                    newSample = None
                    if counter==0:
                        try:
                            if row[0].find('timeStamp') == 0 and row[1].find('elapsed') == 0 and row[0].find('timeStamp') == 0:
                                header_found = True
                        except Exception as e:
                            pass
                    if header_found:
                        if counter >= 1:
                            newSample = Sample(ts=row[0], t=row[1], lb=row[2], rc=row[3],
                                               rm=row[4], tn=row[5], dt=row[6], s=row[7],
                                               by=row[9], lt=row[13])
                    elif len(row) == 10 and self.validateCsvSampleAttributes(row):
                        newSample = Sample(ts=row[0], t=row[1], lb=row[2], rc=row[3],
                                           rm=row[4], tn=row[5], dt=row[6], s=row[7],
                                           by=row[8], lt=row[9])
                    elif len(row) == 12 and self.validateCsvSampleAttributes(row):
                        newSample = Sample2(ts=row[0], t=row[1], lb=row[2], rc=row[3],
                                           rm=row[4], tn=row[5], dt=row[6], s=row[7],
                                           by=row[8], lt=row[9], ng=row[10], na=row[11])
                    if type(newSample) == Sample or type(newSample) == Sample2:
                        self.samples.append(newSample)
                    counter += 1
        except IOError:
            print("ERROR, problems while reading " + str(self.filePath))
        if len(self.samples) <= 0:
            raise JMeterLibException("No samples were found in a log file.")

    def validateCsvSampleAttributes(self, row):
        validated = True
        try:
            intValue = int(row[0])
            intValue = int(row[1])
            intValue = int(row[8])
            intValue = int(row[9])
        except ValueError:
            validated = False
        return validated

class XmlLogAnalyser(LogAnalyser):
    def getSamples(self):
        print("Extracting samples and assertions from " + self.filePath)
        self.samples = []
        try:
            xmlLog = xml.dom.minidom.parse(self.filePath)
        except IOError:
            print("ERROR, problems while reading " + str(self.filePath))
        except xml.parsers.expat.ExpatError:
            print("ERROR, problems while parsing xml")
        else:
            testResultNodes = xmlLog.getElementsByTagName("testResults")
            if len(testResultNodes) > 0:
                testResultNode = testResultNodes[0]
                samplesNodes = testResultNode.childNodes
                for s in samplesNodes:
                    newSample = None
                    if isinstance(s, xml.dom.minidom.Element):
                        if self.validateXmlSampleAttributes(s):
                            if s.hasAttribute('ng') and s.hasAttribute('na'):
                                newSample = Sample2(ts=s.getAttribute('ts'), t=s.getAttribute('t'),
                                               lb=s.getAttribute('lb'), rc=s.getAttribute('rc'),
                                               rm=s.getAttribute('rm'), tn=s.getAttribute('tn'),
                                               dt=s.getAttribute('dt'), s=s.getAttribute('s'),
                                               by=s.getAttribute('by'), lt=s.getAttribute('lt'),
                                               na=s.getAttribute('na'), ng=s.getAttribute('ng'))
                            else:
                                newSample = Sample(ts=s.getAttribute('ts'), t=s.getAttribute('t'),
                                               lb=s.getAttribute('lb'), rc=s.getAttribute('rc'),
                                               rm=s.getAttribute('rm'), tn=s.getAttribute('tn'),
                                               dt=s.getAttribute('dt'), s=s.getAttribute('s'),
                                               by=s.getAttribute('by'), lt=s.getAttribute('lt'))
                            assertNodes = s.childNodes
                            newSample.assertions = []
                            for a in assertNodes:
                                newAssertion = None
                                if isinstance(a, xml.dom.minidom.Element):
                                    nameTagString = self.getAssertionFields("name", a)
                                    failureTagString = self.getAssertionFields("failure", a)
                                    failureMessageTagString = self.getAssertionFields("failureMessage", a)
                                    errorTagString = self.getAssertionFields("error", a)
                                    newAssertion = Assertion(name=nameTagString, failure=failureTagString, failureMessage=failureMessageTagString, error=errorTagString)
                                    newSample.addAssertion(newAssertion)
                            if isinstance(newSample, Sample) or isinstance(newSample, Sample2):
                                self.samples.append(newSample)
        if len(self.samples) <= 0:
            raise JMeterLibException("No samples were found in a log file.")

    def validateXmlSampleAttributes(self, element):
        validated = True
        attributes = ['ts','t','lb','rc','rm','tn','dt','s','by','lt']
        for a in attributes:
            if not element.hasAttribute(a):
                validated = False
                break
        if validated:
            try:
                intValue = int(element.getAttribute('ts'))
                intValue = int(element.getAttribute('t'))
                intValue = int(element.getAttribute('lt'))
                intValue = int(element.getAttribute('by'))
            except ValueError:
                validated = False
        return validated

    def getAssertionFields(self, tag, elem):
        someTagString = ""
        if len(elem.getElementsByTagName(tag)) >= 1:
            someTag = elem.getElementsByTagName(tag)[0]
            someTagString = someTag.toxml()
            someTagString = someTagString.replace("<" + tag + ">", "")
            someTagString = someTagString.replace("</" + tag + ">", "")
        return someTagString

class Sample(object):
    def __init__(self, **values):
        self.assertions = []
        if 'ts' in values:
            self.setStartTime(values['ts'])
        if 't' in values:
            self.setSampleTime(values['t'])
        if 'lb' in values:
            self.setLabel(values['lb'])
        if 'rc' in values:
            self.setRespCode(values['rc'])
        if 'rm' in values:
            self.setRespMsg(values['rm'])
        if 'tn' in values:
            self.setThreadName(values['tn'])
        if 'dt' in values:
            self.setDataType(values['dt'])
        if 's' in values:
            self.setStatus(values['s'])
        if 'by' in values:
            self.setBytes(values['by'])
        if 'lt' in values:
            self.setLatency(values['lt'])

    def setStartTime(self, ts):
        self.startTime = ts

    def getStartTime(self):
        return self.startTime

    def setSampleTime(self, t):
        self.sampleTime = t

    def getSampleTime(self):
        return self.sampleTime

    def setLabel(self, lb):
        self.label = lb

    def getLabel(self):
        return self.label

    def setRespCode(self, rc):
        self.respCode = rc

    def getRespCode(self):
        return self.respCode

    def setRespMsg(self, rm):
        self.respMsg = rm

    def getRespMsg(self):
        return self.respMsg

    def setThreadName(self, tn):
        self.threadName = tn

    def getThreadName(self):
        return self.threadName

    def setDataType(self, dt):
        self.dataType = dt

    def getDataType(self):
        return self.dataType

    def setStatus(self, s):
        self.status = s

    def getStatus(self):
        return self.status

    def setBytes(self, by):
        self.bytes = by

    def getBytes(self):
        return self.bytes

    def setLatency(self, lt):
        self.latency = lt

    def getLatency(self):
        return self.latency

    def addAssertion(self, a):
        self.assertions.append(a)

    def getAssertions(self):
        return self.assertions

class Sample2(Sample):
    def __init__(self, **values):
        super(Sample2, self).__init__(**values)
        if 'ng' in values:
            self.setNg(values['ng'])
        if 'na' in values:
            self.setNa(values['na'])

    def setNg(self, Ng):
        self.ng = Ng

    def setNa(self, Na):
        self.na = Na

class Assertion(object):
    def __init__(self, **values):
        if 'name' in values:
            self.setName(values['name'])
        if 'failure' in values:
            self.setFailure(values['failure'])
        if 'failureMessage' in values:
            self.setFailureMsg(values['failureMessage'])
        if 'error' in values:
            self.setError(values['error'])

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setFailure(self, fail):
        if fail=='true':
            self.failure = True
        else:
            self.failure = False

    def getFailure(self):
        return str(self.failure)

    def setFailureMsg(self, failmsg):
        self.failureMessage = failmsg

    def getFailureMsg(self):
        return self.failureMessage

    def setError(self, err):
        if err == 'true':
            self.error = True
        else:
            self.error = False

    def getError(self):
        return str(self.error)

class AggregatedSummary(object):
    def __init__(self):
        self.initiateAll()

    def initiateAll(self):
        self.samples = 0
        self.assertions = 0
        self.samplesSuccessRateNoAssert = 0
        self.samplesSuccessRateInclAssert = 0
        self.assertionPassRate = 0
        self.averageTime = 0
        self.minTime = None
        self.maxTime = 0

    def convertToDictionary(self):
        aggrSumDict = {}
        aggrSumDict['samples'] = self.samples
        aggrSumDict['assertions'] = self.assertions
        aggrSumDict['samplesSuccessRateNoAssert'] = self.samplesSuccessRateNoAssert
        aggrSumDict['samplesSuccessRateInclAssert'] = self.samplesSuccessRateInclAssert
        aggrSumDict['assertionPassRate'] = self.assertionPassRate
        aggrSumDict['averageTime'] = self.averageTime
        aggrSumDict['minTime'] = self.minTime
        aggrSumDict['maxTime'] = self.maxTime
        return aggrSumDict

    def addSample(self):
        self.samples += 1

    def getAmountOfSamples(self):
        return self.samples

    def addAssertion(self):
        self.assertions += 1

    def getAmountOfAssertions(self):
        return self.assertions

    def addSuccessfullSampleNoAssert(self):
        self.samplesSuccessRateNoAssert += 1

    def calculateSampleSuccessRateNoAssert(self):
        if self.samples > 0:
            self.samplesSuccessRateNoAssert = self.samplesSuccessRateNoAssert*100 / self.samples
            if type(self.samplesSuccessRateNoAssert) == float:
                self.samplesSuccessRateNoAssert = "%.2f" % self.samplesSuccessRateNoAssert

    def getSamplesSuccessRateNoAssert(self):
        return self.samplesSuccessRateNoAssert

    def addSuccessfullSampleInclAssert(self):
        self.samplesSuccessRateInclAssert += 1

    def calculateSampleSuccessRateInclAssert(self):
        if self.samples > 0:
            self.samplesSuccessRateInclAssert = self.samplesSuccessRateInclAssert*100 / self.samples
            if type(self.samplesSuccessRateInclAssert) == float:
                self.samplesSuccessRateInclAssert = "%.2f" % self.samplesSuccessRateInclAssert

    def getSamplesSuccessRateInclAssert(self):
        return self.samplesSuccessRateInclAssert

    def addAssertionPassRate(self):
        self.assertionPassRate += 1

    def calculateAssertionPassRate(self):
        if self.assertions > 0:
            self.assertionPassRate = self.assertionPassRate*100 / self.assertions
            if type(self.assertionPassRate) == float:
                self.assertionPassRate = "%.2f" % self.assertionPassRate

    def getAssertionPassRate(self):
        return self.assertionPassRate

    def addAverageTime(self, t):
        if isinstance(t, str):
            t = int(t)
        self.averageTime += t

    def calculateAverageTime(self):
        if self.samples > 0:
            self.averageTime = self.averageTime/self.samples
            if type(self.averageTime) == float:
                self.averageTime = "%.2f" % self.averageTime

    def getAverageTime(self):
        return self.averageTime

    def addMinTime(self, t):
        if type(t) == str:
            t = int(t)
        if self.minTime == None:
            self.minTime = t
        elif t < self.minTime:
            self.minTime = t

    def getMinTime(self):
        return self.minTime

    def addMaxTime(self, t):
        if type(t) == str:
            t = int(t)
        if t > self.maxTime:
            self.maxTime = t

    def getMaxTime(self):
        return self.maxTime

class AggregatedSamples(AggregatedSummary):
    def __init__(self, name, Id=-1):
        super(AggregatedSamples,self).__init__()
        self.sampleName = name
        self.makeLink(Id)
        self.samplesErrorNoAssert = 0
        self.samplesErrorInclAssert = 0
        self.startTime = None
        self.endTime = None
        self.totalTime = None
        self.throughput = 0
        self.averageBytes = 0
        self.bytesPerSec = 0
        self.kBytesPerSec = 0
        self.median = 0
        self.stddev = 0
        self.percentil90 = 0
        self.timeTable = []

    def convertToDictionary(self):
        aggrSamplDict = {}
        aggrSamplDict['sampleName'] = self.sampleName
        aggrSamplDict['samplesErrorNoAssert'] = self.samplesErrorNoAssert
        aggrSamplDict['samplesErrorInclAssert'] = self.samplesErrorInclAssert
        aggrSamplDict['samplesSuccessRateNoAssert'] = self.samplesSuccessRateNoAssert
        aggrSamplDict['samplesSuccessRateInclAssert'] = self.samplesSuccessRateInclAssert
        aggrSamplDict['startTime'] = self.startTime
        aggrSamplDict['endTime'] = self.endTime
        aggrSamplDict['totalTime'] = self.totalTime
        aggrSamplDict['throughput'] = self.throughput
        aggrSamplDict['averageBytes'] = self.averageBytes
        aggrSamplDict['bytesPerSec'] = self.bytesPerSec
        aggrSamplDict['kBytesPerSec'] = self.kBytesPerSec
        aggrSamplDict['median'] = self.median
        aggrSamplDict['stddev'] = self.stddev
        aggrSamplDict['percentil90'] = self.percentil90
        aggrSamplDict['timeTable'] = self.timeTable
        return aggrSamplDict

    def makeLink(self, which):
        if which == -1 and self.sampleName == "TOTAL":
            self.link = "samples_"
        else:
            self.link = "aggr" + str(which)

    def calculateSampleSuccessRateNoAssert(self):
        if self.samples > 0:
            self.samplesSuccessRateNoAssert = self.samplesSuccessRateNoAssert*100 / self.samples
            self.samplesErrorNoAssert = 100 - self.samplesSuccessRateNoAssert
            if type(self.samplesSuccessRateNoAssert) == float:
                self.samplesSuccessRateNoAssert = "%.2f" % self.samplesSuccessRateNoAssert
                self.samplesErrorNoAssert = "%.2f" % self.samplesErrorNoAssert

    def getSampleErrorNoAssert(self):
        return self.samplesErrorNoAssert

    def calculateSampleSuccessRateInclAssert(self):
        if self.samples > 0:
            self.samplesSuccessRateInclAssert = self.samplesSuccessRateInclAssert*100 / self.samples
            self.samplesErrorInclAssert = 100 - self.samplesSuccessRateInclAssert
            if type(self.samplesSuccessRateInclAssert) == float:
                self.samplesSuccessRateInclAssert = "%.2f" % self.samplesSuccessRateInclAssert
                self.samplesErrorInclAssert = "%.2f" % self.samplesErrorInclAssert

    def getSampleErrorInclAssert(self):
        return self.samplesErrorInclAssert

    def setStartTime(self, t):
        self.startTime = datetime.datetime.fromtimestamp(int(t) / 1e3)

    def getStartTime(self):
        return self.startTime

    def setEndTime(self, t, p):
        start = int(t)
        duration = int(p)
        if self.endTime == None:
            self.endTime = datetime.datetime.fromtimestamp(start / 1e3)
            timeDiff = self.endTime - self.startTime
            self.totalTime = timeDiff.total_seconds() + (duration / 1000)
        else:
            newEndTime = datetime.datetime.fromtimestamp(start / 1e3)
            newTimeDiff = newEndTime - self.startTime
            newTotalTime = newTimeDiff.total_seconds() + (duration / 1000)
            if newTotalTime > self.totalTime:
                self.totalTime = newTotalTime
                self.endTime = newEndTime

    def calculateThroughput(self):
        if self.totalTime > 0:
            self.throughput = self.samples / self.totalTime
            self.throughput = "%.2f" % self.throughput

    def getThroughput(self):
        return self.throughput

    def addAverageBytes(self, b):
        if isinstance(b, str):
            b = int(b)
        self.averageBytes = self.averageBytes + b
        self.addBytesPerSec(b)

    def calculateAverageBytes(self):
        if self.samples > 0:
            self.averageBytes = self.averageBytes / self.samples
            if type(self.averageBytes) == float:
                self.averageBytes = "%.1f" % self.averageBytes

    def getAverageBytes(self):
        return self.averageBytes

    def addBytesPerSec(self, b):
        self.bytesPerSec = self.bytesPerSec + b

    def calculateKBytesPerSec(self):
        if self.totalTime > 0:
            self.bytesPerSec = self.bytesPerSec / self.totalTime
            self.kBytesPerSec = self.bytesPerSec / 1000
            if type(self.kBytesPerSec) == float:
                self.kBytesPerSec = "%.1f" % self.kBytesPerSec

    def getKBytesPerSec(self):
        return self.kBytesPerSec

    def calculatePercentils(self):
        medianSample = 0
        perc90Sample = 0
        sortedSamples = sorted(self.timeTable)
        if self.samples%2 == 0:
            medianSample = self.samples / 2
            medianSample = int(medianSample)
            if len(sortedSamples) > medianSample and (medianSample-1) >= 0:
                self.median = (sortedSamples[medianSample] + sortedSamples[medianSample-1]) / 2
                self.median = int(self.median)
        else:
            if self.samples > 1:
                medianSample = (self.samples // 2)
                medianSample = int(medianSample)
            elif self.samples == 1:
                medianSample = 0
            if len(sortedSamples) > medianSample:
                self.median = sortedSamples[medianSample]
                self.median = int(self.median)
                self.median = sortedSamples[medianSample]
        perc90Sample = round((0.9*self.samples) + 0.5)
        perc90Sample = int(perc90Sample)
        if len(sortedSamples) == perc90Sample:
            perc90Sample = perc90Sample - 1
        if len(sortedSamples) > perc90Sample:
            self.percentil90 = sortedSamples[perc90Sample]

    def getMedian(self):
        return self.median

    def calculateStdDev(self):
        squares = 0
        sortedSamples = sorted(self.timeTable)
        for s in sortedSamples:
            squares = squares + ((s-float(self.averageTime)) ** 2)
        self.stddev = math.sqrt(squares / self.samples)
        if type(self.stddev) == float:
            self.stddev = "%.1f" % self.stddev

    def getStdDev(self):
        return self.stddev

    def getPerc90(self):
        return self.percentil90

    def addTime(self, t):
        self.timeTable.append(int(t))

class LogConverterSql(object):
    def __init__(self, parentHandler):
        dbReady = False
        self.loganalyser = parentHandler
        self.dbStatus = True
        self.dbName = self.loganalyser.jtlPath + ".sql"
        self.checkIfDbFileExists()
        self.readDbInTheEnd = False
        try:
            if dbReady:
                print("Accessing SQLite DB file " + self.dbName)
            else:
                print("Creating SQLite DB file " + self.dbName)
            self.db = sqlite3.connect(self.dbName)
        except sqlite3.Error:
            if dbReady:
                print("ERROR while accessing " + self.dbName)
            else:
                print("ERROR while creating " + self.dbName)
            self.dbStatus = False
        if not dbReady:
            self.createStructure2()

    def checkIfDbFileExists(self):
        while os.path.isfile(self.dbName):
            self.dbName = self.loganalyser.jtlPath + strftime("%Y%m%d%H%M%S", gmtime()) + ".sql"

    def createSql(self):
        if self.dbStatus:
            testRunId = self.insertTestrun()
            idNameDict = self.insertAggregations(testRunId)
            self.insertSamples(idNameDict)
            self.testDb()
            self.closeDb()

    def closeDb(self):
        self.db.close()

    def createStructure(self):
        sqlSchema = ""
        sqlSchemaFilePath ="schema.sql"
        if self.dbStatus:
            try:
                sqlSchemaFile = open(sqlSchemaFilePath,'r')
                sqlSchema = sqlSchemaFile.read()
                sqlSchemaFile.close()
            except:
                print("ERROR, problems while reading " + sqlSchemaFilePath)
                self.dbStatus = False
            if sqlSchema!="" :
                try:
                   dbCursor = self.db.cursor()
                   dbCursor.executescript(sqlSchema)
                except sqlite3.Error:
                   print("ERROR while creating db schema")
                   self.dbStatus = False

    def createStructure2(self):
        sqlSchema = self.getSqlSchema()
        if self.dbStatus:
            if sqlSchema!="" :
                try:
                   dbCursor = self.db.cursor()
                   dbCursor.executescript(sqlSchema)
                except sqlite3.Error:
                   print("ERROR while creating db schema")
                   self.dbStatus = False

    @classmethod
    def getSqlSchema(self):
        sqlSchema = '''
CREATE TABLE Testrun(testId INTEGER PRIMARY KEY autoincrement, logFile TEXT, runTime TEXT, samples INTEGER, assertions INTEGER, samplesSuccessRate REAL, samplesSuccessRateInclAssertions REAL, assertionPassRate REAL, averageTime REAL, minTime INTEGER, maxTime INTEGER);
CREATE TABLE Aggregated(aggId INTEGER PRIMARY KEY autoincrement, testId INTEGER, label TEXT, samples INTEGER, averageTime REAL, minTime INTEGER, maxTime INTEGER, stDev REAL, error REAL, errorInclAssert REAL, throughput REAL, kbPerSec REAL, avgBytes REAL, median REAL, line90 INTEGER, FOREIGN KEY(testId) REFERENCES Testrun(testId));
CREATE TABLE Sample(sampleId INTEGER PRIMARY KEY autoincrement, aggId INTEGER, sampleTime INTEGER, respCode INTEGER, respMsg TEXT, threadName TEXT, dataType TEXT, status TEXT, bytes INTEGER, latency INTEGER, FOREIGN KEY(aggId) REFERENCES Aggregated(aggId));
CREATE TABLE Assert(assertId INTEGER PRIMARY KEY autoincrement, sampleId INTEGER, name TEXT, failure TEXT, failureMsg TEXT, error TEXT, FOREIGN KEY(sampleId) REFERENCES Sample(sampleId));
        '''
        return sqlSchema

    def insertTestrun(self):
        sqlCommand = ""
        testRunId = -1
        if self.dbStatus:
            sqlCommand += "INSERT INTO Testrun (logFile ,runTime, samples, assertions, "
            sqlCommand += "samplesSuccessRate, samplesSuccessRateInclAssertions,"
            sqlCommand += " assertionPassRate, averageTime, minTime, maxTime) VALUES (\'"
            sqlCommand += self.loganalyser.jtlPath + "\',\'"
            sqlCommand += self.loganalyser.timeStamp + "\',"
            sqlCommand += str(self.loganalyser.aggrSummary.getAmountOfSamples()) + ","
            sqlCommand += str(self.loganalyser.aggrSummary.getAmountOfAssertions()) + ","
            sqlCommand += str(self.loganalyser.aggrSummary.getSamplesSuccessRateNoAssert()) + ","
            sqlCommand += str(self.loganalyser.aggrSummary.getSamplesSuccessRateInclAssert()) + ","
            sqlCommand += str(self.loganalyser.aggrSummary.getAssertionPassRate()) + ","
            sqlCommand += str(self.loganalyser.aggrSummary.getAverageTime()) + ","
            sqlCommand += str(self.loganalyser.aggrSummary.getMinTime()) + ","
            sqlCommand += str(self.loganalyser.aggrSummary.getMaxTime()) + ");"
            if sqlCommand!="":
                try:
                    dbCursor = self.db.cursor()
                    dbCursor.executescript(sqlCommand)
                except sqlite3.Error:
                    print("ERROR while executing \"INSERT INTO Testrun\" command")
                    self.dbStatus = False
            sqlSelect = "SELECT testId FROM Testrun WHERE runTime=\'" + self.loganalyser.timeStamp
            #sqlSelect += "\' AND logFile=\'" + self.loganalyser.filePath + "\';"
            sqlSelect += "\' AND logFile=\'" + self.loganalyser.jtlPath + "\';"
            testRunId = self.getIdFromSelect(sqlSelect,"ERROR while executing \"SELECT ... FROM Testrun\" command")
        return testRunId

    def getIdFromSelect(self, command, errMsg):
        foundId = -1
        if command!="":
            try:
                dbCursor = self.db.cursor()
                dbCursor.execute(command)
                selectTuple = dbCursor.fetchone()
                if type(selectTuple)==tuple and len(selectTuple)>=1:
                    foundId = selectTuple[0]
            except sqlite3.Error:
                print(errMsg)
                self.dbStatus = False
        return foundId

    def insertAggregations(self, testrunKey):
        idNameDict = {}
        if type(testrunKey)==int and testrunKey>0 and self.dbStatus:
            for agg in self.loganalyser.aggrSamples:
                sqlCommand = ""
                sqlCommand += "INSERT INTO Aggregated (testId, label,"
                sqlCommand += "samples, averageTime, minTime, maxTime,stDev, error, errorInclAssert, "
                sqlCommand += "throughput, kbPerSec, avgBytes, median, line90)"
                sqlCommand += " VALUES (" + str(testrunKey) + ",\'" + agg.sampleName + "\',"
                sqlCommand += str(agg.getAmountOfSamples()) + ","
                sqlCommand += str(agg.getAverageTime()) + ","
                sqlCommand += str(agg.getMinTime()) + ","
                sqlCommand += str(agg.getMaxTime()) + ","
                sqlCommand += str(agg.getStdDev()) + ","
                sqlCommand += str(agg.getSampleErrorNoAssert()) + ","
                sqlCommand += str(agg.getSampleErrorInclAssert()) + ","
                sqlCommand += str(agg.getThroughput()) + ","
                sqlCommand += str(agg.getKBytesPerSec()) + ","
                sqlCommand += str(agg.getAverageBytes()) + ","
                sqlCommand += str(agg.getMedian()) + ","
                sqlCommand += str(agg.getPerc90()) + ");"
                if sqlCommand!="" and agg.sampleName!="TOTAL":
                    try:
                        dbCursor = self.db.cursor()
                        dbCursor.executescript(sqlCommand)
                    except sqlite3.Error:
                        print("ERROR while executing \"INSERT INTO Aggregated\" command")
                        self.dbStatus = False
                    sqlSelect = "SELECT aggId FROM Aggregated WHERE testId=" + str(testrunKey)
                    sqlSelect += " AND label=\'" + agg.sampleName + "\';"
                    aggrId = self.getIdFromSelect(sqlSelect,"ERROR while executing \"SELECT ... FROM Aggregated\" command")
                    if aggrId>0 and type(aggrId)==int:
                        idNameDict[agg.sampleName] = aggrId
        return idNameDict

    def insertSamples(self, idNameDict):
        if self.dbStatus:
            for s in self.loganalyser.samples:
                fk = -1
                for k in idNameDict.keys():
                    if k == s.getLabel():
                        fk = idNameDict[k]
                if fk>0 and type(fk) == int :
                    sqlCommand = "INSERT INTO Sample (aggId, sampleTime, respCode, respMsg, threadName, dataType, status, bytes, latency)"
                    sqlCommand += " VALUES (" + str(fk) + ","
                    sqlCommand += s.getSampleTime() + ","
                    sqlCommand += "\'" + s.getRespCode() + "\',"
                    sqlCommand += "\'" + s.getRespMsg() + "\',"
                    sqlCommand += "\'" + s.getThreadName() + "\',"
                    sqlCommand += "\'" + s.getDataType() + "\',"
                    sqlCommand += "\'" + s.getStatus() + "\',"
                    sqlCommand += s.getBytes() + ","
                    sqlCommand += s.getLatency() + ");"
                    if sqlCommand != "":
                        try:
                            dbCursor = self.db.cursor()
                            dbCursor.executescript(sqlCommand)
                        except sqlite3.Error:
                            print("ERROR while executing \"INSERT INTO Sample\" command")
                            self.dbStatus = False
                        sqlSelect = "SELECT sampleId FROM Sample ORDER BY sampleId DESC"
                        sampleId = self.getIdFromSelect(sqlSelect,"Error while executing \"SELECT ... FROM Sample\" command")
                    self.insertAssertion(sampleId,s.assertions)

    def insertAssertion(self, sampleKey, assertionList):
        if self.dbStatus:
            if isinstance(sampleKey,int) and sampleKey > 0:
                for a in assertionList:
                    sqlCommand = "INSERT INTO Assert (sampleId, name, failure, failureMsg, error) "
                    sqlCommand += " VALUES (" + str(sampleKey) + ","
                    sqlCommand += "\'" + a.getName() + "\',"
                    sqlCommand += "\'" + a.getFailure() + "\',"
                    sqlCommand += "\'" + a.getFailureMsg() + "\',"
                    sqlCommand += "\'" + a.getError() + "\')"
                    if sqlCommand!="":
                        try:
                            dbCursor = self.db.cursor()
                            dbCursor.executescript(sqlCommand)
                        except sqlite3.Error:
                            print("ERROR while executing \"INSERT INTO Assert\" command")
                            self.dbStatus = False

    def testDb(self):
        filePath = self.dbName + ".txt"
        if self.readDbInTheEnd:
            sqlLog = ""
            sqlLog += self.selectFrom("Testrun")
            sqlLog += self.selectFrom("Aggregated")
            sqlLog += self.selectFrom("Sample")
            sqlLog += self.selectFrom("Assert")
            if filePath!=None:
                try:
                    dbLogFile = open(filePath, 'w')
                    dbLogFile.write(sqlLog)
                    dbLogFile.close()
                except IOError:
                    print("ERROR while saving data to a log file")

    def selectFrom(self, fromWhat):
        sqlCommand = "SELECT * FROM " + fromWhat + ";\n"
        sqlData = sqlCommand + "\n"
        try:
            dbCursor = self.db.cursor()
            dbCursor.execute(sqlCommand)
            for r in dbCursor:
                for t in r:
                    sqlData += str(t) + " "
                sqlData += "\n"
            sqlData += "\n"
        except sqlite3.Error:
            print("ERROR while executing command " + sqlCommand)
        return sqlData

class LogConverterHtml(object):
    def __init__(self, parentHandler, disableReports=None):
        self.loganalyser = parentHandler
        self.logPath = parentHandler.jtlPath
        self.predefineHtml()
        self.customizeNaviBar(disableReports)
        self.printDetails = False

    def createNewHtmlPath(self):
        self.htmlLogPath = self.logPath + ".html"
        while os.path.isfile(self.htmlLogPath):
            self.htmlLogPath = self.logPath + strftime("%Y%m%d%H%M%S", gmtime()) + ".html"
        self.saveDataToHtml(" ")

    def saveDataToHtml(self,data):
        try:
            htmlHndl = open(self.htmlLogPath, "w")
            htmlHndl.write(data)
            htmlHndl.close()
        except IOError:
            print("ERROR, problems while writing " + str(self.htmlLogPath))

    def createHtml(self, disableReports):
        tableOfSamples = self.loganalyser.samples
        if isinstance(disableReports, str):
            disableReports = int(disableReports)
        if not isinstance(disableReports, int):
            disableReports = 0
        print("Creating html " + self.htmlLogPath)
        newHtml = self.createHtmlBeginning()
        newHtml += self.createHtmlNaviPanel()
        newHtml += self.createHtmlInfo()
        newHtml += self.createHtmlSummaryReport()
        if disableReports & 0b00000001 == 0:
            newHtml += self.createHtmlAggrRepAndGraph()
        if disableReports & 0b00000010 == 0:
            newHtml += self.createHtmlAggrSamples()
        if disableReports & 0b00000100 == 0:
            newHtml += self.createHtmlRespTimeGraph()
        if disableReports & 0b00001000 == 0:
            newHtml += self.createHtmlAllSamples()
        newHtml += self.createHtmlEnd()
        self.saveDataToHtml(newHtml)

    def howManyAssertions(self, samples):
        assertNum = 0
        for s in samples:
            assertNum = assertNum + len(s.assertions)
        return assertNum

    def createHtmlBeginning(self):
        return self.htmlParts['start']

    def createHtmlNaviPanel(self):
        return self.htmlParts['navi']

    def createHtmlInfo(self):
        htmlInfo = self.htmlParts['belowmenudiv']
        htmlInfo += "<p>File <i>" + self.logPath + "</i> parsed and converted by "
        htmlInfo += "<a href=http://robotframework.org target=_blank>Robot Framework</a> "
        htmlInfo += "<a href=https://github.com/kowalpy/Robot-Framework-JMeter-Library target=_blank>JMeter library </a> on "
        htmlInfo += self.loganalyser.timeStamp + ".</p>"
        htmlInfo += self.htmlParts['infoTableStartAndHeader']
        htmlInfo += "<tr><td>" + str(self.loganalyser.aggrSummary.getAmountOfSamples()) + "</td>"
        htmlInfo += "<td>" + str(self.loganalyser.aggrSummary.getAmountOfAssertions()) + "</td>"
        htmlInfo += "<td>" + str(self.loganalyser.aggrSummary.getSamplesSuccessRateNoAssert()) + " %</td>"
        htmlInfo += "<td>" + str(self.loganalyser.aggrSummary.getSamplesSuccessRateInclAssert()) + " %</td>"
        htmlInfo += "<td>" + str(self.loganalyser.aggrSummary.getAssertionPassRate()) + " %</td>"
        htmlInfo += "<td>" + str(self.loganalyser.aggrSummary.getAverageTime()) + " ms</td>"
        htmlInfo += "<td>" + str(self.loganalyser.aggrSummary.getMinTime()) + " ms</td>"
        htmlInfo += "<td>" + str(self.loganalyser.aggrSummary.getMaxTime()) + " ms</td>"
        htmlInfo += "</table>"
        htmlInfo += self.createTbdList()
        return htmlInfo

    def createHtmlSummaryReport(self):
        sumHtml = "<a id=\"sumrep\"><p id=\"navifont\">Summary report </p></a><br>"
        sumHtml += self.htmlParts['SummaryReportTableStartAndHeader']
        for agg in self.loganalyser.aggrSamples:
            sumHtml += "<td><a href=\"#" + agg.link + "\">" + agg.sampleName + "</a></td><td>"
            sumHtml += str(agg.getAmountOfSamples()) + "</td><td>" + str(agg.getAverageTime()) + " ms</td>"
            sumHtml += "<td>" + str(agg.getMinTime()) + " ms</td>"
            sumHtml += "<td>" + str(agg.getMaxTime()) + " ms</td>"
            sumHtml += "<td>" + str(agg.getStdDev()) + "</td>"
            sumHtml += "<td>" + str(agg.getSampleErrorNoAssert()) + " %</td>"
            sumHtml += "<td>" + str(agg.getSampleErrorInclAssert()) + " %</td>"
            sumHtml += "<td>" + str(agg.getThroughput()) + "/sec</td>"
            sumHtml += "<td>" + str(agg.getKBytesPerSec()) + "KB/sec</td>"
            sumHtml += "<td>" + str(agg.getAverageBytes()) + "</td>"
            sumHtml += "</tr>"
        sumHtml += "</table>"
        return sumHtml

    def createHtmlAggrRepAndGraph(self):
        aggHtml = "<a id=\"aggrrep\"><p id=\"navifont\">Aggregated report and graph </p></a>"
        aggHtml += self.htmlParts['AggrReportTableStartAndHeader']
        for agg in self.loganalyser.aggrSamples:
            aggHtml += "<td><a href=\"#" + agg.link + "\">" + agg.sampleName + "</a></td><td>"
            aggHtml += str(agg.getAmountOfSamples()) + "</td><td>" + str(agg.getAverageTime()) + " ms</td>"
            aggHtml += "<td>" + str(agg.getMedian()) + " ms</td>"
            aggHtml += "<td>" + str(agg.getPerc90()) + " ms</td>"
            aggHtml += "<td>" + str(agg.getMinTime()) + " ms</td>"
            aggHtml += "<td>" + str(agg.getMaxTime()) + " ms</td>"
            aggHtml += "<td>" + str(agg.getSampleErrorNoAssert()) + " %</td>"
            aggHtml += "<td>" + str(agg.getSampleErrorInclAssert()) + " %</td>"
            aggHtml += "<td>" + str(agg.getThroughput()) + "/sec</td>"
            aggHtml += "<td>" + str(agg.getKBytesPerSec()) + "KB/sec </td>"
            aggHtml += "</tr>"
        aggHtml += "</table><br>"
        aggCounter = 0
        for agg in self.loganalyser.aggrSamples:
            if agg.getAmountOfSamples() > 1:
                aggCounter += 1
                canvasId = "aggrRep" + str(aggCounter)
                aggHtml += "\n<br><br><canvas id=\"" + canvasId + "\" width=\"800\" height=\"600\">"
                aggHtml += "Your browser does not support the HTML5 canvas tag."
                aggHtml += "</canvas><br>\n"
                aggHtml += self.addAggrRepJs(canvasId,aggCounter,agg.sampleName,[agg.getAverageTime(),agg.getMedian(),
                                                                                 agg.getPerc90(),agg.getMinTime(),
                                                                                 agg.getMaxTime()])
        return aggHtml

    def addAggrRepJs(self, canvId, num, label, dt):
        barVar = "bc" + str(num)
        aggRespJs = "\n<script>\n"
        aggRespJs += "var " + barVar + " = new BarChart(\"" + canvId + "\");\n"
        aggRespJs += barVar + ".setLabel(\"" + label + "\");\n"
        if len(dt) > 4:
             aggRespJs += barVar + ".addData("
             dCounter = 0
             for d in dt:
                 if dCounter>0:
                     aggRespJs += ","
                 aggRespJs += str(d)
                 dCounter += 1
             aggRespJs += ");\n"
        aggRespJs += barVar + ".createChart();\n"
        aggRespJs += "</script>\n"
        return aggRespJs

    def createHtmlAggrSamples(self):
        aggHtml = "<a id=\"aggrsam\"><p id=\"navifont\">Aggregated samples </p></a>"
        for agg in self.loganalyser.aggrSamples:
            if agg.link != "samples_" and agg.sampleName != "TOTAL":
                aggHtml += "<a id=\"" + agg.link + "\"><p id=\"navifont\">"+ self.htmlParts['nbspx10'] + agg.sampleName + " </p></a><br>"
                oneTypeTable = []
                for o in self.loganalyser.samples:
                    if agg.sampleName==o.getLabel():
                        oneTypeTable.append(o)
                aggHtml += self.samplesToHtml(oneTypeTable) + "</table>"
        return aggHtml

    def createHtmlRespTimeGraph(self):
        respHtml = "<a id=\"respgr\"><p id=\"navifont\">Response time graph </p></a>"
        respHtml += "<p id=\"justsmallfont\"> Charts are generated only after clicking buttons because drawing might be time consuming!</p>"
        aggCounter = 0
        for agg in self.loganalyser.aggrSamples:
            if agg.getAmountOfSamples() > 1:
                aggCounter += 1
                canvasId = "respTime" + str(aggCounter)
                respHtml +=" <button onclick=\"lc" + str(aggCounter) + ".drawChartData()\">DRAW CHART for " + agg.sampleName + "</button><br><br>"
                respHtml += "<canvas id=\"" + canvasId + "\" width=\"800\" height=\"600\" >"
                respHtml += "Your browser does not support the HTML5 canvas tag. </canvas><br><br><br>"
                respHtml += self.addRespTimeJs(canvasId,"#00A3CC",agg.sampleName,aggCounter,agg.timeTable)
        return respHtml

    def addRespTimeJs(self, canvId, color, label, counter, data):
        jsVar = "lc" + str(counter)
        respJs = "\n<script>\nvar " +  jsVar + "= new LineChart(\"" + canvId + "\");\n"
        respJs += jsVar + ".setLabel(\""+ label +"\");\n" + jsVar + ".setColor(\"" + color + "\");\n"
        for d in data:
            respJs += jsVar + ".addData(" + str(d) + ");\n"
        respJs += jsVar + ".createChart();\n</script>\n"
        return respJs

    def createHtmlAllSamples(self):
        return "<br><a id=\"samples_\"><p id=\"navifont\">All samples </p></a>" + self.samplesToHtml(self.loganalyser.samples)

    def createTbdList(self):
        tbdHtml = ""
        tbdHtml = tbdHtml + "</p>"
        return tbdHtml

    def samplesToHtml(self, tableOfSamples):
        samplesHtml = self.htmlParts['sampleTableStart'] + self.htmlParts['sampleTableHeader']
        sampleNumber = 0
        whichRow = 0
        for s in tableOfSamples:
            sampleNumber += 1
            if self.printDetails:
                print("     Writing sample number " + str(sampleNumber) + " into " + self.htmlLogPath)
            samplesHtml += "<tr"
            if whichRow == 1:
                samplesHtml += " class=\"even\" "
            samplesHtml += "><td>"
            newTime = datetime.datetime.fromtimestamp(int(s.getStartTime()) / 1e3)
            samplesHtml += str(newTime) + "</td><td>"
            samplesHtml += s.getSampleTime() + "</td><td>"
            samplesHtml += s.getLabel() + "</td><td>"
            samplesHtml += s.getRespCode() + "</td><td>"
            samplesHtml += s.getRespMsg() + "</td><td>"
            samplesHtml += s.getThreadName() + "</td><td>"
            samplesHtml += s.getDataType() + "</td><td>"
            samplesHtml += s.getStatus() + "</td><td>"
            samplesHtml += s.getBytes() + "</td><td>"
            samplesHtml += s.getLatency() + "</td></tr>\n"
            sampleAssertList = s.getAssertions()
            if len(sampleAssertList) > 0:
                samplesHtml += "<tr"
                if whichRow == 1:
                   samplesHtml += " class=\"even\" "
                samplesHtml += "><td></td><td>Assertions:</td><td colspan=8>"
                saCounter = 0
                for sa in sampleAssertList:
                    if saCounter==0:
                        samplesHtml += self.htmlParts['assertTableStart']
                        samplesHtml += self.htmlParts['assertTableHeader']
                    samplesHtml += "<tr"
                    samplesHtml += "><td>"
                    samplesHtml += sa.getName() + "</td><td>"
                    samplesHtml += sa.getFailure() + "</td><td>"
                    samplesHtml += sa.getFailureMsg() + "</td><td>"
                    samplesHtml += sa.getError() + "</td></tr>\n"
                    saCounter += 1
                samplesHtml += "</td></table>"
            if whichRow == 1:
                whichRow = 0
            elif whichRow == 0:
                whichRow = 1
        return samplesHtml

    def createHtmlEnd(self):
        return self.htmlParts['end']

    def readCss(self):
        cssContents = '''
#samples
{
    font-family:Arial;
    width:100%;
    border-collapse:collapse;
}
#samples td, #samples th
{
    font-size:1em;
    border:1px solid #00A3CC;
    padding:3px 7px 2px 7px;
}
#samples th
{
	font-size:1.1em;
	text-align:left;
	padding-top:5px;
	padding-bottom:4px;
	background-color:#00A3CC;
	color:#ffffff;
}
#samples tr.even td
{
	color:#000000;
	background-color:#D1EEF6;
}
#assertions
{
	font-family:Arial;
	width:100%;
	border-collapse:collapse;
}
#assertions td, #assertions th
{
	font-size:0.8em;
	border:1px solid #AADAEB;
	padding:3px 7px 2px 7px;
}
#assertions th
{
	font-size:0.9em;
	tempHtml = tempHtml + "text-align:left;
	padding-top:5px;
	padding-bottom:4px;
	background-color:#AADAEB;
	color:#ffffff;
}
#assertions tr.even td
{
	color:#000000;
	background-color:#E7F4FA;
}
#menu
{
	position:fixed;
	top:0px;
	width:100%;
	height:50px;
}
#belowmenu
{
	margin-top:28px;
}
#summary
{
	font-family:Arial;
	font-size:1em;
	width:100%;
	border-collapse:collapse;
}
#navifont
{
	font-family:Arial;
	font-size:1.1em;
	font-weight:bold;
}
#justsmallfont
{
	font-family:Arial;
	font-size:0.9em;
}
        '''
        return cssContents

    def readJs(self):
        jsContents = '''
<script>
function BarChart (canvasID) {
    this.debug = false;
    this.label = "";
	this.defineColors();
    this.canvas=document.getElementById(canvasID);
    this.context=this.canvas.getContext("2d");
	this.chartData=new Array();
	this.startX = 55;
	this.startY = 560;
	this.maxX = 795;
	this.maxY = 25
}

BarChart.prototype.addData = function(av,me,ni,mi,ma)
{
    this.chartData[0] = av
	this.chartData[1] = me
	this.chartData[2] = ni
	this.chartData[3] = mi
	this.chartData[4] = ma
}

BarChart.prototype.calculateWidth = function() {
    this.barWidth = (this.maxX - this.startX)/7
}

BarChart.prototype.calculateHeightStep = function() {
    if(this.chartData[4]>0){
        this.heightStep = (this.startY-this.maxY)/(1.1*this.chartData[4])
	}
}

BarChart.prototype.defineColors = function() {
    this.bgColor = "#000000";
	this.bgColor2 = "#B8B8B8";
	this.bgLight = "#FFFFFF";
    this.colorAverage = "#AF3E19";
	this.colorMedian = "#0033CC";
	this.color90 = "#006600";
	this.colorMin = "#AAAAAA";
	this.colorMax = "#474747";
}

BarChart.prototype.setLabel = function(l) {
    this.label = l;
}

BarChart.prototype.drawChartArea = function() {
    this.context.beginPath();
    this.context.lineWidth=2;
    this.context.moveTo(this.startX,this.startY)
    this.context.lineTo(this.maxX,this.startY)
	this.context.lineTo(this.maxX,this.maxY)
	this.context.lineTo(this.startX,this.maxY)
	this.context.moveTo(this.startX,this.startY)
	this.context.lineTo(this.startX,this.maxY)
    this.context.strokeStyle=this.bgColor;
    this.context.stroke();
	this.context.fillStyle=this.bgColor;
	this.context.font="20px Arial";
	this.context.fillText("Response time graph - " + this.label,(this.maxX - this.startX - 550)/2,this.maxY-10);
	this.drawLabels();
	this.context.save();
	this.context.translate(0, -200);
	this.context.rotate(90*Math.PI/180);
	this.context.fillStyle=this.bgColor;
	this.context.font="15px Arial";
	this.context.fillText("miliseconds",450,0);
	this.context.restore();
	lineStep = (this.startY - this.maxY)/15
	for (var i=0;i<15;i++){
	    this.drawSingleHorizontalLine(this.startY - i*lineStep)
	}
}

BarChart.prototype.drawLabels = function() {
	this.context.fillStyle=this.bgColor;
	this.context.font="15px Arial";
	this.context.fillText("Average",this.startX + 1*this.barWidth + 15,this.startY+35);
	this.context.fillText("Median",this.startX + 2*this.barWidth + 15,this.startY+35);
	this.context.fillText("90% Line",this.startX + 3*this.barWidth + 15,this.startY+35);
	this.context.fillText("Min",this.startX + 4*this.barWidth + 15,this.startY+35);
	this.context.fillText("Max",this.startX + 5*this.barWidth + 15,this.startY+35);
	this.context.fillStyle=this.colorAverage;
	this.context.fillRect(this.startX + 1*this.barWidth,this.startY+25,10,10);
	this.context.fillStyle=this.colorMedian;
    this.context.fillRect(this.startX + 2*this.barWidth,this.startY+25,10,10);
	this.context.fillStyle=this.color90;
    this.context.fillRect(this.startX + 3*this.barWidth,this.startY+25,10,10);
	this.context.fillStyle=this.colorMin;
    this.context.fillRect(this.startX + 4*this.barWidth,this.startY+25,10,10);
	this.context.fillStyle=this.colorMax;
	this.context.fillRect(this.startX + 5*this.barWidth,this.startY+25,10,10);
}

BarChart.prototype.drawSingleRect = function(color,text,startingX,startingY,width,height) {
	this.context.fillStyle=color;
    this.context.fillRect(startingX,startingY,width,-height);
	this.context.font="15px Arial";
	if((height)>15){
	    this.context.fillStyle=this.bgLight;
	    this.context.fillText(text,startingX + (width-25)/2,startingY - height +12);
	}
	else{
	    this.context.fillStyle=this.bgColor
	    this.context.fillText(text,startingX + (width-25)/2,startingY - height - 2);
	}
}

BarChart.prototype.addYScale = function() {
	this.context.fillStyle=this.bgColor;
	this.context.font="15px Arial";
	this.context.fillText("0",(this.startX)-40,this.startY);
	this.context.fillText(this.chartData[4],(this.startX)-40,this.startY-(this.heightStep*this.chartData[4]));
}

BarChart.prototype.drawSingleHorizontalLine = function(yStart) {
	this.context.beginPath()
    this.context.lineWidth=1;
	this.context.moveTo(this.startX,yStart)
    this.context.lineTo(this.maxX,yStart)
    this.context.strokeStyle=this.bgColor2;
    this.context.stroke();
}

BarChart.prototype.drawChartData = function() {
    this.drawSingleRect(this.colorAverage,this.chartData[0],this.startX + this.barWidth,this.startY,this.barWidth,this.heightStep*this.chartData[0]);
	this.drawSingleRect(this.colorMedian,this.chartData[1],this.startX + 2*this.barWidth,this.startY,this.barWidth,this.heightStep*this.chartData[1]);
	this.drawSingleRect(this.color90,this.chartData[2],this.startX + 3*this.barWidth,this.startY,this.barWidth,this.heightStep*this.chartData[2]);
	this.drawSingleRect(this.colorMin,this.chartData[3],this.startX + 4*this.barWidth,this.startY,this.barWidth,this.heightStep*this.chartData[3]);
	this.drawSingleRect(this.colorMax,this.chartData[4],this.startX + 5*this.barWidth,this.startY,this.barWidth,this.heightStep*this.chartData[4]);
}

BarChart.prototype.createChart = function() {
    this.calculateWidth();
	this.calculateHeightStep();
    this.addYScale();
    this.drawChartArea();
	this.drawChartData();
}

function LineChart (canvasID) {
    this.debug = false;
    this.label = "";
	this.bgColor = "#000000";
	this.bgColor2 = "#B8B8B8";
    this.canvas=document.getElementById(canvasID);
    this.context=this.canvas.getContext("2d");
	this.chartData=new Array();
	this.startX = 55;
	this.startY = 560;
	this.maxX = 795;
	this.maxY = 25;
}

LineChart.prototype.addData = function(d)
{
    arrayIndex = this.chartData.length;
	this.chartData[arrayIndex] = d;
}

LineChart.prototype.setColor = function(c) {
    this.color = c;
}

LineChart.prototype.setLabel = function(l) {
    this.label = l;
}

LineChart.prototype.calculateStep = function() {
    this.minData = this.chartData[0];
	this.maxData = 0;
	this.dataLen = 0;
	for (var i=0;i<this.chartData.length;i++)
    {
		this.dataLen = i;
		if(this.minData>this.chartData[i])
		{
		    this.minData = this.chartData[i];
		}
		if(this.maxData<this.chartData[i])
		{
		    this.maxData = this.chartData[i];
		}
    }
	this.stepX = (this.maxX - this.startX - 2)/this.dataLen;
	this.stepY = (this.startY - this.maxY - 2)/(this.maxData - this.minData + 2);
	if(this.debug==true)
	{
	    document.write("<br>minData = " + this.minData + "<br>");
	    document.write("maxData = " + this.maxData + "<br>");
	    document.write("dataLen = " + this.dataLen + "<br>");
	    document.write("stepX = " + this.stepX + "<br>");
		document.write("stepY = " + this.stepY + "<br>");
	}
}

LineChart.prototype.drawChartArea = function() {
    this.context.beginPath();
    this.context.lineWidth=2;
    this.context.moveTo(this.startX,this.startY);
    this.context.lineTo(this.maxX,this.startY);
	this.context.lineTo(this.maxX,this.maxY);
	this.context.lineTo(this.startX,this.maxY);
	this.context.moveTo(this.startX,this.startY);
	this.context.lineTo(this.startX,this.maxY);
    this.context.strokeStyle=this.bgColor;
    this.context.stroke();
	this.context.fillStyle=this.bgColor;
	this.context.font="20px Arial";
	this.context.fillText("Response time graph",(this.maxX - this.startX - 85)/2,this.maxY-10);
	this.drawLabels();
	this.context.save();
	this.context.translate(0, -200);
	this.context.rotate(90*Math.PI/180);
	this.context.fillStyle=this.bgColor;
	this.context.font="15px Arial";
	this.context.fillText("miliseconds",450,0);
	this.context.restore();
}

LineChart.prototype.drawLabels = function() {
	this.context.fillStyle=this.bgColor;
	this.context.font="15px Arial";
	this.context.fillText(this.label,(this.maxX - this.startX - 65)/2,this.startY+35);
	this.context.fillStyle=this.color;
    this.context.fillRect((this.maxX - this.startX - 90)/2,this.startY+25,10,10);
}

LineChart.prototype.testChartData = function() {
    if(this.debug==true)
	{
        document.write("<br><br>");
        for (var i=0;i<this.chartData.length;i++)
        {
            document.write(this.chartData[i] + "<br>");
        }
	}
}

LineChart.prototype.addYScale = function() {
	this.context.fillStyle=this.bgColor;
	this.context.font="15px Arial";
	this.context.fillText(this.minData-1,(this.startX)-40,this.startY);
    this.context.fillText(this.maxData+1,(this.startX)-40,this.maxY+10);
	if((this.maxData - this.minData)<20){
        this.drawMiddleHelpLine();
	}
	else if((this.maxData - this.minData)<50){
	    this.drawMiddleHelpLine();
        this.drawQuarterHelpLines();
    }
	else{
	    this.drawMiddleHelpLine();
        this.drawQuarterHelpLines();
		this.drawOneEightsHelpLines();
	}
}

LineChart.prototype.drawMiddleHelpLine = function() {
	this.drawSingleHorizontalLine(0.5);
}

LineChart.prototype.drawQuarterHelpLines = function() {
    this.drawSingleHorizontalLine(0.75);
	this.drawSingleHorizontalLine(0.25);
}

LineChart.prototype.drawOneEightsHelpLines = function() {
    this.drawSingleHorizontalLine(0.875);
	this.drawSingleHorizontalLine(0.625);
	this.drawSingleHorizontalLine(0.375);
	this.drawSingleHorizontalLine(0.125);
}

LineChart.prototype.drawSingleHorizontalLine = function(factor) {
	data = this.minData+((this.maxData - this.minData)*factor);
	loc = this.startY-this.stepY-((data-this.minData)*this.stepY);
	this.context.beginPath();
    this.context.lineWidth=1;
	this.context.moveTo(this.startX,loc);
    this.context.lineTo(this.maxX,loc);
    this.context.strokeStyle=this.bgColor2;
    this.context.stroke();
	data = Math.round(data);
	this.context.fillText(data,(this.startX)-40,loc);
}

LineChart.prototype.drawChartData = function() {
   	this.context.beginPath();
    this.context.lineWidth=1;
	this.context.strokeStyle=this.color;
    for (var i=0;i<this.chartData.length;i++)
    {
		this.context.lineTo(this.startX+(i*this.stepX),this.startY-this.stepY-((this.chartData[i]-this.minData)*this.stepY));
	    this.context.stroke();
    }
}

LineChart.prototype.createChart = function() {
    this.calculateStep();
    this.testChartData();
    this.addYScale();
    this.drawChartArea();
}
</script>
        '''
        return jsContents

    def predefineHtml(self):
        self.htmlParts = {'start':'''
<!DOCTYPE html>
<!--
Log file parsed and converted by Robot Framework JMeter lib released under LGPL license.
Website: http://sourceforge.net/projects/rf-jmeter-py/
-->
<html>\n<head>\n<title>jmeterTestDifferentSamplers_xml.jtl.html</title>
<style>\n''' + self.readCss() + "\n</style>\n</head>\n<body>\n" + self.readJs(),
                          'navi':'''
<div id="menu"><table id="samples"><tr class="even">
<td><a href="#info">Info</a></td>
<td><a href="#sumrep">Summary report</a></td>
<td><a href="#aggrrep">Aggregated report and graph</a></td>
<td><a href="#aggrsam">Aggregated samples</a></td>
<td><a href="#respgr">Response time graph</a></td>
<td><a href="#samples_">All samples</a></td></tr></table></div>'''
                             ,
                          'belowmenudiv':'''
<div id="belowmenu"><a id="info"> </a><br><table id="samples">
<tr><td><p id="navifont">Info</p>'''
                             ,
                          'infoTableStartAndHeader':'''
<table id="samples">
<tr><th>Samples</th><th>Assertions</th><th>Samples success rate</th>
<th>Samples success rate<br>(inlcuding assertions)</th><th>Assertions pass rate</th>
<th>Average time [ms]</th><th>Min time</th><th>Max time</th></tr>'''
                             ,
                          'SummaryReportTableStartAndHeader':'''
<table id="samples">
<tr><th>Label</th><th>#Samples</th><th>Average</th><th>Min</th><th>Max</th>
<th>Std. Dev.</th><th>Error %</th><th>Error % incl. assert.</th><th>Throughput</th>
<th>KB/sec</th><th>Avg. Bytes</th></tr>'''
                             ,
                          'AggrReportTableStartAndHeader':'''
<table id="samples">
<tr><th>Label</th><th>#Samples</th><th>Average</th><th>Median</th><th>90% Line</th>
<th>Min</th><th>Max</th><th>Error %</th><th>Error % incl. assert.</th><th>Throughput</th>
<th>KB/sec</th></tr>'''
                             ,
                          'sampleTableStart':'<table id="samples">\n',
                          'sampleTableHeader':'''
<tr><th>Start time</th><th>Sample time (ms)</th><th>Label</th>
<th>Response code</th><th>Response message</th>
<th>Thread name</th><th>Data type</th>
<th>Status</th><th>Bytes</th><th>Latency</th></tr>'''
                              ,
                          'assertTableStart':'<table id=\"assertions\">\n',
                          'assertTableHeader':'''
<tr><th>Name</th><th>Failure</th>
<th>Failure msg</th><th>Error</th></tr>'''
                              ,
                          'end':'</body></html>',
                          'nbspx10':'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        }

    def customizeNaviBar(self, reportOptions):
        if isinstance(reportOptions, str):
            reportOptions = int(reportOptions)
        if not isinstance(reportOptions, int):
            reportOptions = 0
        self.htmlParts['navi'] = '''
<div id="menu"><table id="samples"><tr class="even">
<td><a href="#info">Info</a></td>
<td><a href="#sumrep">Summary report</a></td>
<td>
        '''
        if reportOptions & 0b00000001 == 0:
            self.htmlParts['navi'] += "<a href=\"#aggrrep\">Aggregated report and graph</a>"
        else:
            for i in range(27):
                self.htmlParts['navi'] += "&nbsp;"
        self.htmlParts['navi'] += '''
</td>
<td>
        '''
        if reportOptions & 0b00000010 == 0:
            self.htmlParts['navi'] += "<a href=\"#aggrsam\">Aggregated samples</a>"
        else:
            for i in range(18):
                self.htmlParts['navi'] += "&nbsp;"
        self.htmlParts['navi'] += '''
</td>
<td>
        '''
        if reportOptions & 0b00000100 == 0:
            self.htmlParts['navi'] += "<a href=\"#respgr\">Response time graph</a>"
        else:
            for i in range(19):
                self.htmlParts['navi'] += "&nbsp;"
        self.htmlParts['navi'] += '''
</td>
<td>
        '''
        if reportOptions & 0b00001000 == 0:
            self.htmlParts['navi'] += "<a href=\"#samples_\">All samples</a>"
        else:
            for i in range(11):
                self.htmlParts['navi'] += "&nbsp;"
        self.htmlParts['navi'] += '''
</td>
<td></tr></table></div>
        '''
