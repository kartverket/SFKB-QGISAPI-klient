from xsd_parser.models.xsd_parser_models import Attribute, Avgrensing, Geometry, XsdElement
from qgis.core import (QgsWkbTypes)

class XsdParser:
    
    debug = False

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

    def __init__(self, elements, types, parent_map):
        self.elements = elements
        self.types = types
        self.parent_map = parent_map

    def add_sekvens(self, sekvens, parentAttribute, session):
        underelementer = sekvens.findall(f"{self.defaultNamespace}element")
        result = []
        for element in underelementer:
            elementRef = element.attrib.get('ref', None)
            try:
                if elementRef:
                    namespace, refTypeName = elementRef.split(':', 1)
                    elementTypeNamespace, elementTypeName = self.elements[refTypeName].split(':', 1)
                    if self.debug: print(f"Referer til {element} ({elementTypeName})")
                    ele = XsdElement(refTypeName,elementTypeNamespace, elementTypeName)
                    # Add extra attribute for list of complex self.elements here? (maton, 31.10.2022)
                    result.extend(self.utled_egenskaper(ele, parentAttribute, True, session))
                else:
                    elementName = element.attrib.get('name', None)
                    elementType = element.attrib.get('type', None)
                    substitutionGroup = element.attrib.get('substitutionGroup', None)

                    minOccurs = element.attrib.get('minOccurs', 1)
                    maxOccurs = element.attrib.get('maxOccurs', 1)

                    if self.debug: print(f"Sekvens {elementName} ({elementType})")
                    
                    namespace = None
                    elementTypeName = None
                    elementTypeNamespace = None
                    
                    if elementType:
                        *namespace, elementTypeName = elementType.split(':', 1)
                        elementTypeNamespace = namespace[0] if namespace else None
                    
                    doc, codeSpace, reverseProperty = self.get_documentation_from_annotation(element)

                    ele = XsdElement(elementName, elementTypeNamespace, elementTypeName, doc, codeSpace, substitutionGroup)
                    ele.minOccurs = minOccurs
                    ele.maxOccurs = maxOccurs
                    if reverseProperty is not None:
                        print("jasså")
                    if reverseProperty is None:
                        result.extend(self.utled_egenskaper(ele, parentAttribute, False, session))
            except Exception as e:
                if self.debug: print(f'Exception here: {elementType}')
        
        return result

    def get_documentation_from_annotation(self, element):
        annotation = element.find(f"{self.defaultNamespace}annotation")
        doc = None
        codeSpace = None
        reverseProperty = None
        if annotation is not None:
            documentation = annotation.find(f"{self.defaultNamespace}documentation")
            if documentation is not None: 
                doc = documentation.text
            appinfo = annotation.find(f"{self.defaultNamespace}appinfo")
            if appinfo is not None:
                defaultCodeSpace = appinfo.find(f"{self.gmlNamespace}defaultCodeSpace")
                if defaultCodeSpace is not None:
                    codeSpace = defaultCodeSpace.text
                reversePropertyName = appinfo.find(f"{self.gmlNamespace}reversePropertyName")
                if reversePropertyName is not None:
                    reverseProperty = reversePropertyName.text
        return doc, codeSpace, reverseProperty

    def handle_restriction(self, entryName, element, parentAttribute):
        base = element.attrib['base']
        enumerations = element.findall(f"{self.defaultNamespace}enumeration")
        pattern = element.find(f"{self.defaultNamespace}pattern")
        
        parent = self.parent_map[element] if element in self.parent_map else None
        restriction_doc = None
        
        if parent:
            restriction_doc, _, _ = self.get_documentation_from_annotation(parent)

        if enumerations:
            enums = []
            for enum in enumerations:
                val = enum.attrib['value']
                doc, _, _ = self.get_documentation_from_annotation(enum)
                enums.append({"type": base, "value": val, "desc": doc})
            if self.debug: print(f"fant {entryName} (enum)")
            return [Attribute(entryName, "enum", 1, 1, enums, parentAttribute, restriction_doc)]
        elif pattern is not None:
            # TODO
            return []
        else:
            raise Exception("Not implemented")

    def handle_kodeliste(self, xsdElement: XsdElement, parentAttribute, session):

        if xsdElement.defaultCodeSpace is None:
            return [Attribute(xsdElement.name, "string", xsdElement.minOccurs, xsdElement.maxOccurs, None, parentAttribute, xsdElement.documentation)]

        response = session.get(f"{xsdElement.defaultCodeSpace}.json", verify=False)
        json = response.json()

        enums = []
        if "containeditems" in json:
            for enum in json["containeditems"]:
                base = enum['label']
                val = enum['codevalue']
                doc = enum['description']
                enums.append({"type": base, "value": val, "desc": doc})

        return [Attribute(xsdElement.name, "enum", xsdElement.minOccurs, xsdElement.maxOccurs, enums, parentAttribute, xsdElement.documentation)]

    def utled_egenskaper(self, xsdElement: XsdElement, parentAttribute, ref, session):

        typeDict = self.types.get(xsdElement.typeName, None)

        if xsdElement.name[0:11] == 'avgrensesAv':
            return[Avgrensing(xsdElement.name[11:])]

        if xsdElement.typeNamespace == 'gml':
            if xsdElement.typeName == 'CodeType': 
                return self.handle_kodeliste(xsdElement, parentAttribute, session)
            if xsdElement.typeName == 'SurfacePropertyType':
                return [Geometry(xsdElement.name, QgsWkbTypes.PolygonZ, xsdElement.minOccurs, xsdElement.maxOccurs, xsdElement.documentation)]
            if xsdElement.typeName == 'PointPropertyType':
                return [Geometry(xsdElement.name, QgsWkbTypes.PointZ, xsdElement.minOccurs, xsdElement.maxOccurs, xsdElement.documentation)]
            if xsdElement.typeName == 'CurvePropertyType':
                return [Geometry(xsdElement.name, QgsWkbTypes.LineStringZ, xsdElement.minOccurs, xsdElement.maxOccurs, xsdElement.documentation)]
            return []
        
        if not xsdElement.typeNamespace:
            if self.debug: print(f"fant {xsdElement.name} ({xsdElement.typeName})")
            return [Attribute(xsdElement.name, xsdElement.typeName, xsdElement.minOccurs, xsdElement.maxOccurs, None, parentAttribute, xsdElement.documentation)]


        simple = typeDict['simple']
        entry = typeDict['entry']
        entryName = entry.attrib['name']
        
        if simple:
            union = entry.find(f"{self.defaultNamespace}union")
            restriction = entry.find(f"{self.defaultNamespace}restriction")
            if self.debug: print(f"Simple type: Inne i {entryName}")
            if union is not None:
                memberTypes = union.attrib.get('memberTypes', None)
                result = []
                for memberType in memberTypes.split(' '):
                    *namespace, typeName = memberType.split(':', 1)
                    typeNamespace = namespace[0] if namespace else None
                    ele = XsdElement(xsdElement.name, typeNamespace, typeName)
                    ele.minOccurs = xsdElement.minOccurs
                    ele.maxOccurs = xsdElement.maxOccurs
                    
                    res = self.utled_egenskaper(ele, parentAttribute, False, session)
                    result.extend(res)
                return result
            elif restriction is not None:
                return self.handle_restriction(xsdElement.name, restriction, parentAttribute)
            else:
                raise Exception("Not implemented")
        else:
            if self.debug: print(f"Complex type: Inne i {entryName}")
            complexContent = entry.find(f"{self.defaultNamespace}complexContent")
            sequence = entry.find(f"{self.defaultNamespace}sequence")
            if complexContent is not None:
                child = list(complexContent)[0]
                if child.tag == f"{self.defaultNamespace}extension":
                    # extension
                    base = child.attrib['base']
                    extensionTypeNamespace, extensionTypeName = base.split(':', 1)
                    if self.debug: print(f"Extension: Utleder egenskaper til {extensionTypeName}")
                    result = []
                    ele = XsdElement(entryName, extensionTypeNamespace, extensionTypeName)
                    result.extend(self.utled_egenskaper(ele, parentAttribute, False, session))
                    sekvens = child.find(f"{self.defaultNamespace}sequence")
                    if self.debug: print(f"Extension: Utleder egenskaper i sekvensen til {entryName}")
                    result.extend(self.add_sekvens(sekvens, parentAttribute, session))
                    return result
            elif sequence is not None:
                if not ref:
                    parentAttribute = Attribute(xsdElement.name, "complexType", xsdElement.minOccurs, xsdElement.maxOccurs, None, parentAttribute, xsdElement.documentation)
                if self.debug: print("sequence")
                return self.add_sekvens(sequence, parentAttribute, session)
            else:
                raise Exception("Not implemented")
    
