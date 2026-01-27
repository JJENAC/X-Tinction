"""Quick demo script to render population density on a map via the API.

Defaults target the Toulouse R4_C19 tile and the local FastAPI instance
(`docker compose up --scale api=6` for parallel queries). Adjust with CLI flags as needed.
"""

import argparse
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import requests

matplotlib.use("Agg")  # non-interactive backend for headless runs


def query_cell(api_url, lat, lon, timeout=5.0):
    """Query a single cell and return (lat, lon, density)."""
    try:
        resp = requests.get(api_url, params={"lat": lat, "lon": lon}, timeout=timeout)
        resp.raise_for_status()
        density = resp.json().get("density", 0.0)
        return (lat, lon, density)
    except Exception as e:
        print(f"Error querying ({lat}, {lon}): {e}")
        return (lat, lon, 0.0)


def build_density_map(api_url, lat_min, lat_max, lon_min, lon_max, step=0.001, timeout=5.0, max_workers=6):
    """Query the API on a lat/lon grid in parallel and return lats, lons, density matrix."""
    lats = np.arange(lat_min, lat_max, step)
    lons = np.arange(lon_min, lon_max, step)
    density = np.zeros((len(lats), len(lons)))

    # Create a flat list of all (lat, lon) pairs to query
    cells = [(i, j, lat, lon) for i, lat in enumerate(lats) for j, lon in enumerate(lons)]
    total_cells = len(cells)
    print(f"Querying {total_cells} cells with {max_workers} parallel workers...")

    # Use ThreadPoolExecutor for parallel requests
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(query_cell, api_url, lat, lon, timeout): (i, j)
            for i, j, lat, lon in cells
        }

        completed = 0
        for future in as_completed(futures):
            i, j = futures[future]
            lat_result, lon_result, dens = future.result()
            density[i, j] = dens
            completed += 1
            if completed % 100 == 0:
                print(f"  Progress: {completed}/{total_cells} cells")

    return lats, lons, density


def plot_density_map(lats, lons, density, title, output):
    output = Path(output)
    plt.figure(figsize=(8, 6))
    plt.imshow(
        density,
        extent=[lons.min(), lons.max(), lats.min(), lats.max()],
        origin="lower",
        cmap="hot",
        aspect="auto",
    )
    plt.colorbar(label="Population density (people/km²)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title(title)
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output, dpi=200)
    plt.close()
    return output


def main():
    parser = argparse.ArgumentParser(description="Render population density from the API")
    parser.add_argument("--api-url", default="http://localhost/density", help="Density endpoint URL")
    parser.add_argument("--lat-min", type=float, default=43.53, help="Min latitude (WGS84)")
    parser.add_argument("--lat-max", type=float, default=43.68, help="Max latitude (WGS84)")
    parser.add_argument("--lon-min", type=float, default=1.34, help="Min longitude (WGS84)")
    parser.add_argument("--lon-max", type=float, default=1.52, help="Max longitude (WGS84)")
    parser.add_argument("--step", type=float, default=0.001, help="Grid step in degrees (~0.001 ≈ 100 m)")
    parser.add_argument("--timeout", type=float, default=5.0, help="HTTP timeout seconds")
    parser.add_argument("--workers", type=int, default=6, help="Number of parallel workers")
    parser.add_argument("--output", default="outputs/density_toulouse.png", help="Output image path")

    args = parser.parse_args()

    start = time.perf_counter()
    lats, lons, density = build_density_map(
        api_url=args.api_url,
        lat_min=args.lat_min,
        lat_max=args.lat_max,
        lon_min=args.lon_min,
        lon_max=args.lon_max,
        step=args.step,
        timeout=args.timeout,
        max_workers=args.workers,
    )
    end = time.perf_counter()

    cells = round(((args.lat_max - args.lat_min) / args.step) * ((args.lon_max - args.lon_min) / args.step))
    print(f"Computed {cells} cells in {end - start:.2f} s ({cells / (end - start):.0f} cells/sec)")

    out_path = plot_density_map(lats, lons, density, "Population density – Toulouse", args.output)
    print(f"Saved map to {out_path}")


if __name__ == "__main__":
    main()
