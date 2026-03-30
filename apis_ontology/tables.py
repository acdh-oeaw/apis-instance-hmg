from apis_core.generic.tables import GenericTable

import django_tables2 as tables


class EntityMixinRelationsTable(GenericTable):
    start = tables.Column(accessor="start")
    end = tables.Column(accessor="end")
    # glossary = tables.Column(accessor="glossar_terms")
    notes = tables.Column(accessor="notes")

    class Meta(GenericTable.Meta):
        exclude = ["noduplicate"]
        per_page = 1000
        sequence = (
            "desc",
            "...",
            "view",
            "edit",
            "delete",
        )
