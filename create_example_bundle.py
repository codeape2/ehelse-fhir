from lxml import etree as ET
from datetime import datetime as dt
import pytz

from fhirlib import FHIRElement, value, wrap_in_entry, printprettyxml, add_subelements_from_dict


TZ = pytz.timezone("Europe/Oslo")

ldt = lambda *args: TZ.localize(dt(*args))

ORGANIZATIONS = [
    {
        "name": "Nordlandssykehuset HF",
        "phone": "95812112",
    },

    {
        "name": "Finnmarkssykehuset HF",
        "phone": "01234",
    },

    {
        "name": "Medisinsk avdeling",
        "orgref": "1",
    },

    {
        "name": "Gastrokirurgisk avdeling",
        "orgref": "2",
    }
]

LOCATIONS = [
    {
        "name": "Se innkallingsbrev",
        "orgref": "4",
    },
    {
        "name": "Medisinsk poliklinikk, Søndregate 18, STOKMARKNES",
        "orgref": "3",
    },
    {
        "name": "Beh.omr.K3 Bodø, Prinsensgt. 164, Bodø",
        "orgref": "3",

    },
]

DOCUMENTREFERENCES = [
    {
        "description": "Innkallingsbrev",
        "encounterref": "1",
        "xdsdocid": "157222",
    },

    {
        "description": "Viktig informasjon før du kommer til timen",
        "encounterref": "1",
        "xdsdocid": "164399",
    }
]

ENCOUNTERS = [
    {
        "start": ldt(2016, 5, 3, 12, 30),
        "end": ldt(2016, 5, 3, 13, 0),
        "locationref": "2",
        "class": "outpatient" # inpatient, outpatient, ambulatory, emergency, home, field, daytime, virtual, other
    },

    {
        "start": ldt(2016, 5, 4, 14),
        "end": ldt(2016, 5, 4, 14, 30),
        "locationref": "1",
        "class": "inpatient",
    },

    {
        "start": ldt(2016, 5, 12, 15),
        "end": ldt(2016, 5, 12, 16),
        "locationref": "3",
        "class": "inpatient",
    }
]


def OrganizationElement(id, organization_dict):
    retval = FHIRElement("Organization", id=value(id), name=value(organization_dict["name"]))
    if "orgref" in organization_dict:
        add_subelements_from_dict(retval, {"partOf": {"reference": value("Organization/{}".format(organization_dict["orgref"]))}})
    if "phone" in organization_dict:
        add_subelements_from_dict(retval, {"telecom": {"system": value("phone"), "value": value(organization_dict["phone"])}})
    return retval


bundle = FHIRElement("Bundle", type=value("searchset"))

locations = [
    FHIRElement(
        "Location",
        id=value(str(i + 1)),
        name=value(location_dict["name"]),
        managingOrganization={"reference": value("Organization/{}".format(location_dict["orgref"]))}
    )
    for i, location_dict in enumerate(LOCATIONS)
]
organizations = [
    OrganizationElement(str(i+1), organization_dict)
    for i, organization_dict in enumerate(ORGANIZATIONS)
]

encounters = [
    FHIRElement(
        "Encounter",
        id=value(str(i + 1)),
        class_=value(encounter_dict["class"]),
        period={"start": value(encounter_dict["start"].isoformat()), "end": value(encounter_dict["end"].isoformat())},
        location={
            "location": {"reference": value("Location/{}".format(encounter_dict["locationref"]))}
        }
    )
    for i, encounter_dict in enumerate(ENCOUNTERS)]

documentreferences = [
    FHIRElement(
        "DocumentReference",
        id=value(document_dict["xdsdocid"]),
        description=value(document_dict["description"]),
        masterIdentifier={"value": value(document_dict["xdsdocid"])},
        context={
            "encounter": {"reference": value("Encounter/{}".format(document_dict["encounterref"]))}
        }
    )
    for i, document_dict in enumerate(DOCUMENTREFERENCES)
]

#location = FHIRElement("Location", name=value(LOCATIONS[0]))
bundle.extend(wrap_in_entry(encounter) for encounter in encounters)
bundle.extend(wrap_in_entry(location) for location in locations)
bundle.extend(wrap_in_entry(organization) for organization in organizations)
bundle.extend(wrap_in_entry(dref) for dref in documentreferences)
#printprettyxml(location)
printprettyxml(bundle)