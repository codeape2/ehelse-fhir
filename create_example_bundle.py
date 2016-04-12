from lxml import etree as ET
from datetime import datetime as dt
import pytz


TZ = pytz.timezone("Europe/Oslo")

ldt = lambda *args: TZ.localize(dt(*args))

LOCATIONS = [
    "Se innkallingsbrev",
    "Medisinsk poliklinikk, Søndregate 18, STOKMARKNES",
    "Beh.omr.K3 Bodø, Prinsensgt. 164, Bodø",
]

DOCUMENTREFERENCES = [
    {
        "title": "Innkallingsbrev",
        "encounterref": "2"
    },

    {
        "title": "Viktig informasjon før du kommer til timen",
        "encounterref": "2"
    }
]

ENCOUNTERS = [
    {
        "start": ldt(2016, 5, 3, 12, 30),
        "end": ldt(2016, 5, 3, 13, 0),
        "locationref": "2"
    }
]

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

bundle = FHIRElement("Bundle", type=value("searchset"))

locations = [FHIRElement("Location", id=value(str(i + 1)), name=value(text)) for i, text in enumerate(LOCATIONS)]
encounters = [
    FHIRElement(
        "Encounter",
        id=value(str(i + 1)),
        period={"start": value(encounter_dict["start"].isoformat()), "end": value(encounter_dict["end"].isoformat())},
        location={
            "location": {"reference": value("Location/{}".format(encounter_dict["locationref"]))}
        }
    )
    for i, encounter_dict in enumerate(ENCOUNTERS)]

documentreferences = [
    FHIRElement(
        "DocumentReference",
        id=value(str(i+1)),
        context={
            "encounter": {"reference": value("Encounter/{}".format(document_dict["encounterref"]))}
        }
    )
    for i, document_dict in enumerate(DOCUMENTREFERENCES)
]

#location = FHIRElement("Location", name=value(LOCATIONS[0]))
bundle.extend(wrap_in_entry(encounter) for encounter in encounters)
bundle.extend(wrap_in_entry(location) for location in locations)
bundle.extend(wrap_in_entry(dref) for dref in documentreferences)
#printprettyxml(location)
printprettyxml(bundle)