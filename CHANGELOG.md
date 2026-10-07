# Changelog

All notable changes will be documented in this file.

## [0.1.2] - 2026-10-07

### Added
- Dedicated application icons for **ODB2VTU-S Exporter** and **ODB2VTU-S CPFEM Postprocessor**.
- Linux Exporter vertical scrolling and mouse-wheel support for smaller displays.

### Changed
- Linux installer now installs and assigns separate desktop icons to the two applications.
- Release builder now includes application icon assets in Windows and Linux packages.


## [0.1.1] - 2026-10-07

### Changed
- Project branding standardized as **ODB2VTU-S** (`S = Selective`).
- Application names standardized as **ODB2VTU-S Exporter** and **ODB2VTU-S CPFEM Postprocessor**.
- Automatic output directory renamed from `ADE_Output` to `ODB2VTU_Output`.
- Windows launchers, Linux desktop entries, installer paths, and release asset names aligned with the ODB2VTU-S naming scheme.
- Repository links updated after the repository was renamed to `yline0829/ODB2VTU-S`.

### Added
- Linux Exporter now includes a dedicated **Selection Summary** panel showing ODB, instance/region, selected Step/Frame states, fields, derived fields, and output path.
- Linux Exporter now includes a dedicated **Output Messages** panel with clear-log control.
- Real-time Linux backend logging via `PYTHONUNBUFFERED=1`.
- Explicit success/failure dialogs for VTU/PVD export, Curve Data export, and Field Analysis.
- Scrollable Linux panels for smaller displays (ODB → VTU/PVD, Curve Data, and Field Analysis).
- Dedicated desktop icons: ODB→VTU visualization for **Exporter** and a curve-analysis icon for **CPFEM Postprocessor**.

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
