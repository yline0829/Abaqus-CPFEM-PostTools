# ODB2VTU-S — Windows installation

## ODB2VTU-S Exporter

Use the Windows portable release and launch:

```text
Launch_ODB2VTU-S_Exporter.vbs
```

Abaqus must be callable from Command Prompt, normally as `abaqus`.

## ODB2VTU-S CPFEM Postprocessor

Launch:

```text
Launch_ODB2VTU-S_CPFEM_Postprocessor.bat
```

The GUI calls `abaqus python abaqus_postprocess_master.py ...`.

## Notes

- Keep the launcher, GUI, and backend scripts in the same folder.
- Close Abaqus/Viewer before writing PEEQCP back to an ODB.
- Do not keep a generated PVD open in ParaView while replacing that same file on Windows.
