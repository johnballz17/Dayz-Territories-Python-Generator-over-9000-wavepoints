from pathlib import Path

INPUT_FILE = "input.txt"
OUTPUT_FILE = "mixed_zombie_territories.xml"

# How many zones each territory should contain
ZONES_PER_TERRITORY = 6

# Territory templates:
# Each territory block will use ONE of these zombie types for all zones in that block,
# then move to the next template for the next territory.
TERRITORY_TYPES = [
    {
        "color": 3014176010,
        "zone_name": "InfectedCity",
        "smin": 0,
        "smax": 0,
        "dmin": 3,
        "dmax": 5,
        "radius": 50,
    },
    {
        "color": 1124502272,
        "zone_name": "InfectedArmy",
        "smin": 0,
        "smax": 0,
        "dmin": 5,
        "dmax": 8,
        "radius": 80,
    },
    {
        "color": 2615190015,
        "zone_name": "InfectedIndustrial",
        "smin": 0,
        "smax": 0,
        "dmin": 5,
        "dmax": 8,
        "radius": 80,
    },
    {
        "color": 2193199729,
        "zone_name": "InfectedVillageTier1",
        "smin": 0,
        "smax": 0,
        "dmin": 4,
        "dmax": 8,
        "radius": 80,
    },
    {
        "color": 2387830984,
        "zone_name": "InfectedMedic",
        "smin": 0,
        "smax": 0,
        "dmin": 3,
        "dmax": 5,
        "radius": 50,
    },
    {
        "color": 4287731209,
        "zone_name": "InfectedCityTier1",
        "smin": 0,
        "smax": 0,
        "dmin": 4,
        "dmax": 6,
        "radius": 70,
    },
]


def parse_line(line: str):
    """
    Parse lines like:
    SodaCan_Pipsi|5920.674316 269.325012 10255.281250|0.000000 0.000000 -0.000000

    Returns:
        (x, z) as floats
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
    text = f"{value:.2f}"
    return text.rstrip("0").rstrip(".")


def make_zone_xml(x: float, z: float, template: dict) -> str:
    return (
        f'        <zone name="{template["zone_name"]}" '
        f'smin="{template["smin"]}" '
        f'smax="{template["smax"]}" '
        f'dmin="{template["dmin"]}" '
        f'dmax="{template["dmax"]}" '
        f'x="{format_num(x)}" '
        f'z="{format_num(z)}" '
        f'r="{format_num(template["radius"])}"/>'
    )


def chunk_list(items, chunk_size):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]


def build_territory_block(points, template):
    lines = [f'<territory color="{template["color"]}">']

    for x, z in points:
        lines.append(make_zone_xml(x, z, template))

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

    territory_blocks = []
    territory_index = 0

    for group in chunk_list(points, ZONES_PER_TERRITORY):
        if not group:
            continue

        template = TERRITORY_TYPES[territory_index % len(TERRITORY_TYPES)]
        territory_blocks.append(build_territory_block(group, template))
        territory_index += 1

    final_output = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<territory-type>\n"
        + "\n\n".join(territory_blocks)
        + "\n</territory-type>\n"
    )

    with output_path.open("w", encoding="utf-8") as f:
        f.write(final_output)

    print(f"Done. Wrote {len(territory_blocks)} mixed zombie territory block(s).")
    print(f"Output saved to: {output_path}")


if __name__ == "__main__":
    main()