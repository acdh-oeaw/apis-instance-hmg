from apis_core.generic.tables import GenericTable

import django_tables2 as tables


class EntityMixinRelationsTable(GenericTable):
    start = tables.Column(accessor="start")
    end = tables.Column(accessor="end")
    # glossary = tables.Column(accessor="glossar_terms")
    notes = tables.Column(accessor="notes")

    class Meta(GenericTable.Meta):
        per_page = 1000
        sequence = ("desc", "...", "actions")


class GenericListViewTable(GenericTable):
    class Meta(GenericTable.Meta):
        attrs = {
            "td": {"class": "preserve-linebreaks"},
        }
        sequence = (
            "id",
            "desc",
            "...",
            "actions",
        )


class EntityMixinTable(GenericListViewTable):
    pass


class RelationMixinTable(GenericListViewTable):
    pass
