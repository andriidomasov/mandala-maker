from PIL import Image, ImageDraw


def draw_petal(draw, center, size, stretch_factor, min_distance, fill=None):
    """Draw a single petal that will be rotated to create the mandala"""
    width = size // 2
    height = int(size * stretch_factor)

    left = center[0] - width // 2
    top = center[1] + min_distance
    right = center[0] + width // 2
    bottom = center[1] + height + min_distance

    draw.ellipse([left, top, right, bottom], outline='black', fill=fill, width=1)


# def draw_connecting_arcs(draw, center, radius, min_radius, segments):
#     """Draw decorative arcs between petals"""
#     for segment in range(segments):
#         # Calculate start and end angles for this segment
#         start_angle = 360 * segment / segments
#         end_angle = 360 * (segment + 1) / segments
#         mid_angle = (start_angle + end_angle) / 2
#
#         # Convert angles to radians for math calculations
#         mid_rad = math.radians(mid_angle)
#
#         # Calculate a random radius between min_radius and radius
#         arc_radius = random.uniform(min_radius, radius)
#
#         # Calculate arc center position
#         x = center[0] + arc_radius * math.cos(mid_rad)
#         y = center[1] + arc_radius * math.sin(mid_rad)
#
#         # Calculate random arc size (smaller than the gap between petals)
#         segment_width = 2 * math.pi * arc_radius / segments  # Width of one segment at this radius
#         max_arc_size = segment_width * 0.3  # Limit arc size to 30% of segment width
#         arc_size = random.uniform(max_arc_size * 0.5, max_arc_size)
#
#         # Draw the connecting arc
#         left = x - arc_size
#         top = y - arc_size
#         right = x + arc_size
#         bottom = y + arc_size
#
#         # Calculate arc angles to stay within segment bounds
#         max_span = (360 / segments) * 0.4  # 40% of segment angle
#         arc_span = random.uniform(20, max_span)
#         arc_start = mid_angle - arc_span/2
#         arc_end = mid_angle + arc_span/2
#
#         draw.arc([left, top, right, bottom], arc_start, arc_end, fill='black', width=1)

def generate_mandala(size=1600, segments=16, petal_configs=None, fill_petals=False):
    # Create a larger image for antialiasing
    scale_factor = 2  # Back to original scale factor
    large_size = size * scale_factor

    # Create a new white image at larger size
    image = Image.new('RGB', (large_size, large_size), 'white')
    draw = ImageDraw.Draw(image)

    # Calculate center point of larger image
    center = (large_size // 2, large_size // 2)

    # Use default petal configurations if none provided
    if petal_configs is None:
        petal_configs = [
            {"size": large_size * 0.10, "stretch": 1.4, "min_dist": large_size * 0.20},
            {"size": large_size * 0.12, "stretch": 1.3, "min_dist": large_size * 0.10},
            {"size": large_size * 0.10, "stretch": 1.2, "min_dist": large_size * 0.08},
            {"size": large_size * 0.08, "stretch": 1.1, "min_dist": large_size * 0.05}
        ]

    # Draw a simple circle in the center
    center_radius = int(large_size * 0.02)
    draw.ellipse([
        center[0] - center_radius,
        center[1] - center_radius,
        center[0] + center_radius,
        center[1] + center_radius
    ], outline='black', width=2)

    # Draw all petals
    for config in petal_configs:
        petal_layer = Image.new('RGBA', (large_size, large_size), (0, 0, 0, 0))
        petal_draw = ImageDraw.Draw(petal_layer)

        draw_petal(petal_draw,
                   center,
                   config["size"],
                   config["stretch"],
                   config["min_dist"],
                   fill='white' if fill_petals else None)

        for segment in range(segments):
            angle = 360 * segment / segments
            rotated_petal = petal_layer.rotate(angle, center=center, expand=False)
            image.paste(rotated_petal, (0, 0), rotated_petal)

    # Simple single-step resize with antialiasing
    final_image = image.resize((size, size), Image.Resampling.LANCZOS)
    return final_image