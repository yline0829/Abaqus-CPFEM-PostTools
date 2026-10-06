# Linux installation

The Linux GUIs use system Python 3 + Tkinter. ODB operations run through Abaqus Python.

## Dependencies

Example for CentOS 7:

```bash
sudo yum install -y python3-tkinter
```

## Abaqus command

If your executable is directly available:

```bash
ABAQUS_CMD=abaqus ./launch.sh
```

or:

```bash
ABAQUS_CMD=abq2024 ./launch.sh
```

For Singularity/Apptainer installations, use the full prefix, for example:

```bash
ABAQUS_CMD='singularity exec /path/to/abaqus2024.sif /opt/run_abaqus.sh' ./launch.sh
```

Do not append `cae -mesa`; the tools append `python <script>` themselves.

## Desktop install

From the repository root:

```bash
chmod +x packaging/linux/install_clickable.sh
./packaging/linux/install_clickable.sh
```

Uninstall:

```bash
./packaging/linux/uninstall_clickable.sh
```

Uninstalling removes only program files and shortcuts, not ODB/INP/results.
