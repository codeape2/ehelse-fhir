from datetime import datetime as dt


LOCATIONS = [
    "Se innkallingsbrev",
    "Medisinsk poliklinikk, Søndregate 18, STOKMARKNES",
    "Beh.omr. K3 Bodø, Prisensgt. 164, BODØ",
]


DOCUMENTS = [
    {"title": "Innkallingsbrev til timen", "docid": 1234}
]


ENCOUNTERS = [
    {
        "start": dt(2016, 5, 3, 12, 0, 0),
        "end": dt(2016, 5, 3, 12, 20, 0),
        "location": LOCATIONS[0],
        "documents": []
    }
]

REFERRALS = []



