# Abaqus-CPFEM-PostTools

[![Latest Release](https://img.shields.io/github/v/release/yline0829/Abaqus-CPFEM-PostTools?display_name=tag&sort=semver)](https://github.com/yline0829/Abaqus-CPFEM-PostTools/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Windows](https://img.shields.io/badge/Windows-supported-0078D6?logo=windows&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-supported-FCC624?logo=linux&logoColor=black)

Cross-platform post-processing tools for **Abaqus/CPFEM**, focused on selective ODB extraction, ParaView visualization, grain-resolved analysis, GND evolution, tribological history data, and PEEQCP reconstruction.
# Abaqus-CPFEM-PostTools

Cross-platform post-processing tools for **Abaqus/CPFEM**, with a focus on selective ODB extraction, ParaView visualization, grain-resolved analysis, GND evolution, tribological history data, and PEEQCP reconstruction.

> This project is independent of Dassault Systèmes. Abaqus is required to read/write ODB files; no Abaqus libraries or binaries are distributed here.

## Applications

### Abaqus Data Exporter

- Selective ODB → **VTU/PVD** export for ParaView
- Large-ODB workflow: read only selected instances, sets, steps, frames, and fields
- `GrainID` reconstruction and `<All Grains>` selection
- Derived **von Mises stress**
- **Initial HCP-Ti IPF** from per-grain material Euler angles in the INP
- Field extrema / grain correlation analysis
- Top-N / extreme-band grain-only VTU export
- History/curve CSV export
- 18-slip-system GND evolution from `gnd_field.dat` vs. `SDV11–SDV28`
- Sliding-start GND increment using the first sliding frame or the previous step's last frame as reference

### Abaqus CPFEM Postprocess

- RP history extraction: `U1/U2`, `RF1/RF2`, `CF1/CF2`, COF
- Frame-by-frame PEEQCP reconstruction from `Fp = SDV1–SDV9`
- Target-state saving:
  - indentation/normal-loading step: first + last frame
  - each sliding cycle: **T0/T25/T50/T75/T100 by StepTime**
- Nearest actual ODB frame is selected when a target StepTime is not stored exactly
- PEEQCP can be written back to those selected ODB frames
- Linux live progress logging and completion notifications

## Repository layout

```text
src/
  data_exporter/
    backend/     # Abaqus-Python ODB backends
    windows/     # PowerShell/WPF GUI
    linux/       # Python/Tk GUI
  postprocess/
    backend/     # history + PEEQCP backend
    windows/     # PowerShell GUI
    linux/       # Python/Tk GUI
packaging/linux/ # desktop installer/uninstaller
scripts/         # release builder
docs/            # methods and installation notes
examples/        # small, non-proprietary examples
```

## Requirements

- A licensed Abaqus installation providing `odbAccess`
- An Abaqus command such as `abaqus` or `abq2024`
- ParaView for VTU/PVD visualization (tested workflow includes ParaView 5.10.1)
- Windows: Windows PowerShell / WPF
- Linux GUI: Python 3 + Tkinter

For containerized Abaqus on Linux, set the GUI's **Abaqus command** to the full prefix, for example:

```bash
singularity exec /path/to/abaqus2024.sif /opt/run_abaqus.sh
```

The application appends `python <backend.py> ...` automatically.

## Important model assumptions

Some CPFEM-derived functions are model-specific. In particular, the current GND mapping assumes:

- `SDV11–SDV28` are the 18 slip-system GND densities
- `gnd_field.dat` column 1 is Abaqus element label
- columns 2–10 are nine initial GND/Burgers-direction densities
- each direction is split equally between its paired slip systems

See [docs/gnd_mapping.md](docs/gnd_mapping.md) before using the GND tools with another UMAT.

PEEQCP reconstruction assumes `SDV1–SDV9` contain `Fp` in the documented Fortran column-major mapping. See [docs/peeqcp.md](docs/peeqcp.md).

## Installation

- [Windows](docs/install-windows.md)
- [Linux](docs/install-linux.md)

For normal users, downloading a packaged asset from **Releases** is recommended. The repository itself is primarily the maintainable source tree.

## Build release packages

From a normal Python 3 environment:

```bash
python scripts/build_release.py
```

The generated ZIP files are written to `dist/` and are intentionally ignored by Git.

## Development status

This is the first public source release (`v0.1.0`). The project grew from an internal research post-processing workflow and is being generalized incrementally. Please report model/version compatibility issues through GitHub Issues.

## License

MIT License. See [LICENSE](LICENSE).
