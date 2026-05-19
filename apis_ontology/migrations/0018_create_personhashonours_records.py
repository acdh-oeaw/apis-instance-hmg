from django.db import migrations


def forwards(apps, schema_editor):
    Person = apps.get_model("apis_ontology", "Person")
    Honours = apps.get_model("apis_ontology", "Honours")
    HonoursEntity = apps.get_model("apis_ontology", "HonoursEntity")
    PersonHasHonours = apps.get_model("apis_ontology", "PersonHasHonours")
    ContentType = apps.get_model("contenttypes", "ContentType")

    try:
        ct_person = ContentType.objects.get(app_label="apis_ontology", model="person")
        ct_honoursentity = ContentType.objects.get(app_label="apis_ontology", model="honoursentity")
    except ContentType.DoesNotExist:
        return

    # Map honours -> honoursentity by label (created in migration 0016)
    label_map = {he.label: he for he in HonoursEntity.objects.all()}

    for person in Person.objects.all():
        # iterate M2M honours on Person (Honours instances)
        for h in person.honours.all():
            he = label_map.get(getattr(h, "label", None))
            if not he:
                # fallback: try to find by label in DB
                he = HonoursEntity.objects.filter(label=getattr(h, "label", None)).first()
            if not he:
                continue

            # create relation record linking person -> honoursentity
            PersonHasHonours.objects.create(
                subj_content_type=ct_person,
                subj_object_id=person.pk,
                obj_content_type=ct_honoursentity,
                obj_object_id=he.pk,
            )


def reverse(apps, schema_editor):
    PersonHasHonours = apps.get_model("apis_ontology", "PersonHasHonours")
    ContentType = apps.get_model("contenttypes", "ContentType")

    try:
        ct_person = ContentType.objects.get(app_label="apis_ontology", model="person")
        ct_honoursentity = ContentType.objects.get(app_label="apis_ontology", model="honoursentity")
    except ContentType.DoesNotExist:
        return

    PersonHasHonours.objects.filter(
        subj_content_type=ct_person, obj_content_type=ct_honoursentity
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("apis_ontology", "0017_personhashonours_versionpersonhashonours_and_more"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("relations", "0003_relation_relations_r_subj_content_type_and_more"),
    ]

    operations = [
        migrations.RunPython(forwards, reverse),
    ]
