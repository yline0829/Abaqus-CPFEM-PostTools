# Changelog

All notable changes will be documented in this file.

## [Unreleased]

### Changed
- Project branding standardized as **ODB2VTU-S** (`S = Selective`).
- Application names standardized as **ODB2VTU-S Exporter** and **ODB2VTU-S CPFEM Postprocessor**.
- Automatic output directory renamed from `ADE_Output` to `ODB2VTU_Output` for future builds.
- Future release asset names use the ODB2VTU-S naming scheme.

## [0.1.0] - 2026-10-06

### Added
- First public source release.
- Cross-platform ODB2VTU-S Exporter (original v0.1.0 name: Abaqus Data Exporter).
- Selective VTU/PVD export and large-ODB frame selection.
- GrainID, Mises, Initial HCP-Ti IPF, and field-extremum analysis.
- 18-slip-system GND differences from DAT initial state and sliding-start reference state.
- Cross-platform RP history and PEEQCP postprocessor.
- Q5 StepTime target schedule: indentation first/last; sliding T0/T25/T50/T75/T100.
- PEEQCP target-frame write-back and validation.
- Linux live progress logging.
