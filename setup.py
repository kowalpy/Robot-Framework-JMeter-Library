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

"""
To install Robot Framework JMeter Library execute command:
    python setup.py install
"""
from distutils.core import setup

setup(name='robotframework-jmeterlibrary',
      version='1.2',
      description='Robot Framework JMeter Library',
      author='Marcin Kowalczyk',
      author_email='mkov80@gmail.com',
      license='LGPLv3',
      url='https://github.com/kowalpy/Robot-Framework-JMeter-Library',
      py_modules=['JMeterLib', 'JMeterClasses'],
      data_files=[('Scripts', ['jmeterLibExample.txt']),
                  ('Doc', ['JMeterLib.html'])]
      )