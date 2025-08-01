"""
Initializes the vocabulary for the data model
"""

from django.core.management.base import BaseCommand

from apis_ontology.models import EventCategory, Title, PlaceCategory

EVENT_CATEGORIES = [
    "Assistenzeinsatz",
    "Auslandseinsatz",
    "Konflikte",
    "Kriege",
    "Schlachten",
    "Marsch",
    "Geburtstag",
    "Todestag",
    "politische Ereignisse",
    "Demonstration",
    "Kundgebung",
    "Versammlung",
    "Veranstaltungen",
    "Feierlichkeiten",
    "Sportveranstaltung",
    "Naturereignis",
    "Streik",
    "Parade",
    "Revolution",
    "Brand",
    "Protestaktion",
    "Bürgerinitiative",
    "Attentat",
    "Anschlag",
    "Gedenkveranstaltung",
    "Jubiläum",
    "sonstiges Ereignis",
]

TITLES = {
    "akademischer Titel": [
        ("Dr.", "Doktor"),
        ("Prof.", "Professor"),
        ("Prof.", "Professorin"),
    ],
    "militärischer Dienstgrad": [
        ("Rer", "Rekrut"),
        ("Gfr", "Gefreite"),
        ("Kpl", "Korporal"),
        ("Lt", "Leutnant"),
    ],
    "Adelstitel": [
        ("Prinz", "Prinz"),
        ("Prinzessin", "Prinzessin"),
        ("König", "König"),
        ("Königin", "Königin"),
        ("Herzog", "Herzog"),
        ("Herzogin", "Herzogin"),
        ("Graf", "Graf"),
        ("Gräfin", "Gräfin"),
        ("Baron", "Baron"),
        ("Baronin", "Baronin"),
    ],
    "Amtstitel": [
        ("Bundespräsident", "Bundespräsident"),
        ("Bundeskanzler", "Bundeskanzler"),
        ("Minister", "Minister"),
        ("Staatssekretär", "Staatssekretär"),
        ("Abgeordneter", "Abgeordneter"),
        ("Abgeordnete", "Abgeordnete"),
    ],
}

PLACE_TYPES = [
    "Stadt",
    "Bundesland",
    "Bezirk",
    "Kanton",
    "Provinz",
    "Staat",
    "Kaserne",
    "Flugplatz",
    "Kommandogebäude",
    "Gedenkstätte",
    "Erinnerungsort",
    "Gemeinde",
]


class Command(BaseCommand):
    """Populate the vocabulary with initial data"""

    help = "Populate the vocabulary with initial data"

    def handle(self, *args, **kwargs):
        """Handle the command"""
        # Create initial professions
        for ec in sorted(EVENT_CATEGORIES):
            EventCategory.objects.get_or_create(label=ec)

        for title_group, titles in TITLES.items():
            for t in titles:
                Title.objects.get_or_create(
                    label_type=title_group, abbreviation=t[0], label=t[1]
                )

        for place_type in sorted(PLACE_TYPES):
            PlaceCategory.objects.get_or_create(label=place_type)

        self.stdout.write(self.style.SUCCESS("Vocabulary populated successfully."))
