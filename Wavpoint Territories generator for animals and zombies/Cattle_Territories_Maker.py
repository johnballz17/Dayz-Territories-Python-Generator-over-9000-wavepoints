from pathlib import Path

INPUT_FILE = "input.txt"
OUTPUT_FILE = "cattle_territories.xml"

TERRITORY_COLOR = 864420070

# Pattern for each 5-point territory block
ZONE_PATTERN = [
    ("Rest", 90),
    ("Graze", 195),
    ("Graze", 150),
    ("Rest", 82.5),
    ("Water", 90),
]

SMIN = 0
SMAX = 0
DMIN = 0
DMAX = 0


def parse_line(line: str):
    """
    Parse a line like:
    SodaCan_Pipsi|5920.674316 269.325012 10255.281250|0.000000 0.000000 -0.000000

    Returns:
        tuple[float, float] -> (x, z)
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
        x = float(coords[0])
        z = float(coords[2])
        return x, z
    except ValueError:
        return None


def format_num(value: float) -> str:
    """
    Keep decimals but remove unnecessary trailing zeros.
    """
    text = f"{value:.2f}"
    text = text.rstrip("0").rstrip(".")
    return text


def make_zone_xml(zone_name: str, x: float, z: float, radius: float) -> str:
    return (
        f'        <zone name="{zone_name}" '
        f'smin="{SMIN}" smax="{SMAX}" '
        f'dmin="{DMIN}" dmax="{DMAX}" '
        f'x="{format_num(x)}" z="{format_num(z)}" r="{format_num(radius)}"/>'
    )


def chunk_list(items, chunk_size):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]


def build_territory_block(points):
    lines = [f'<territory color="{TERRITORY_COLOR}">']

    for (zone_name, radius), (x, z) in zip(ZONE_PATTERN, points):
        lines.append(make_zone_xml(zone_name, x, z, radius))

    lines.append("</territory>")
    return "\n".join(lines)


def main():
    input_path = Path(INPUT_FILE)
    output_path = Path(OUTPUT_FILE)

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return

    points = []

    with input_path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            parsed = parse_line(line)
            if parsed is None:
                print(f"Skipping invalid line {line_number}: {line.strip()}")
                continue
            points.append(parsed)

    if not points:
        print("No valid points found.")
        return

    pattern_size = len(ZONE_PATTERN)
    territory_blocks = []

    for group in chunk_list(points, pattern_size):
        if len(group) < pattern_size:
            print(f"Skipping incomplete group of {len(group)} point(s) at end of file.")
            break
        territory_blocks.append(build_territory_block(group))

    final_output = "\n\n".join(territory_blocks)

    with output_path.open("w", encoding="utf-8") as f:
        f.write(final_output)

    print(f"Done. Wrote {len(territory_blocks)} cattle territory block(s).")
    print(f"Output saved to: {output_path}")


if __name__ == "__main__":
    main()