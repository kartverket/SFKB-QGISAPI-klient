import os
import xml.etree.ElementTree as ET
from xml.parsers.expat import ExpatError  # XML formatting errors
import requests
import time
from multiprocessing import Pool
from qgis.core import (
  QgsProcessingContext,
  QgsTaskManager,
  QgsTask,
  QgsProcessingAlgRunnerTask,
  Qgis,
  QgsProcessingFeedback,
  QgsApplication,
  QgsMessageLog)

class XsdElement:
    name = None
    minOccurs = 1
    maxOccurs = 1
    typeName = None
    typeNamespace = None
    documentation = None
    defaultCodeSpace = None

    def __init__(self, name, typeNamespace, typeName, documentation = None, defaultCodeSpace = None):
        self.name = name
        self.typeNamespace = typeNamespace
        self.typeName = typeName
        self.documentation = documentation
        self.defaultCodeSpace = defaultCodeSpace

class Attribute:
    name = None
    type = None
    minOccurs = None
    maxOccurs = None
    values = None
    xmlPath = None
    readOnly = False
    documentation = None

    def __init__(self, name, type, minOccurs, maxOccurs, values, xmlPath, documentation = None):
        self.name = name
        self.type = type

        if maxOccurs == "unbounded":
            self.maxOccurs = 99999
        else: 
            self.maxOccurs = int(maxOccurs)
        self.minOccurs = int(minOccurs)
        self.values = values
        self.xmlPath = xmlPath
        self.documentation = documentation

def add_sekvens(sekvens, schemaPath, session):
    underelementer = sekvens.findall(f"{defaultNamespace}element")
    result = []
    for element in underelementer:
        elementRef = element.attrib.get('ref', None)
        try:
            if elementRef:
                namespace, refTypeName = elementRef.split(':', 1)
                elementTypeNamespace, elementTypeName = elements[refTypeName].split(':', 1)
                print(f"Referer til {element} ({elementTypeName})")
                ele = XsdElement(refTypeName,elementTypeNamespace, elementTypeName)
                result.extend(utled_egenskaper(ele, schemaPath, True, session))
            else:
                elementName = element.attrib.get('name', None)
                elementType = element.attrib.get('type', None)

                minOccurs = element.attrib.get('minOccurs', 1)
                maxOccurs = element.attrib.get('maxOccurs', 1)

                print(f"Sekvens {elementName} ({elementType})")
                
                namespace = None
                elementTypeName = None
                elementTypeNamespace = None
                
                if elementType:
                    *namespace, elementTypeName = elementType.split(':', 1)
                    elementTypeNamespace = namespace[0] if namespace else None
                
                doc, codeSpace = get_documentation_from_annotation(element)

                ele = XsdElement(elementName, elementTypeNamespace, elementTypeName, doc, codeSpace)
                ele.minOccurs = minOccurs
                ele.maxOccurs = maxOccurs

                result.extend(utled_egenskaper(ele, schemaPath, False, session))
        except Exception as e:
            print(f'Exception here: {elementType}')
    return result

def get_documentation_from_annotation(element):
    annotation = element.find(f"{defaultNamespace}annotation")
    doc = None
    codeSpace = None
    if annotation is not None:
        documentation = annotation.find(f"{defaultNamespace}documentation")
        if documentation is not None: 
            doc = documentation.text
        appinfo = annotation.find(f"{defaultNamespace}appinfo")
        if appinfo is not None:
            defaultCodeSpace = appinfo.find(f"{gmlNamespace}defaultCodeSpace")
            if defaultCodeSpace is not None:
                codeSpace = defaultCodeSpace.text
    return doc, codeSpace

def handle_restriction(entryName, element, schemaPath):
    base = element.attrib['base']
    enumerations = element.findall(f"{defaultNamespace}enumeration")
    pattern = element.find(f"{defaultNamespace}pattern")
    
    parent = parent_map[element] if element in parent_map else None
    restriction_doc = None
    
    if parent:
        restriction_doc, _ = get_documentation_from_annotation(parent)

    if enumerations:
        enums = []
        for enum in enumerations:
            val = enum.attrib['value']
            doc, _ = get_documentation_from_annotation(enum)
            enums.append({"type": base, "value": val, "desc": doc})
        print(f"fant {entryName} (enum)")
        return [Attribute(entryName, "enum", 1, 1, enums, schemaPath, restriction_doc)]
    elif pattern is not None:
        # TODO
        return []
    else:
        raise Exception("Not implemented")

def handle_kodeliste(xsdElement: XsdElement, schemaPath, session):

    if xsdElement.defaultCodeSpace is None:
        return [Attribute(xsdElement.name, "string", xsdElement.minOccurs, xsdElement.maxOccurs, None, schemaPath, xsdElement.documentation)]

    response = session.get(f"{xsdElement.defaultCodeSpace}.json", verify=False)
    json = response.json()

    enums = []
    if "containeditems" in json:
        for enum in json["containeditems"]:
            base = enum['label']
            val = enum['codevalue']
            doc = enum['description']
            enums.append({"type": base, "value": val, "desc": doc})

    return [Attribute(xsdElement.name, "enum", xsdElement.minOccurs, xsdElement.maxOccurs, enums, schemaPath, xsdElement.documentation)]


def utled_egenskaper(xsdElement: XsdElement, schemaPath, ref, session):

    typeDict = types.get(xsdElement.typeName, None)
    if xsdElement.typeNamespace == 'gml':
        if xsdElement.typeName == 'CodeType': 
            return handle_kodeliste(xsdElement, schemaPath, session)
        return []
    if not xsdElement.typeNamespace:
        print(f"fant {xsdElement.name} ({xsdElement.typeName})")
        return [Attribute(xsdElement.name, xsdElement.typeName, xsdElement.minOccurs, xsdElement.maxOccurs, None, schemaPath, xsdElement.documentation)]
    
    simple = typeDict['simple']
    entry = typeDict['entry']
    entryName = entry.attrib['name']
    
    if simple:
        union = entry.find(f"{defaultNamespace}union")
        restriction = entry.find(f"{defaultNamespace}restriction")
        print(f"Simple type: Inne i {entryName}")
        if union is not None:
            memberTypes = union.attrib.get('memberTypes', None)
            result = []
            for memberType in memberTypes.split(' '):
                *namespace, typeName = memberType.split(':', 1)
                typeNamespace = namespace[0] if namespace else None
                ele = XsdElement(xsdElement.name, typeNamespace, typeName)
                ele.minOccurs = xsdElement.minOccurs
                ele.maxOccurs = xsdElement.maxOccurs
                
                res = utled_egenskaper(ele, schemaPath, False, session)
                result.extend(res)
            return result
        elif restriction is not None:
            return handle_restriction(xsdElement.name, restriction, schemaPath)
        else:
            raise Exception("Not implemented")
    else:
        print(f"Complex type: Inne i {entryName}")
        complexContent = entry.find(f"{defaultNamespace}complexContent")
        sequence = entry.find(f"{defaultNamespace}sequence")
        if complexContent is not None:
            child = list(complexContent)[0]
            if child.tag == f"{defaultNamespace}extension":
                # extension
                base = child.attrib['base']
                extensionTypeNamespace, extensionTypeName = base.split(':', 1)
                print(f"Extension: Utleder egenskaper til {extensionTypeName}")
                result = []
                ele = XsdElement(entryName, extensionTypeNamespace, extensionTypeName)
                result.extend(utled_egenskaper(ele, schemaPath, False, session))
                sekvens = child.find(f"{defaultNamespace}sequence")
                print(f"Extension: Utleder egenskaper i sekvensen til {entryName}")
                result.extend(add_sekvens(sekvens, schemaPath, session))
                return result
        elif sequence is not None:
            if not ref:
                schemaPath = [xsdElement.name]
            print("sequence")
            return add_sekvens(sequence, schemaPath, session)
        else:
            raise Exception("Not implemented")

defaultNamespace = f"{{http://www.w3.org/2001/XMLSchema}}"
gmlNamespace = f"{{http://www.opengis.net/gml/3.2}}"
elements = {}
types = {}
parent_map = {}
result_dict = {}
result_counter = 0

elementString = f"{defaultNamespace}element"
simpleTypeString = f"{defaultNamespace}simpleType"
complexTypeString = f"{defaultNamespace}complexType"

def parseXSD(xmlstring):
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
    
    global parent_map
    parent_map = {c: p for p in tree.iter() for c in p}

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

    global result_dict
    global result_counter

    for element in elements:
        result_dict[element] = {}
    
    tm = QgsApplication.taskManager()

    for element in elements:
        print(f"EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE {element}")
        tm.addTask(RandomIntegerSumTask(f"TASK_{element}",result_dict, elements, element))
        #for egenskap in egenskaper:
            #result[element][egenskap.name] = egenskap


    #for element in elements:
    #    egenskaper = testfunction(element)
    #    for egenskap in egenskaper:
    #        result[element][egenskap.name] = egenskap
    time.sleep(5)
    
    return result_dict

def completed():
    
    global result_dict
    global result_counter

    print(f"COMPLETED")
    
    #element = result["element"]
    

   # for egenskap in result["egenskaper"]:
    #        result[element][egenskap.name] = egenskap
    
    #result_counter += 1

def testfunction(task, element):

    print(f"Started task {task.description()}")

    namespace, typeName = elements[element].split(':', 1)

    ele = XsdElement(element, namespace, typeName)

    session = requests.Session()

    egenskaper = utled_egenskaper(ele, [], False, session)

    print(f"Ferdig med task {task.description()}")
    return {'element': element, 'egenskaper': egenskaper}


class RandomIntegerSumTask(QgsTask):
    """This shows how to subclass QgsTask"""
    def __init__(self, description, result_dict, elements, element):
        super().__init__(description, QgsTask.CanCancel)
        self.result_dict = result_dict
        self.description = description
        self.element = element
        self.elements = elements
        self.egenskaper = None
        self.exception = None
    def run(self):
        """Here you implement your heavy lifting.
        Should periodically test for isCanceled() to gracefully
        abort.
        This method MUST return True or False.
        Raising exceptions will crash QGIS, so we handle them
        internally and raise them in self.finished
        """
        print(f"Started task {self.description}")

        namespace, typeName = self.elements[self.element].split(':', 1)

        ele = XsdElement(self.element, namespace, typeName)

        session = requests.Session()

        self.egenskaper = utled_egenskaper(ele, [], False, session)

        print(f"Feeeerdig med task {self.description}")
    
        for egenskap in self.egenskaper:
            self.result_dict[self.element][egenskap.name] = egenskap
        return True

    def finished(self, result):
        """
        This function is automatically called when the task has
        completed (successfully or not).
        You implement finished() to do whatever follow-up stuff
        should happen after the task is complete.
        finished is always called from the main thread, so it's safe
        to do GUI operations and raise Python exceptions here.
        result is the return value from self.run.
        """

        print("FERDIG")

    def cancel(self):
        QgsMessageLog.logMessage(
            'Task "{name}" was canceled'.format(
                name=self.description()),
            MESSAGE_CATEGORY, Qgis.Info)
        super().cancel()