from django.db import migrations


def forwards(apps, schema_editor):
    Honours = apps.get_model("apis_ontology", "Honours")
    HonoursEntity = apps.get_model("apis_ontology", "HonoursEntity")

    # Determine concrete, non-M2M field names present on both models (excluding PK)
    src_fields = [
        f.name
        for f in Honours._meta.get_fields()
        if getattr(f, "concrete", False) and not getattr(f, "many_to_many", False)
    ]
    tgt_fields = {
        f.name
        for f in HonoursEntity._meta.get_fields()
        if getattr(f, "concrete", False) and not getattr(f, "many_to_many", False)
    }

    common_fields = [n for n in src_fields if n in tgt_fields and n != "id"]

    for src in Honours.objects.all():
        data = {name: getattr(src, name) for name in common_fields}
        HonoursEntity.objects.create(**data)


def reverse(apps, schema_editor):
    Honours = apps.get_model("apis_ontology", "Honours")
    HonoursEntity = apps.get_model("apis_ontology", "HonoursEntity")

    labels = list(Honours.objects.values_list("label", flat=True))
    if labels:
        HonoursEntity.objects.filter(label__in=labels).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("apis_ontology", "0015_honoursentity_versionhonoursentity_and_more"),
    ]

    operations = [
        migrations.RunPython(forwards, reverse),
    ]
