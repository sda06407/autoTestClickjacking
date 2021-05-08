#!/usr/bin/env python3
import argparse
from selenium import webdriver
import os, sys, re



html_content = """
<html>
    <head>
        <title>Clickjack test page</title>
    </head>
    <body>
        <iframe src="target" width="500" height="500"></iframe>
    </body>
</html>
"""

def getScreenshot(driver_type, location, content, name):
    try:  
        if driver_type == 'edge':
            driver = webdriver.Edge(location)
        if driver_type == 'chrome':
            driver = webdriver.Chrome(location)
        if driver_type == 'firefox':
            driver = webdriver.Firefox(location)
        if driver_type == 'opera':
            driver = webdriver.Opera(location)
        
        driver.get("data:text/html;charset=utf-8," + content)
        fileName = os.path.abspath(resultPath) + "//" + name
        driver.get_screenshot_as_file(fileName) 
        driver.close()
    except Exception as e:
        print("something wrong, check if your driver is match your broswer")
        print(e)
        exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", choices=['edge', 'chrome', 'firefox', 'opera'],help="broswer driver type", required=True)
    parser.add_argument("-l", "--location", help="broswer driver location", required=True)
    parser.add_argument("-f", "--file", help="url file list", required=True)
    parser.add_argument("-p", "--path", help="the location where to store screenshot", required=True)
    args = parser.parse_args()

    driver_type = args.type
    driver_location = args.location
    allTargetFile = args.file
    resultPath = args.path

    if not os.path.isdir(os.path.abspath(resultPath)):
        os.mkdir(os.path.abspath(resultPath))

    # parse url list file
    targetList = open(allTargetFile, "r")
    for oneSite in targetList.readlines():
        raw_HTML = html_content
        testHTML = raw_HTML.replace("target", oneSite) 
        resultName = oneSite.replace("/","").replace(":","").strip() + ".png"
        getScreenshot(driver_type, str(driver_location),testHTML, resultName)
