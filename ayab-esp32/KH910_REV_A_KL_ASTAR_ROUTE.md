# KH910 Rev A K/L route report v14

grid 0.2 mm; width 0.25 mm; clearance raster 0.22 mm

Pull-ups sit below J801 at y=124/126 mm. Machine L approaches its GPIO via vertically to clear the adjacent GND and ESP21 vias. KiCad DRC after zone refill is authoritative.

## machine-l
- net: `/BROTHER-CONNECTORS/EOL_R_S`
- candidate: 1
- layer: `In2.Cu`
- via start: (238.45, 145.63)
- start stub: (239.8, 146.8)
- goal stub: (221.67, 132.6)
- via goal: (221.67, 134.14)
- A* cells: 103
- routed segments: 7
- A* points: (239.800,146.800) -> (235.000,146.800) -> (223.000,134.800) -> (221.600,134.800) -> (221.600,132.800) -> (221.670,132.600)

## machine-k
- net: `/BROTHER-CONNECTORS/EOL_R_N`
- candidate: 1
- layer: `In2.Cu`
- via start: (239.22, 145.65)
- start stub: (240.2, 144.4)
- goal stub: (220.0, 133.2)
- via goal: (220.97, 134.15)
- A* cells: 132
- routed segments: 10
- A* points: (240.200,144.400) -> (240.200,138.800) -> (234.200,132.800) -> (227.400,132.800) -> (226.600,132.000) -> (226.600,131.800) -> (221.200,131.800) -> (220.000,133.000) -> (220.000,133.200)

## pullup-l
- net: `/BROTHER-CONNECTORS/EOL_R_S`
- candidate: 1
- layer: `In1.Cu`
- via start: (262.0, 126.0)
- start stub: (262.8, 126.0)
- goal stub: (238.45, 144.6)
- via goal: (238.45, 145.63)
- A* cells: 123
- routed segments: 4
- A* points: (262.800,126.000) -> (244.200,144.600) -> (238.450,144.600)

## pullup-k
- net: `/BROTHER-CONNECTORS/EOL_R_N`
- candidate: 1
- layer: `B.Cu`
- via start: (262.0, 124.0)
- start stub: (262.8, 124.0)
- goal stub: (240.2, 144.4)
- via goal: (239.22, 145.65)
- A* cells: 185
- routed segments: 8
- A* points: (262.800,124.000) -> (261.600,125.200) -> (245.400,125.200) -> (239.800,130.800) -> (239.800,144.200) -> (240.000,144.400) -> (240.200,144.400)

