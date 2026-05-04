from apis_core.generic.tables import GenericTable
from apis_core.relations.tables import RelationsListTable

import django_tables2 as tables


class EntityMixinRelationsTable(RelationsListTable):
    start = tables.Column(accessor="start")
    end = tables.Column(accessor="end")
    notes = tables.Column(accessor="notes")

    class Meta(GenericTable.Meta):
        per_page = 1000
        sequence = ("relation", "...", "actions")


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
