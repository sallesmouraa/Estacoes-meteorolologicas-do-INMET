import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT_CSV = ROOT / "br_inmet_bdmep_estacao.csv"
OUTPUT_CSV = ROOT / "br_inmet_bdmep_estacao_clean.csv"

POINT_RE = re.compile(r"^POINT\(([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\)$")


def parse_point(value: str):
    if not value:
        return "", ""
    m = POINT_RE.match(value.strip())
    if not m:
        return "", ""
    latitude = m.group(1)
    longitude = m.group(2)
    return latitude, longitude


def normalize_altitude(value: str):
    if value is None:
        return "NA"
    stripped = value.strip()
    return stripped if stripped else "NA"


def clean():
    with INPUT_CSV.open("r", encoding="utf-8", newline="") as f_in, OUTPUT_CSV.open(
        "w", encoding="utf-8", newline=""
    ) as f_out:
        reader = csv.DictReader(f_in)

        fieldnames = list(reader.fieldnames or [])
        if "latitude" not in fieldnames:
            fieldnames.append("latitude")
        if "longitude" not in fieldnames:
            fieldnames.append("longitude")

        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            row["altitude"] = normalize_altitude(row.get("altitude", ""))
            lat, lon = parse_point((row.get("geolocalizacao") or "").strip())
            row["latitude"] = lat
            row["longitude"] = lon
            writer.writerow(row)

    print(f"Arquivo limpo gerado em: {OUTPUT_CSV}")


if __name__ == "__main__":
    clean()
