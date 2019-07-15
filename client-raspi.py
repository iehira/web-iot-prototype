import urllib.request
import xml.etree.ElementTree as ET
import RPi.GPIO as GPIO
import time

class Node:
    def __init__(self):
        self.pinList = []
        self.trigerList = []
        self.actionList = []

    def parse_nodeinfo(self, XmlData):
        root = ET.fromstring(XmlData)
        if root.tag == 'node':
            for child in root:
                if child.tag == 'pin':
                    self.pinList.append(child.attrib)
                if child.tag == 'triger':
                    self.trigerList.append(child.attrib)
                if child.tag == 'action':
                    self.actionList.append(child.attrib)
    
    def node_initialization(self):
        #端末のピンを初期化
        for pin in self.pinList:
            dir = GPIO.IN
            if pin['dir'] == 'Output':
                dir = GPIO.OUT
            GPIO.setup(int(pin['number']), dir)

    def triger_check(self):
        #トリガーの発火を確認
        triger_info = [] #発火したトリガー
        for triger in self.trigerList:
            for pin in self.pinList:
                if ('name', triger['pin']) in pin:
                    if GPIO.input(int(pin['number'])) == GPIO.HIGH:
                        triger_info.append(triger['name'])
        return triger_info
    
    def run_action(self, run_triger_list):
        #指定されたトリガーを実行条件とするアクションを実行
        for triger in run_triger_list:
            for action in self.actionList:
                if ('triger', triger) in action:
                    self.run_action_child(action['url'])

    def run_action_child(self, url):
        with urllib.request.urlopen(url) as res:
            pin_output = res.read().decode("utf-8")
            root = ET.fromstring(pin_output)
            for child in root:
                if child.tag == 'pin':
                    for pin in self.pinList:
                        value = GPIO.HIGH
                        if child.attrib['value'] == '0':
                            value = GPIO.LOW
                        if ('name', child.attrib['name']) in pin:
                            GPIO.output(int(pin['number']), value)

    def mainfunction(self):
        print('test')
        triger_list = self.triger_check()
        print(trigerList)
        self.run_action(triger_list)

GPIO.setmode(GPIO.BCM)

with urllib.request.urlopen("http://XXX.XXX.XXX.XXX:8080/static/Board_info.xml") as res:
    node_info = res.read().decode("utf-8")

    node1 = Node()
    node1.parse_nodeinfo(node_info)
    print(node1.pinList)
    print(node1.trigerList)
    print(node1.actionList)

    while True:
        node1.mainfunction()

        

GPIO.cleanup()