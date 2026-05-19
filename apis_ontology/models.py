from apis_core.apis_entities.abc import (
    E53_Place,
    E21_Person,
    E74_Group,
    SimpleLabelModel,
)
from apis_core.apis_entities.models import AbstractEntity
from apis_core.generic.abc import GenericModel
from apis_core.history.models import VersionMixin
from apis_core.relations.models import Relation
from django.utils.translation import gettext_lazy as _
from django.db import models
from django_interval.fields import FuzzyDateParserField


class Glossar(GenericModel, SimpleLabelModel):
    definition = models.TextField(blank=True, null=True)

    class Meta(SimpleLabelModel.Meta):
        verbose_name = _("Glossary")
        verbose_name_plural = _("Glossary")


class EntityMixin(models.Model):
    glossar_terms = models.ManyToManyField(
        Glossar, blank=True, verbose_name=_("Glossary terms")
    )

    class Meta:
        abstract = True


class DateMixin(models.Model):
    start = FuzzyDateParserField(
        null=True,
        blank=True,
        verbose_name=_("Start"),
    )
    end = FuzzyDateParserField(
        null=True,
        blank=True,
        verbose_name=_("End"),
    )

    class Meta:
        abstract = True


class EventCategory(GenericModel, SimpleLabelModel):
    """
    Z. B. Einsatz: Assistenzeinsatz, Auslandseinsatz; Konflikte,
    Kriege, Schlachten, Marsch, Geburtstag, Todestag,
    politische Ereignisse, Demonstration, Kundgebung, Versammlung,
    Veranstaltungen und Feierlichkeiten, Sportveranstaltung,
    Naturereignis, Streik, Parade, Revolution, Brand, Protestaktion,
    Bürgerinitiative, Attentat, Anschlag, Gedenkveranstaltung,
    Jubiläum, sonstiges Ereignis etc.
    """

    description = models.TextField(blank=True, null=True)

    class Meta(SimpleLabelModel.Meta):
        verbose_name = _("Event category")
        verbose_name_plural = _("Event categories")


class Event(EntityMixin, AbstractEntity, DateMixin, VersionMixin):
    label = models.CharField(max_length=1024, blank=True, null=True, verbose_name=_("Label"))
    category = models.ManyToManyField(
        EventCategory, blank=True, verbose_name=_("Category")
    )
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    background = models.TextField(
        blank=True, verbose_name=_("background")
    )  # Hintergrund
    anecdotes = models.TextField(
        blank=True, null=True, verbose_name=_("anecdotes")
    )  # anekdoten
    is_turning_point = models.BooleanField(
        default=False, verbose_name=_("Turning point")
    )
    is_decisive = models.BooleanField(default=False, verbose_name=_("Decisive moment"))
    short_term_effects = models.TextField(
        blank=True, verbose_name=_("short term effects")
    )  # Kurzfristige Auswirkungen
    long_term_effects = models.TextField(
        blank=True, verbose_name=_("long term effects")
    )  # Langfristige Auswirkungen

    changes = models.TextField(blank=True, verbose_name=_("changes"))  # Veränderungen
    historical_significance = models.TextField(
        blank=True, verbose_name=_("historical significance")
    )  # Historische Bedeutung
    interpretation = models.TextField(
        blank=True, verbose_name=_("interpretation")
    )  # Nachwelt
    commemoration = models.TextField(
        blank=True, verbose_name=_("commemoration")
    )  # Denkmäler/Gedenken

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ["start"]

    def __str__(self):
        label = getattr(self, "label", None)
        if label:
            return f"{label} ({self.pk})"

        # Fallback to a textual field if `label` is not available.
        # Prefer `description` if present, otherwise `background`.
        desc = (getattr(self, "description", None) or getattr(self, "background", None) or "").strip()
        if not desc:
            return f"({self.pk})"

        # Shorten and collapse whitespace, append ellipsis when trimmed.
        short = " ".join(desc.split())
        max_len = 50
        if len(short) > max_len:
            short = short[:max_len].rstrip() + "…"

        return f"{short} ({self.pk})"


class Insigne(EntityMixin, AbstractEntity, GenericModel, VersionMixin):
    """
    Model representing an insignia or badge.
    """

    label = models.CharField(max_length=255, verbose_name=_("Label"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Insigne")
        verbose_name_plural = _("Insigia")

    def __str__(self):
        return f"{self.label} ({self.pk})"


class PlaceCategory(GenericModel, SimpleLabelModel):
    """
    Z. B. Liegenschaft (Kaserne, Flugplatz, Kommandogebäude),
    Gedenkstätte, Erinnerungsort, Gemeinde, Stadt, Bundesland
    """

    description = models.TextField(blank=True, null=True)

    class Meta(SimpleLabelModel.Meta):
        verbose_name = _("Place Category")
        verbose_name_plural = _("Place Categories")


class Place(EntityMixin, E53_Place, AbstractEntity, VersionMixin):
    """
    Model representing a place.
    """

    event_site = models.BooleanField(default=False, verbose_name=_("Event Site"))
    memorial_site = models.BooleanField(default=False, verbose_name=_("Memorial Site"))
    alternative_name = models.TextField(blank=True, verbose_name=_("Other names"))
    kind = models.ManyToManyField(
        PlaceCategory,
        blank=True,
        verbose_name=_("Kind of Place"),
    )
    address = models.TextField(blank=True, null=True, verbose_name=_("Address"))
    place_history = models.TextField(blank=True, null=True, verbose_name=_("History"))
    role_present = models.TextField(
        blank=True, null=True, verbose_name=_("Current role")
    )
    role_past = models.TextField(blank=True, null=True, verbose_name=_("Past roles"))
    name_origin = models.TextField(
        blank=True, null=True, verbose_name=_("Origin of name")
    )

    class Meta(E53_Place.Meta):
        verbose_name = _("Place")
        verbose_name_plural = _("Places")


class Title(GenericModel, SimpleLabelModel):
    label_type = models.CharField(
        blank=True, null=True, max_length=255, verbose_name=_("Label Type")
    )
    abbreviation = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Abbreviation")
    )


class Honours(GenericModel, SimpleLabelModel):
    """Model representing an award or recognition."""

    class Meta(SimpleLabelModel.Meta):
        verbose_name = _("Honours")
        verbose_name_plural = _("Honours")


class Nobility(AbstractEntity, GenericModel, SimpleLabelModel, VersionMixin):
    class Meta(SimpleLabelModel.Meta):
        verbose_name = _("nobility")
        verbose_name_plural = _("nobilities")


class Person(EntityMixin, E21_Person, AbstractEntity, GenericModel, VersionMixin):
    class Meta(E21_Person.Meta):
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")

    class GenderChoices(models.TextChoices):
        MALE = "male", _("male")
        FEMALE = "female", _("female")

    # we override inherited fields to either disable or adapt them
    gender = models.CharField(
        blank=True,
        choices=GenderChoices,
        default="",
        max_length=4096,
        verbose_name=_("Gender"),
    )

    title = models.ManyToManyField(
        Title, blank=True, max_length=255, verbose_name=_("Title")
    )
    honours = models.ManyToManyField(
        blank=True, to=Honours, verbose_name=_("Honours"), editable=False
    )
    bionote = models.TextField(blank=True, null=True, verbose_name=_("bionote"))
    attended_military_basic_education = models.BooleanField(
        default=False, verbose_name=_("Attended military basic education")
    )


class HonoursEntity(
    SimpleLabelModel, DateMixin, AbstractEntity, GenericModel, VersionMixin
):
    """Model representing an award or recognition."""

    donour = models.ManyToManyField(Person, verbose_name=_("Donour"))
    purpose = models.TextField(blank=True, null=True, verbose_name=_("Purpose"))

    class Meta(SimpleLabelModel.Meta):
        verbose_name = _("Honours")
        verbose_name_plural = _("Honours")


class Bureau(EntityMixin, E74_Group, AbstractEntity, GenericModel, VersionMixin):
    """
    Model representing a bureau or group.
    """

    class Meta(E74_Group.Meta):
        verbose_name = _("Bureau")
        verbose_name_plural = _("Bureaus")


class RelationMixin(DateMixin, Relation, VersionMixin):
    notes = models.TextField(blank=True, null=True, verbose_name=_("Notes"))
    glossar_terms = models.ManyToManyField(
        Glossar, blank=True, verbose_name=_("Glossary terms")
    )

    class Meta:
        abstract = True
        ordering = ["pk"]


class PersonHasHonours(RelationMixin):
    """
    Relation between a person and an honour they received.
    """

    subj_model = Person
    obj_model = HonoursEntity
    in_relation_to = models.ForeignKey(
        Event,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("In relation to event"),
    )

    @classmethod
    def name(cls):
        return _("has honours")

    @classmethod
    def reverse_name(self):
        return _("is an honour of")


class EventOccuredAtPlace(RelationMixin):
    """
    Relation between an event and a place where it occurred.
    """

    subj_model = Event
    obj_model = Place

    @classmethod
    def name(cls):
        return _("occurred at")

    @classmethod
    def reverse_name(self):
        return _("place of occurence of")


class PersonBornInPlace(RelationMixin):
    """
    Relation between a person and a place where they were born.
    """

    subj_model = Person
    obj_model = Place

    @classmethod
    def name(cls):
        return _("born in")

    @classmethod
    def reverse_name(self):
        return _("place of birth of")


class PersonParentOf(RelationMixin):
    """
    Relation between a person and their child.
    """

    subj_model = Person
    obj_model = Person

    @classmethod
    def name(cls):
        return _("parent of")

    @classmethod
    def reverse_name(self):
        return _("child of")


class PersonSiblingOf(RelationMixin):
    """
    Relation between a person and their sibling.
    """

    subj_model = Person
    obj_model = Person

    @classmethod
    def name(cls):
        return _("sibling of")

    @classmethod
    def reverse_name(self):
        return _("sibling of")


class PersonPartnerOf(RelationMixin):
    """
    Relation between a person and their partner.
    """

    subj_model = Person
    obj_model = Person

    @classmethod
    def name(cls):
        return _("partner of")

    @classmethod
    def reverse_name(self):
        return _("partner of")


class PersonRelatedTo(RelationMixin):
    """
    Relation between a person and another person they are related to.
    This could be any kind of familial relationship.
    """

    subj_model = Person
    obj_model = Person

    @classmethod
    def name(cls):
        return _("related to")

    @classmethod
    def reverse_name(self):
        return _("related to")


class PersonDiedInPlace(RelationMixin):
    """Relation between a person and a place where they died."""

    subj_model = Person
    obj_model = Place

    @classmethod
    def name(cls):
        return _("died in")

    @classmethod
    def reverse_name(self):
        return _("place of death of")


class PersonActiveAtPlace(RelationMixin):
    """
    Relation between a person and a place where they were active.
    """

    subj_model = Person
    obj_model = Place

    @classmethod
    def name(cls):
        return _("active at")

    @classmethod
    def reverse_name(self):
        return _("place of activity of")


class PersonParticipatedInEvent(RelationMixin):
    """
    Relation between a person and an event they participated in.
    """

    subj_model = Person
    obj_model = Event

    @classmethod
    def name(cls):
        return _("participated in")

    @classmethod
    def reverse_name(self):
        return _("included as participant")


class BureauActiveAtPlace(RelationMixin):
    """
    Relation between a bureau and a place where it was active.
    """

    subj_model = Bureau
    obj_model = Place

    @classmethod
    def name(cls):
        return _("active at")

    @classmethod
    def reverse_name(self):
        return _("place of activity of")


class PersonWorkedForBureau(RelationMixin):
    """Relation between a person and a bureau they worked for."""

    subj_model = Person
    obj_model = Bureau

    @classmethod
    def name(cls):
        return _("worked for")

    @classmethod
    def reverse_name(self):
        return _("employed by")


class ImportantMomentInAnEvent(RelationMixin):
    """
    Relation between an event and a moment in that event.
    The order should be calculated based on the date;
    position field should be used only if the dates are unknown
    """

    class Meta(RelationMixin.Meta):
        ordering = ["position", "start_date_sort", "end_date_sort"]

    subj_model = Event
    obj_model = Event
    position = models.IntegerField(default=0, verbose_name=_("Position"))

    @classmethod
    def name(cls):
        return _("is an important moment in")

    @classmethod
    def reverse_name(self):
        return _("contains the moment")


class EventInvolvedBureau(RelationMixin):
    """
    Relation between an event and a bureau involved in it.
    """

    subj_model = Event
    obj_model = Bureau

    @classmethod
    def name(cls):
        return _("is relevant to")

    @classmethod
    def reverse_name(self):
        return _("is relevant for")


class InsigneLocatedAtPlace(RelationMixin):
    """
    Relation between an insigne and a place where it is located.
    """

    subj_model = Insigne
    obj_model = Place

    @classmethod
    def name(cls):
        return _("located at")

    @classmethod
    def reverse_name(self):
        return _("location of")


class InsignePossessedByBureau(RelationMixin):
    """
    Relation between an insigne and a bureau that possesses it.
    """

    subj_model = Insigne
    obj_model = Bureau

    @classmethod
    def name(cls):
        return _("belongs to")

    @classmethod
    def reverse_name(self):
        return _("owns")
