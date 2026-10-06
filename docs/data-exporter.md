# Data Exporter notes

The exporter opens ODBs read-only and is designed to avoid full-database conversion for large simulations.

## VTU/PVD

- one VTU file represents one selected state
- a PVD file indexes multiple VTUs as a time series
- element/integration-point fields are written as CellData
- nodal fields are written as PointData
- integration-point values are averaged per element for visualization

## Derived fields

- \`Mises\`: computed from stress components
- Initial IPF: HCP-Ti initial orientation from per-grain material Euler angles in the INP
- GND increment fields: see \`gnd_mapping.md\`

## Field analysis

The extrema tool supports global extrema, grain statistics, Top-N grains, extreme-band grains, and optional region/BBox filtering. Selected grains can be exported as geometry-only VTUs so unrelated grains are absent in ParaView.
