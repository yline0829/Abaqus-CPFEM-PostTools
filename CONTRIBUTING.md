# Contributing

Contributions, bug reports, and compatibility reports are welcome.

## Before opening an issue

Please include:
- operating system
- Abaqus version
- launch command style (\`abaqus\`, \`abq2024\`, Singularity/Apptainer, etc.)
- whether the problem is in Data Exporter or CPFEM Postprocess
- Step/Frame and field involved
- the complete error traceback or log

Do **not** upload proprietary ODB/INP files unless you have permission to share them.

## Development workflow

1. Create a branch from \`main\`.
2. Make a focused change.
3. Run syntax checks and test with a small ODB when possible.
4. Update \`CHANGELOG.md\` for user-visible changes.
5. Open a pull request describing the model assumptions and validation performed.

## Compatibility principle

Avoid silently changing CPFEM variable definitions. Model-specific mappings (for example SDV → Fp or GND slip systems) must be documented explicitly.
