# Generate Population Density Maps for Major Cities

Copy-paste these commands to generate maps using the deployed OpenShift API.

## Europe

### Paris, France
```bash
python dynamic_pop_density.py --lat-min 48.78 --lat-max 48.95 --lon-min 2.25 --lon-max 2.50 --output outputs/density_paris.png --workers 12
```

### London, UK
```bash
python dynamic_pop_density.py --lat-min 51.38 --lat-max 51.62 --lon-min -0.35 --lon-max 0.15 --output outputs/density_london.png --workers 12
```

### Berlin, Germany
```bash
python dynamic_pop_density.py --lat-min 52.40 --lat-max 52.62 --lon-min 13.24 --lon-max 13.54 --output outputs/density_berlin.png --workers 12
```

### Madrid, Spain
```bash
python dynamic_pop_density.py --lat-min 40.32 --lat-max 40.52 --lon-min -3.82 --lon-max -3.52 --output outputs/density_madrid.png --workers 12
```

### Rome, Italy
```bash
python dynamic_pop_density.py --lat-min 41.78 --lat-max 42.00 --lon-min 12.38 --lon-max 12.62 --output outputs/density_rome.png --workers 12
```

### Amsterdam, Netherlands
```bash
python dynamic_pop_density.py --lat-min 52.30 --lat-max 52.42 --lon-min 4.78 --lon-max 4.98 --output outputs/density_amsterdam.png --workers 12
```

### Barcelona, Spain
```bash
python dynamic_pop_density.py --lat-min 41.32 --lat-max 41.48 --lon-min 2.08 --lon-max 2.24 --output outputs/density_barcelona.png --workers 12
```

### Vienna, Austria
```bash
python dynamic_pop_density.py --lat-min 48.14 --lat-max 48.28 --lon-min 16.28 --lon-max 16.48 --output outputs/density_vienna.png --workers 12
```

## North America

### New York, USA
```bash
python dynamic_pop_density.py --lat-min 40.60 --lat-max 40.85 --lon-min -74.05 --lon-max -73.80 --output outputs/density_newyork.png --workers 12
```

### Los Angeles, USA
```bash
python dynamic_pop_density.py --lat-min 33.95 --lat-max 34.15 --lon-min -118.40 --lon-max -118.15 --output outputs/density_losangeles.png --workers 12
```

### Chicago, USA
```bash
python dynamic_pop_density.py --lat-min 41.78 --lat-max 41.98 --lon-min -87.75 --lon-max -87.55 --output outputs/density_chicago.png --workers 12
```

### Mexico City, Mexico
```bash
python dynamic_pop_density.py --lat-min 19.30 --lat-max 19.50 --lon-min -99.25 --lon-max -99.00 --output outputs/density_mexicocity.png --workers 12
```

### Toronto, Canada
```bash
python dynamic_pop_density.py --lat-min 43.60 --lat-max 43.78 --lon-min -79.50 --lon-max -79.25 --output outputs/density_toronto.png --workers 12
```

## Asia

### Tokyo, Japan
```bash
python dynamic_pop_density.py --lat-min 35.60 --lat-max 35.75 --lon-min 139.65 --lon-max 139.85 --output outputs/density_tokyo.png --workers 12
```

### Shanghai, China
```bash
python dynamic_pop_density.py --lat-min 31.15 --lat-max 31.35 --lon-min 121.35 --lon-max 121.60 --output outputs/density_shanghai.png --workers 12
```

### Beijing, China
```bash
python dynamic_pop_density.py --lat-min 39.85 --lat-max 40.00 --lon-min 116.30 --lon-max 116.50 --output outputs/density_beijing.png --workers 12
```

### Mumbai, India
```bash
python dynamic_pop_density.py --lat-min 18.90 --lat-max 19.15 --lon-min 72.80 --lon-max 73.00 --output outputs/density_mumbai.png --workers 12
```

### Delhi, India
```bash
python dynamic_pop_density.py --lat-min 28.50 --lat-max 28.75 --lon-min 77.10 --lon-max 77.35 --output outputs/density_delhi.png --workers 12
```

### Singapore
```bash
python dynamic_pop_density.py --lat-min 1.25 --lat-max 1.42 --lon-min 103.70 --lon-max 103.90 --output outputs/density_singapore.png --workers 12
```

### Seoul, South Korea
```bash
python dynamic_pop_density.py --lat-min 37.48 --lat-max 37.62 --lon-min 126.90 --lon-max 127.10 --output outputs/density_seoul.png --workers 12
```

### Bangkok, Thailand
```bash
python dynamic_pop_density.py --lat-min 13.68 --lat-max 13.85 --lon-min 100.48 --lon-max 100.65 --output outputs/density_bangkok.png --workers 12
```

## Middle East

### Dubai, UAE
```bash
python dynamic_pop_density.py --lat-min 25.15 --lat-max 25.30 --lon-min 55.20 --lon-max 55.40 --output outputs/density_dubai.png --workers 12
```

### Istanbul, Turkey
```bash
python dynamic_pop_density.py --lat-min 40.98 --lat-max 41.12 --lon-min 28.92 --lon-max 29.12 --output outputs/density_istanbul.png --workers 12
```

### Tel Aviv, Israel
```bash
python dynamic_pop_density.py --lat-min 32.04 --lat-max 32.12 --lon-min 34.76 --lon-max 34.84 --output outputs/density_telaviv.png --workers 12
```

## South America

### São Paulo, Brazil
```bash
python dynamic_pop_density.py --lat-min -23.65 --lat-max -23.45 --lon-min -46.75 --lon-max -46.55 --output outputs/density_saopaulo.png --workers 12
```

### Buenos Aires, Argentina
```bash
python dynamic_pop_density.py --lat-min -34.70 --lat-max -34.52 --lon-min -58.52 --lon-max -58.32 --output outputs/density_buenosaires.png --workers 12
```

### Rio de Janeiro, Brazil
```bash
python dynamic_pop_density.py --lat-min -23.00 --lat-max -22.82 --lon-min -43.30 --lon-max -43.10 --output outputs/density_rio.png --workers 12
```

## Africa

### Cairo, Egypt
```bash
python dynamic_pop_density.py --lat-min 29.98 --lat-max 30.12 --lon-min 31.20 --lon-max 31.38 --output outputs/density_cairo.png --workers 12
```

### Lagos, Nigeria
```bash
python dynamic_pop_density.py --lat-min 6.42 --lat-max 6.52 --lon-min 3.32 --lon-max 3.44 --output outputs/density_lagos.png --workers 12
```

### Johannesburg, South Africa
```bash
python dynamic_pop_density.py --lat-min -26.30 --lat-max -26.10 --lon-min 27.95 --lon-max 28.15 --output outputs/density_johannesburg.png --workers 12
```

## Oceania

### Sydney, Australia
```bash
python dynamic_pop_density.py --lat-min -33.95 --lat-max -33.80 --lon-min 151.10 --lon-max 151.30 --output outputs/density_sydney.png --workers 12
```

### Melbourne, Australia
```bash
python dynamic_pop_density.py --lat-min -37.90 --lat-max -37.72 --lon-min 144.90 --lon-max 145.10 --output outputs/density_melbourne.png --workers 12
```

## Custom Parameters

Adjust these flags as needed:
- `--lat-min`, `--lat-max`: Latitude bounds (WGS84)
- `--lon-min`, `--lon-max`: Longitude bounds (WGS84)
- `--step`: Grid resolution (default 0.001 ≈ 100m, use 0.002 for faster rendering)
- `--workers`: Parallel requests (higher = faster, but don't overload server)
- `--output`: Output file path

Example with lower resolution for faster rendering:
```bash
python dynamic_pop_density.py --lat-min 48.78 --lat-max 48.95 --lon-min 2.25 --lon-max 2.50 --step 0.002 --output outputs/density_paris_lowres.png --workers 12
```
