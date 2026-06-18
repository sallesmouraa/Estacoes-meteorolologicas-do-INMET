import csv
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT_CSV = ROOT / "br_inmet_bdmep_estacao_clean.csv"
REPORT_DIR = ROOT / "reports"
REPORT_PATH = REPORT_DIR / "data_quality_report.md"

POINT_RE = re.compile(r"^POINT\(([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\)$")


def is_valid_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except Exception:
        return False


def to_float(value: str):
    try:
        return float(value)
    except Exception:
        return None


def validate():
    if not INPUT_CSV.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {INPUT_CSV}. Rode scripts/clean_data.py primeiro."
        )

    total_rows = 0
    missing_altitude = 0
    invalid_dates = []
    invalid_points = []
    out_of_range_coords = []
    empty_required = []

    id_estacao_values = []

    with INPUT_CSV.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):  # header is line 1
            total_rows += 1

            id_estacao = (row.get("id_estacao") or "").strip()
            estacao = (row.get("estacao") or "").strip()
            data_fundacao = (row.get("data_fundacao") or "").strip()
            geolocalizacao = (row.get("geolocalizacao") or "").strip()
            altitude = (row.get("altitude") or "").strip()
            latitude = (row.get("latitude") or "").strip()
            longitude = (row.get("longitude") or "").strip()

            if id_estacao:
                id_estacao_values.append(id_estacao)

            # Required fields check
            required = {
                "id_municipio": (row.get("id_municipio") or "").strip(),
                "id_estacao": id_estacao,
                "estacao": estacao,
                "data_fundacao": data_fundacao,
                "geolocalizacao": geolocalizacao,
            }
            missing_required = [k for k, v in required.items() if not v]
            if missing_required:
                empty_required.append((i, missing_required))

            # Altitude NA check
            if altitude == "NA":
                missing_altitude += 1

            # Date format
            if data_fundacao and not is_valid_date(data_fundacao):
                invalid_dates.append((i, data_fundacao))

            # POINT format + range
            m = POINT_RE.match(geolocalizacao)
            if not m:
                invalid_points.append((i, geolocalizacao))
            else:
                lat = to_float(m.group(1))
                lon = to_float(m.group(2))
                if lat is None or lon is None:
                    invalid_points.append((i, geolocalizacao))
                else:
                    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                        out_of_range_coords.append((i, lat, lon))

                # consistency with derived columns
                dlat = to_float(latitude)
                dlon = to_float(longitude)
                if dlat is None or dlon is None:
                    out_of_range_coords.append((i, latitude, longitude))
                else:
                    if not (-90 <= dlat <= 90 and -180 <= dlon <= 180):
                        out_of_range_coords.append((i, dlat, dlon))

    id_counts = Counter(id_estacao_values)
    duplicate_ids = sorted([k for k, v in id_counts.items() if v > 1])

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    with REPORT_PATH.open("w", encoding="utf-8") as out:
        out.write("# Relatório de Qualidade dos Dados\n\n")
        out.write(f"Arquivo analisado: `{INPUT_CSV.name}`\n\n")
        out.write(f"Total de linhas: **{total_rows}**\n")
        out.write(f"Altitudes marcadas como `NA`: **{missing_altitude}**\n")
        out.write(f"IDs de estação duplicados: **{len(duplicate_ids)}**\n")
        out.write(f"Datas inválidas: **{len(invalid_dates)}**\n")
        out.write(f"Geolocalizações inválidas: **{len(invalid_points)}**\n")
        out.write(f"Coordenadas fora de faixa/derivadas inválidas: **{len(out_of_range_coords)}**\n")
        out.write(f"Linhas com campos obrigatórios vazios: **{len(empty_required)}**\n\n")

        if duplicate_ids:
            out.write("## IDs de estação duplicados\n")
            for _id in duplicate_ids:
                out.write(f"- `{_id}` ({id_counts[_id]} ocorrências)\n")
            out.write("\n")

        if invalid_dates:
            out.write("## Datas inválidas (linha, valor)\n")
            for line_no, value in invalid_dates[:100]:
                out.write(f"- {line_no}: `{value}`\n")
            out.write("\n")

        if invalid_points:
            out.write("## Geolocalizações inválidas (linha, valor)\n")
            for line_no, value in invalid_points[:100]:
                out.write(f"- {line_no}: `{value}`\n")
            out.write("\n")

        if out_of_range_coords:
            out.write("## Coordenadas fora de faixa/derivadas inválidas (linha, lat, lon)\n")
            for item in out_of_range_coords[:100]:
                out.write(f"- {item[0]}: `{item[1]}`, `{item[2]}`\n")
            out.write("\n")

        if empty_required:
            out.write("## Campos obrigatórios vazios (linha, campos)\n")
            for line_no, fields in empty_required[:100]:
                out.write(f"- {line_no}: {', '.join(fields)}\n")
            out.write("\n")

    print(f"Relatório gerado em: {REPORT_PATH}")


if __name__ == "__main__":
    validate()
