# Robot Framework JMeter Library

This library provides simple way to integrate Robot Framework and JMeter. JTL output
files can be analysed and converted to HTML, Python dictionary or SQLite format.

On 19th of March 2017, project has been moved at Github. 

## License
LGPL 3.0

## Keyword documentation
[JMeterLib.html](https://kowalpy.github.io/Robot-Framework-JMeter-Library/JMeterLib.html)

## Version history
Version 1.1 released on 25st of September 2015. What's new in 1.1:
```
    Implementation of change request http://sourceforge.net/p/rf-jmeter-py/tickets/2/:
    " As a End User I want to have option to create smaller reports"
```
Following software versions were used during development:
- robotframework-2.8.7
- robotframework-ride-2.7.5
- JMeter 2.12
- python-2.7.5

Version 1.2 released on 29th of December 2017. What's new in 1.2:

- adapted to new csv log format

## Installation:
- run command: pip install robotframework-jmeterlibrary

OR
- download, unzip and run command: python setup.py install

## Usage:

Example for running JMeter and parsing results in single keyword:
```
    | run jmeter analyse jtl convert | D:/apache-jmeter-2.12/bin/jmeter.bat | D:/Tests/Test1Thread1Loop.jmx | D:/Tests/output1.jtl |
``` 
Example for running JMeter and parsing results in separate keyword:
```
    | ${logPath}=         | set variable                         | D:/Tests/output1.jtl          |            |
    | run jmeter          | D:/apache-jmeter-2.12/bin/jmeter.bat | D:/Tests/Test1Thread1Loop.jmx | ${logPath} |
    | analyse jtl convert | ${logPath}                           |                               |            |
```
Example for reading parsed contents:
```
    | ${result} | analyse jtl convert | ${logPath} |           |
    | log       | ${result}           |            |           |
    | : FOR     | ${ELEMENT}          | IN         | @{result} |
    |           | log dictionary      | ${ELEMENT} |           |
```