# Comprehensive Field Data Collection Guide

_Precision measurement protocols for reliable model inputs_

---

## Overview

This guide provides detailed protocols for collecting the 8 key parameters required for the LuxBio AI Tracking App. Each parameter is designed to be measurable with minimal equipment while providing maximum accuracy for model training and validation.

---

## **1. Actual Distance (0-1000 m)**

**What**: Maximum visibility range where markers are detectable  
**Why**: Primary performance metric for validation  
**How to Measure**:

1. Activate beads at Point A (record GPS)
2. Move observer/drone to increasing distances
3. Record GPS at detection boundary (Point B)
4. Calculate distance: `distance = GPS_distance(A,B)`

**Equipment**:

- Smartphone with GPS (Google Maps)
- Laser rangefinder (optional)

**Criteria**:

- Record when marker becomes _consistently_ visible (>3 sightings in 1 min)
- Maximum 1000m (beyond requires marine radar)

**Example**:  
`320m` - Drone lost visibility beyond this point

---

## **2. Activation Time (0-360 min)**

**What**: Time elapsed since bead activation  
**Why**: Bioluminescence decays exponentially over time  
**How to Measure**:

1. Start stopwatch at activation ("t=0")
2. Record test time relative to activation

**Equipment**:

- Waterproof stopwatch ($10)
- Smartphone timer

**Criteria**:

- Round to nearest minute
- Maximum 6 hours (360 min) - beads exhausted beyond

**Example**:  
`45 min` - Testing at 3/4 of product lifespan

---

## **3. Water Temperature (-2 to 30°C)**

**What**: Temperature at marker deployment depth  
**Why**: Critical for decay kinetics (Arrhenius equation)  
**How to Measure**:

1. Submerge thermometer 0.5m below surface
2. Wait 1 minute for stabilization
3. Record temperature

**Equipment**:

- Digital aquarium thermometer ($8)
- Infrared thermometer (less accurate)

**Criteria**:

- Measure within 5m of marker deployment
- Saltwater: -2°C (freezing) to 30°C (tropical)

**Example**:  
`8.5°C` - Typical North Pacific temperature

---

## **4. Wind Speed (0-25 m/s)**

**What**: Sustained wind speed at 10m height  
**Why**: Affects dispersion and wave formation  
**How to Measure**:

1. Hold phone at arm's length
2. Use anemometer app (e.g., "Wind Meter")
3. Record 1-minute average

**Equipment**:

- Smartphone + anemometer app (free)
- Handheld anemometer ($25)

**Criteria**:

- Beaufort scale cross-check:
  ```plaintext
  0-2 m/s: Calm (smoke rises vertically)
  5-8 m/s: Moderate (leaves rustle)
  10+ m/s: Strong (difficult to walk)
  ```

**Example**:  
`5.2 m/s` - Moderate breeze (Beaufort 3)

---

## **5. Precipitation (0-50 mm/hr)**

**What**: Liquid precipitation intensity  
**Why**: Light scattering reduces visibility  
**How to Measure**:

**Option 1 (Precise)**:

1. Place rain gauge in open area
2. Measure mm collected in 10 minutes
3. Multiply by 6 for mm/hr

**Option 2 (Visual)**:

```plaintext
None (0):       No rain
Light (1-4):    Drizzle, no puddles
Moderate (5-10): Steady rain, puddles form
Heavy (>10):    Downpour, poor visibility
```

**Equipment**:

- Plastic rain gauge ($5)
- Timer

**Criteria**:

- Record during test period
- Snow = 10× depth (e.g., 5cm snow = 50 mm/hr)

**Example**:  
`2.4 mm/hr` - Light rain

---

## **6. Wave Height (0-10 m)**

**What**: Significant wave height (trough to crest)  
**Why**: Surface scattering blocks light  
**How to Measure**:

**Boat Reference Method**:

```plaintext
Calm (0-0.3m):     Wavelets only
Light (0.3-0.8m):  Waves < knee-height
Moderate (0.8-1.5m): Waves waist-height
Rough (>1.5m):     Waves over head
```

**Shore Method**:

1. Time wave interval (seconds)
2. Wave height ≈ (interval × 1.5) meters

**Equipment**:

- Visual reference (human/boat)
- Stopwatch

**Criteria**:

- Estimate average of highest 1/3 waves

**Example**:  
`1.2m` - Whitecaps visible, moderate waves

---

## **7. Ambient Light (0.0001-0.1 lux)**

**What**: Background illumination level  
**Why**: Determines contrast threshold  
**How to Measure**:

1. Open light meter app
2. Point phone straight up
3. Record stable reading

**Equipment**:

- Lux Light Meter app (free)
- Professional lux meter ($50)

**Criteria**:

- Moonlight reference:
  ```plaintext
  0.0001 lux: Moonless night
  0.001 lux: Quarter moon
  0.01 lux: Half moon
  0.1 lux: Full moon
  ```

**Example**:  
`0.002 lux` - Typical starlit night

---

## **8. Sensor Type (human/drone/nvg)**

**What**: Detection technology used  
**Why**: 100× sensitivity differences  
**How to Record**:

```plaintext
human: Unaided vision (even with binoculars)
drone: Any UAV camera system
nvg:  Any night vision device
```

**Equipment**:

- N/A

**Criteria**:

- Test all available sensors separately
- Note model if known (e.g., "DJI Mavic 3")

**Example**:  
`nvg` - Used L3Harris PVS-31A goggles

---

## Field Data Collection Kit ($150 Total)

| **Item**              | **Purpose**       | **Cost** |
| --------------------- | ----------------- | -------- |
| Waterproof phone case | All measurements  | $15      |
| Digital thermometer   | Water temperature | $8       |
| Rain gauge            | Precipitation     | $5       |
| Stopwatch             | Activation timing | $10      |
| Anemometer            | Wind speed        | $25      |
| GPS app               | Distance/location | Free     |
| Lux Light Meter app   | Ambient light     | Free     |
| Field notebook        | Manual recording  | $5       |

---

## Data Validation Checklist

Before submitting data:

1. GPS coordinates within 10m accuracy ✅
2. All values within physical ranges ✅
3. Timestamps consistent across measurements ✅
4. Sensor type clearly specified ✅
5. Wave height matches precipitation/wind ✅

---

## Example Complete Dataset

```csv
test_id,date,lat,lon,actual_distance,activation_time,water_temp,wind_speed,precipitation,wave_height,ambient_light,sensor_type
VH-23,2023-08-15,48.423,-123.367,320,45,8.5,5.2,2.4,1.2,0.002,drone
VH-23,2023-08-15,48.423,-123.367,520,45,8.5,5.2,2.4,1.2,0.002,nvg
```

---

## Field Measurement Process

### Pre-Test Setup (30 minutes)

1. **Equipment Check**: Verify all instruments are calibrated
2. **Weather Assessment**: Record baseline conditions
3. **GPS Calibration**: Ensure accurate positioning
4. **Safety Briefing**: Review emergency procedures

### Test Execution (60-120 minutes)

1. **Activation**: Deploy beads, start stopwatch
2. **Environmental Monitoring**: Record conditions every 5 minutes
3. **Range Testing**: Test detection with each sensor type
4. **Data Recording**: Document all measurements immediately

### Post-Test (15 minutes)

1. **Data Review**: Verify all measurements are complete
2. **Quality Check**: Cross-reference related parameters
3. **Equipment Cleanup**: Secure and protect instruments
4. **Notes**: Record any unusual conditions or observations

---

## Troubleshooting Common Issues

### GPS Accuracy Problems

- **Issue**: Inconsistent distance measurements
- **Solution**: Use multiple GPS readings, average results
- **Prevention**: Calibrate GPS before each test

### Weather Instrument Errors

- **Issue**: Unrealistic readings
- **Solution**: Cross-check with visual observations
- **Prevention**: Regular calibration and maintenance

### Sensor Detection Issues

- **Issue**: Inconsistent detection ranges
- **Solution**: Test multiple times, use median value
- **Prevention**: Standardize test procedures

---

## Data Quality Standards

### Acceptable Ranges

- **Distance**: ±10m accuracy for GPS measurements
- **Time**: ±1 minute for activation timing
- **Temperature**: ±0.5°C for water temperature
- **Wind**: ±1 m/s for wind speed
- **Precipitation**: ±1 mm/hr for rain gauge
- **Waves**: ±0.2m for visual estimates
- **Light**: ±20% for lux meter readings

### Red Flags

- Distance > 1000m (requires verification)
- Activation time > 360 minutes (beads exhausted)
- Water temperature outside -2 to 30°C range
- Wind speed > 25 m/s (storm conditions)
- Precipitation > 50 mm/hr (severe weather)
- Wave height > 10m (extreme conditions)
- Ambient light > 0.1 lux (too bright for testing)

---

> "Consistent methodology beats perfect measurements. Record what you can, when you can - but always record."  
> _Lux Bio Field Operations Handbook_

This protocol enables reliable data collection with minimal equipment. The categorical options (light/moderate/heavy) make it field-practical while capturing essential environmental variation for accurate modeling.
