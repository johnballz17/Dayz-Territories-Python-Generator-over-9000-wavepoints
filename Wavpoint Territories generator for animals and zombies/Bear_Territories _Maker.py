import math
from pathlib import Path

INPUT_FILE = "input.txt"
OUTPUT_FILE = "graze_zones.xml"

# How many zones per territory block
ZONES_PER_TERRITORY = 6

# Default radius for each zone
DEFAULT_RADIUS = 150

# Territory color
TERRITORY_COLOR = 4294923520

# Zone settings
ZONE_NAME = "Graze"
SMIN = 0
SMAX = 0
DMIN = 0
DMAX = 0


def parse_line(line: str):
    """
    Parse a line like:
    SodaCan_Pipsi|5920.674316 269.325012 10255.281250|0.000000 0.000000 -0.000000

    Returns:
        tuple[int, int] -> (x, z)
    """
    line = line.strip()
    if not line:
        return None

    parts = line.split("|")
    if len(parts) < 2:
        return None

    coords = parts[1].split()
    if len(coords) < 3:
        return None

    try:
        x = round(float(coords[0]))
        z = round(float(coords[2]))
        return x, z
    except ValueError:
        return None


def make_zone_xml(x: int, z: int, radius: int = DEFAULT_RADIUS) -> str:
    return (
        f'        <zone name="{ZONE_NAME}" '
        f'smin="{SMIN}" smax="{SMAX}" '
        f'dmin="{DMIN}" dmax="{DMAX}" '
        f'x="{x}" z="{z}" r="{radius}"/>'
    )


def chunk_list(items, chunk_size):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]


def build_territory_block(zones, color=TERRITORY_COLOR):
    lines = [f'<territory color="{color}">']
    lines.extend(zones)
    lines.append("</territory>")
    return "\n".join(lines)


def main():
    input_path = Path(INPUT_FILE)
    output_path = Path(OUTPUT_FILE)

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return

    parsed_points = []

    with input_path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            parsed = parse_line(line)
            if parsed is None:
                print(f"Skipping invalid line {line_number}: {line.strip()}")
                continue
            parsed_points.append(parsed)

    if not parsed_points:
        print("No valid points found.")
        return

    all_blocks = []

    for group in chunk_list(parsed_points, ZONES_PER_TERRITORY):
        zone_lines = [make_zone_xml(x, z) for x, z in group]
        block = build_territory_block(zone_lines)
        all_blocks.append(block)

    final_output = "\n\n".join(all_blocks)

    with output_path.open("w", encoding="utf-8") as f:
        f.write(final_output)

    print(f"Done. Wrote {len(parsed_points)} zones into {len(all_blocks)} territory blocks.")
    print(f"Output saved to: {output_path}")


if __name__ == "__main__":
    main()