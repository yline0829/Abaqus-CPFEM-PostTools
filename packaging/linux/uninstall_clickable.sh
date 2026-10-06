#!/usr/bin/env bash
set -e
PREFIX="$HOME/.local/share/odb2vtu-s"
LEGACY_PREFIX="$HOME/.local/share/abaqus-cpfem-posttools"
APPS="$HOME/.local/share/applications"
DESKTOP=""
if command -v xdg-user-dir >/dev/null 2>&1; then DESKTOP="$(xdg-user-dir DESKTOP 2>/dev/null || true)"; fi
if [ -z "$DESKTOP" ] || [ "$DESKTOP" = "$HOME" ]; then
  if [ -d "$HOME/桌面" ]; then DESKTOP="$HOME/桌面"; else DESKTOP="$HOME/Desktop"; fi
fi
rm -rf "$PREFIX" "$LEGACY_PREFIX"
rm -f "$APPS/odb2vtu-s-exporter.desktop" "$APPS/odb2vtu-s-cpfem-postprocessor.desktop" "$APPS/abaqus-data-exporter.desktop" "$APPS/abaqus-cpfem-postprocess.desktop"
rm -f "$DESKTOP/ODB2VTU-S Exporter.desktop" "$DESKTOP/ODB2VTU-S CPFEM Postprocessor.desktop" "$DESKTOP/Abaqus Data Exporter.desktop" "$DESKTOP/Abaqus CPFEM Postprocess.desktop"
echo "ODB2VTU-S removed. User ODB/INP/results were not touched."
