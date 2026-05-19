from django.db import migrations, models


def forwards(apps, schema_editor):
    Person = apps.get_model("apis_ontology", "Person")
    for p in Person.objects.all():
        parts = []
        for fname in [
            "qualification",
            "career",
            "controversies",
            "achievements",
            "anecdotes",
        ]:
            val = getattr(p, fname, None)
            if val:
                v = val.strip()
                if v:
                    parts.append(v)
        if parts:
            p.bionote = "\n\n".join(parts)
            p.save(update_fields=["bionote"])

    # Also migrate data for historical/version model if present
    try:
        VersionPerson = apps.get_model("apis_ontology", "VersionPerson")
    except LookupError:
        VersionPerson = None

    if VersionPerson is not None:
        for vp in VersionPerson.objects.all():
            parts = []
            for fname in [
                "qualification",
                "career",
                "controversies",
                "achievements",
                "anecdotes",
            ]:
                val = getattr(vp, fname, None)
                if val:
                    v = val.strip()
                    if v:
                        parts.append(v)
            if parts:
                vp.bionote = "\n\n".join(parts)
                vp.save(update_fields=["bionote"])


class Migration(migrations.Migration):

    dependencies = [
        ("apis_ontology", "0011_insignelocatedatplace_insignepossessedbybureau_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="bionote",
            field=models.TextField(blank=True, null=True, verbose_name="bionote"),
        ),
        migrations.AddField(
            model_name="versionperson",
            name="bionote",
            field=models.TextField(blank=True, null=True, verbose_name="bionote"),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
        migrations.RemoveField(model_name="person", name="qualification"),
        migrations.RemoveField(model_name="person", name="career"),
        migrations.RemoveField(model_name="person", name="controversies"),
        migrations.RemoveField(model_name="person", name="achievements"),
        migrations.RemoveField(model_name="person", name="anecdotes"),
        migrations.RemoveField(model_name="versionperson", name="qualification"),
        migrations.RemoveField(model_name="versionperson", name="career"),
        migrations.RemoveField(model_name="versionperson", name="controversies"),
        migrations.RemoveField(model_name="versionperson", name="achievements"),
        migrations.RemoveField(model_name="versionperson", name="anecdotes"),
    ]
