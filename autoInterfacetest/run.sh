#!/bin/bash

if [ $# -lt 1 ] ; then
	echo please int testng.xml file name
	exit
fi

xmlName=$1
mvn clean
sed -i "s#<suiteXmlFile>.*</suiteXmlFile>#<suiteXmlFile>test_suite/${xmlName}</suiteXmlFile>#"  pom.xml
mvn test



if [ ! -d "reports" ]; then
  mkdir reports
fi

if [ ! -d "logs" ]; then
  mkdir logs
fi

cd reports
if [ -f "report.html" ] ; then
        rm report.html
fi
ls -t | sed q | xargs -i cp  {}  report.html

cd ../logs/
if [ -f "log.tar.gz"  ] ; then
        rm log.tar.gz
fi
ls -t | sed q | xargs  -i tar -czvf  log.tar.gz {}
