# KH910 Rev A — Solenoid Route Prefix Isolation

Progressive KiCad load probe. Variant 000 contains the validated net migration + footprints but none of the 50 new routing primitives.

- route_count=50

| Prefix | Result | Primitive added at this step |
|---:|---|---|
| 000 | LOADED | `baseline (no new route primitive)` |
| 001 | **FAILED TO LOAD** | `segment net=4 layer=F.Cu 301.95,150.938->303.43,152.42` |

## First failing prefix

Prefix: **001**

```text
(segment (start 301.95 150.938) (end 303.43 152.42) (width 1) (layer "F.Cu") (net 4) (tstamp 75b28208-c510-49fb-a4dc-f737800c7497))
```

KiCad output:
```text
Failed to load board
```
