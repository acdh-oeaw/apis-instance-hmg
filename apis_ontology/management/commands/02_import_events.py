import unicodedata
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apis_ontology.models import Event


def _strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


MONTH_MAP = {
    "JANUAR": 1,
    "JANNER": 1,
    "JAN": 1,
    "FEBRUAR": 2,
    "FEB": 2,
    "MAERZ": 3,
    "MARZ": 3,
    "MAER": 3,
    "MÄRZ": 3,
    "MÄR": 3,
    "APRIL": 4,
    "APR": 4,
    "MAI": 5,
    "JUNI": 6,
    "JULI": 7,
    "AUGUST": 8,
    "SEPTEMBER": 9,
    "OKTOBER": 10,
    "NOVEMBER": 11,
    "DEZEMBER": 12,
}


class Command(BaseCommand):
    help = "Import events from a CSV file. Usage: manage.py import_events /path/to/file.csv"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", help="Path to input CSV file")

    def handle(self, *args, **options):
        csv_path = Path(options["csv_file"]).expanduser()
        if not csv_path.exists():
            self.stderr.write(f"File not found: {csv_path}")
            return

        out_path = csv_path.with_name(csv_path.stem + "_imported" + csv_path.suffix)

        # read with pandas, keep empty strings (no NaN for empty cells)
        df = pd.read_csv(csv_path, dtype=str, keep_default_na=False, delimiter=";")

        # ensure columns exist
        for col in ("day", "month", "year", "description"):
            if col not in df.columns:
                df[col] = ""

        # add result columns
        df["status"] = ""
        df["pk"] = ""
        df["comments"] = ""

        for idx in tqdm(df.index, desc="Importing rows"):
            row = df.loc[idx]
            try:
                day_raw = (row.get("day") or "").strip()
                month_raw = (row.get("month") or "").strip()
                year_raw = (row.get("year") or "").strip()
                description = (row.get("description") or "").strip()

                if not year_raw:
                    raise ValueError("Missing year")

                month_num = None
                if month_raw:
                    norm = _strip_accents(month_raw).upper()
                    norm = norm.replace(".", "")
                    month_num = MONTH_MAP.get(norm)
                    if month_num is None:
                        for k in MONTH_MAP:
                            if norm.startswith(k):
                                month_num = MONTH_MAP[k]
                                break

                y = int(year_raw)
                d = int(day_raw) if day_raw else 1
                if month_num is None:
                    month_num = 1

                date_str = f"{y:04d}-{month_num:02d}-{d:02d}"
                label = description[:255] if description else None
                if len(description) > 255:
                    label += "..."
                with transaction.atomic():
                    ev = Event.objects.create(start=date_str, description=description, label=label)

                df.at[idx, "status"] = "OK"
                df.at[idx, "pk"] = str(ev.pk)
                df.at[idx, "comments"] = ""

            except Exception as e:
                df.at[idx, "status"] = "FAIL"
                df.at[idx, "pk"] = ""
                df.at[idx, "comments"] = str(e)

        # write output CSV next to input file
        df.to_csv(out_path, index=False, encoding="utf-8-sig")

        self.stdout.write(self.style.SUCCESS(f"Processed {len(df)} rows"))
        self.stdout.write(f"Output written to: {out_path}")
