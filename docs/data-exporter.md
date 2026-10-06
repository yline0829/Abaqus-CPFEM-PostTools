# ODB2VTU-S Exporter notes

ODB2VTU-S Exporter opens ODBs read-only and is designed specifically for large simulations. It selectively reads only the requested instance/region, Step, Frame, and Field Output instead of converting the complete database.

## VTU/PVD

- one VTU file represents one selected state
- a PVD file indexes multiple VTUs as a time series
- element/integration-point fields are written as CellData
- nodal fields are written as PointData
- integration-point values are averaged per element for visualization

## Derived fields

- `Mises`: computed from stress components
- Initial IPF: HCP-Ti initial orientation from per-grain material Euler angles in the INP
- GND increment fields: see `gnd_mapping.md`

## Field analysis

The extrema tool supports global extrema, grain statistics, Top-N grains, extreme-band grains, and optional region/BBox filtering. Selected grains can be exported as geometry-only VTUs so unrelated grains are absent in ParaView.
