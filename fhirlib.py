from lxml import etree as ET


FHIR_NAMESPACE = "http://hl7.org/fhir"
FHIR = "{" + FHIR_NAMESPACE + "}"


def FHIRElement(resourcetype, **kwargs):
    resource = ET.Element(FHIR + resourcetype, nsmap={None: FHIR_NAMESPACE})
    add_subelements_from_dict(resource, kwargs)
    return resource


def add_subelements_from_dict(element, subelements_dict):
    for k, v in subelements_dict.items():
        if k.startswith("@"):
            element.attrib[k[1:]] = v
        else:
            if k == "class_":
                k = "class"
            subelement = ET.SubElement(element, FHIR + k)
            add_subelements_from_dict(subelement, v)
        #add_subelements_from_dict(subelement, v)


def printprettyxml(elmt):
    print(prettyxml(elmt))


def prettyxml(elmt):
    return ET.tostring(elmt, encoding="unicode", pretty_print=True)


def value(text):
    return {"@value": text}


def wrap_in_entry(resource):
    entry = FHIRElement("entry")
    resource_wrapper = FHIRElement("resource")
    entry.append(resource_wrapper)
    resource_wrapper.append(resource)
    return entry