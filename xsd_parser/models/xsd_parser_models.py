class Attribute:
   
    name = None
    type = None
    minOccurs = None
    maxOccurs = None
    values = None
    parentAttribute = None
    readOnly = False
    documentation = None

    def __init__(self, name, type, minOccurs, maxOccurs, values, parentAttribute, documentation = None):
        self.name = name
        self.type = type

        if maxOccurs == "unbounded":
            self.maxOccurs = 99999
        else: 
            self.maxOccurs = int(maxOccurs)
        self.minOccurs = int(minOccurs)
        self.values = values
        self.parentAttribute = parentAttribute
        self.documentation = documentation

class Avgrensing:
    
    avgrensesAv = None
    name = None
    
    def __init__(self, avgrensesAv):
        self.avgrensesAv = avgrensesAv
        self.name = f"avgrensesAv{avgrensesAv}"

class XsdElement:
    
    name = None
    minOccurs = 1
    maxOccurs = 1
    typeName = None
    typeNamespace = None
    documentation = None
    defaultCodeSpace = None
    substitutionGroup = None

    def __init__(self, name, typeNamespace, typeName, documentation = None, defaultCodeSpace = None, substitutionGroup = None):
        self.name = name
        self.typeNamespace = typeNamespace
        self.typeName = typeName
        self.documentation = documentation
        self.defaultCodeSpace = defaultCodeSpace
        self.substitutionGroup = substitutionGroup

class Test:
    
    name = None

    def __init__(self, name):
        self.name = name

class Geometry:
    
    name = None
    type = None
    documentation = None
    minOccurs = None
    maxOccurs = None

    def __init__(self, name, type, minOccurs, maxOccurs, documentation):
        self.name = name
        self.type = type
        self.documentation = documentation
        self.minOccurs = int(minOccurs)
        if maxOccurs == "unbounded":
            self.maxOccurs = 99999
        else: 
            self.maxOccurs = int(maxOccurs)
   