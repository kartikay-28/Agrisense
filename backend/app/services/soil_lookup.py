"""
Soil type lookup from a static lat/lon → soil_type dataset.

In production: load a GeoJSON or CSV with soil zones.
For MVP: rule-based approximation by Indian state/region.
"""

# Rough soil type mapping by lat bands (India-specific)
# You can replace this with a proper soil dataset CSV later
SOIL_ZONES = [
    {"lat_min": 30.0, "lat_max": 36.0, "lon_min": 74.0, "lon_max": 80.0, "soil": "Alluvial"},   # Punjab/HP
    {"lat_min": 26.0, "lat_max": 30.0, "lon_min": 76.0, "lon_max": 84.0, "soil": "Alluvial"},   # UP/Haryana
    {"lat_min": 18.0, "lat_max": 26.0, "lon_min": 73.0, "lon_max": 80.0, "soil": "Black"},      # Maharashtra/MP
    {"lat_min": 8.0,  "lat_max": 18.0, "lon_min": 76.0, "lon_max": 80.0, "soil": "Red Laterite"}, # South India
    {"lat_min": 22.0, "lat_max": 28.0, "lon_min": 68.0, "lon_max": 74.0, "soil": "Arid/Desert"}, # Rajasthan
]


def get_soil_type(lat: float, lon: float) -> str:
    """
    Return approximate soil type for given coordinates.
    """
    for zone in SOIL_ZONES:
        if (zone["lat_min"] <= lat <= zone["lat_max"] and
                zone["lon_min"] <= lon <= zone["lon_max"]):
            return zone["soil"]
    return "Loamy"  # default
