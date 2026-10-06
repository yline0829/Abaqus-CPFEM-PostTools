# Windows installation

## Data Exporter

Use the Windows portable release and launch:

~~~text
Launch_Abaqus_Data_Exporter.vbs
~~~

Abaqus must be callable from Command Prompt, normally as \`abaqus\`.

## CPFEM Postprocess

Launch:

~~~text
Launch_Abaqus_Postprocess_GUI.bat
~~~

The GUI calls \`abaqus python abaqus_postprocess_master.py ...\`.

## Notes

- Keep the launcher, GUI, and backend scripts in the same folder.
- Close Abaqus/Viewer before writing PEEQCP back to an ODB.
- Do not keep a generated PVD open in ParaView while replacing that same file on Windows.
