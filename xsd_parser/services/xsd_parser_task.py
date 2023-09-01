import os
import xml.etree.ElementTree as ET
from xml.parsers.expat import ExpatError  # XML formatting errors
import requests
import time
from multiprocessing import Pool, Process
from xsd_parser.services.xsd_parser_functions import XsdParser
from xsd_parser.models.xsd_parser_models import XsdElement
from PyQt5.QtCore import pyqtSignal

from qgis.core import (
  QgsProcessingContext,
  QgsTaskManager,
  QgsTask,
  QgsProcessingAlgRunnerTask,
  Qgis,
  QgsProcessingFeedback,
  QgsApplication,
  QgsMessageLog,
  QgsWkbTypes)


class FetchXsdElement(QgsTask):

    resultSignal = pyqtSignal(object)

    """This shows how to subclass QgsTask"""
    def __init__(self, description, elements, types, parent_map, element):
        super().__init__(description, QgsTask.CanCancel)
        #Process.__init__(self)
        self.description = description
        self.element = element
        self.elements = elements
        self.exception = None
        self.types = types
        self.parent_map = parent_map
    
    def run(self):

        print(f"Started task {self.description}")

        namespace, typeName = self.elements[self.element].split(':', 1)

        ele = XsdElement(self.element, namespace, typeName)

        session = requests.Session()

        xsd_parser = XsdParser(self.elements, self.types, self.parent_map)

        egenskaper = xsd_parser.utled_egenskaper(ele, None, False, session)

        #print(f"Feeeerdig med task {self.description}")

        # for egenskap in egenskaper:
        #     self.result_dict[self.element][egenskap.name] = egenskap
        
        self.resultSignal.emit((self.element, egenskaper))

        session.close()

        return True

    def finished(self, result):

        if result:
            print(f'Task {self.description} completed successfully')
        else:
            if self.exception is None:
                print(f'Task {self.description} was not successful but did not raise an exception')
            else:
                print(f'Task {self.description} was not successful and raised an exception')

class MainTask(QgsTask):

    resultSignal = pyqtSignal(object)
    subtasks = []
    resultdict = {}

    def handleSubtaskResult(self, result):
        element = result[0]
        egenskaper = result[1]
        self.resultdict[element] = {}
        for egenskap in egenskaper:
            self.resultdict[element][egenskap.name] = egenskap

    def __init__(self, description, subtasks):
        super().__init__(description, QgsTask.CanCancel)
        self.subtasks = subtasks
        for subtask in self.subtasks:
            subtask.resultSignal.connect(self.handleSubtaskResult)
            self.addSubTask(subtask)

    def run(self):
        finished = False
        while not finished:
            for subtask in self.subtasks:
                if subtask.isActive():
                    finished = False
                    break
                finished = True
            time.sleep(1)
        if finished:
            return True

    def finished(self, result):
        self.resultSignal.emit(self.resultdict)
        #self.deleteLater()
        
def ParseXSD(xmlstring):
    try:
        #Parse the given XML file:
        tree = ET.ElementTree(ET.fromstring(xmlstring))
    except ExpatError as e:
        print ("[XML] Error (line %d): %d" % (e.lineno, e.code))
        print ("[XML] Offset: %d" % (e.offset))
        raise e
    except IOError as e:
        print ("[XML] I/O Error %d: %s" % (e.errno, e.strerror))
        raise e

    root = tree.getroot()
    
    
    parent_map = {c: p for p in tree.iter() for c in p}
    elements = {}
    types = {}
    
    defaultNamespace = f"{{http://www.w3.org/2001/XMLSchema}}"
    simpleTypeString = f"{defaultNamespace}simpleType"
    complexTypeString = f"{defaultNamespace}complexType"
    elementString = f"{defaultNamespace}element"

    for entry in root:
        if entry.tag == elementString:
            type = entry.attrib.get('type', None)
            abstract = entry.attrib.get('abstract', False)
            if not abstract:
                elements[entry.attrib['name']] = type
        elif entry.tag == simpleTypeString:
            types[entry.attrib['name']] = {'entry': entry, 'simple': True}
        elif entry.tag == complexTypeString:
            types[entry.attrib['name']] = {'entry': entry, 'simple': False}


    
    # #DEBUG
    # for element in elements:
        
    #     subtask = FetchXsdElement(f"TASK_{element}", elements, types, parent_map, element)
    #     subtask.run()
        

    subtasks = []

    for element in elements:
        
        subtask = FetchXsdElement(f"TASK_{element}", elements, types, parent_map, element)
        subtasks.append(subtask)

    task = MainTask('Tolkning GML-skjema', subtasks)

    return task
    
    
  

def testfunction(self, elements, element):

    namespace, typeName = elements[element].split(':', 1)

    ele = XsdElement(element, namespace, typeName)

    session = requests.Session()

    xsd_parser = XsdParser(self.elements, self.types, self.parent_map)
    
    result =  xsd_parser.utled_egenskaper(ele, None, False, session)

    session.close()

    return result