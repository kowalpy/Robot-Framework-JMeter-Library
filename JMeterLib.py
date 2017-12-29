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

#to generate libdoc documentation run:
#   python -m robot.libdoc JMeterLib JMeterLib.html

import JMeterClasses

class JMeterLib(JMeterClasses.JMeterKeywords):
    """
This library provides simple way to integrate Robot Framework and JMeter. JTL output
files can be analysed and converted to HTML, Python dictionary or SQLite format.

Version 1.2 released on 29th of December 2017.

What's new:

- adapted to new csv log format

Following software versions were used during development:
- Python-2.7.14
- robotframework-3.0.2
- robotframework-ride-1.5.2.1
- jmeter 2.12
- jmeter 3.3


Author: Marcin Kowalczyk

Website: http://sourceforge.net/projects/rf-jmeter-py/

Installation:
- run command: pip install robotframework-jmeterlibrary

OR
- download, unzip and run command: python setup.py install

Example for running JMeter and parsing results in single keyword:
 | run jmeter analyse jtl convert | D:/apache-jmeter-2.12/bin/jmeter.bat | D:/Tests/Test1Thread1Loop.jmx | D:/Tests/output1.jtl |

Example for running JMeter and parsing results in separate keyword:
| ${logPath}= | set variable | D:/Tests/output1.jtl |  |
| run jmeter | D:/apache-jmeter-2.12/bin/jmeter.bat | D:/Tests/Test1Thread1Loop.jmx | ${logPath} |
| analyse jtl convert | ${logPath} |  |  |

Example for reading parsed contents:
| ${result} | analyse jtl convert | ${logPath} |  |
| log | ${result} |  |  |
| : FOR | ${ELEMENT} | IN |	@{result} |
|  | log dictionary	| ${ELEMENT} |  |
"""

    def __init__(self):
        pass

if __name__ == '__main__':
    mainMsg = "robotframework-jmeterlib is a Robot Framework library " \
              "for starting JMeter and parsing JMeter logs. For " \
              "instruction on how to use please visit" \
              " https://github.com/kowalpy/Robot-Framework-JMeter-Library"
    print(mainMsg)
