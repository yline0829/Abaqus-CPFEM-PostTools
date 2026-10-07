#!/usr/bin/env bash
set -e
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PREFIX="$HOME/.local/share/odb2vtu-s"
APPS="$HOME/.local/share/applications"
DESKTOP=""
if command -v xdg-user-dir >/dev/null 2>&1; then DESKTOP="$(xdg-user-dir DESKTOP 2>/dev/null || true)"; fi
if [ -z "$DESKTOP" ] || [ "$DESKTOP" = "$HOME" ]; then
  if [ -d "$HOME/桌面" ]; then DESKTOP="$HOME/桌面"; else DESKTOP="$HOME/Desktop"; fi
fi
mkdir -p "$PREFIX/data_exporter" "$PREFIX/postprocess" "$PREFIX/icons" "$APPS" "$DESKTOP"
if [ -d "$SRC/assets/icons" ]; then ICON_SRC="$SRC/assets/icons"; else ICON_SRC="$SRC/icons"; fi
cp -a "$SRC/src/data_exporter/linux/." "$PREFIX/data_exporter/"
cp -a "$SRC/src/data_exporter/backend/." "$PREFIX/data_exporter/"
cp -a "$SRC/src/postprocess/linux/." "$PREFIX/postprocess/"
cp -a "$SRC/src/postprocess/backend/." "$PREFIX/postprocess/"
cp -a "$ICON_SRC/." "$PREFIX/icons/"
chmod +x "$PREFIX/data_exporter/launch.sh" "$PREFIX/postprocess/launch.sh"
cat > "$APPS/odb2vtu-s-exporter.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=ODB2VTU-S Exporter
Exec=$PREFIX/data_exporter/launch.sh
Icon=$PREFIX/icons/odb2vtu-s-exporter.png
Terminal=false
Categories=Science;Engineering;
StartupNotify=true
EOF
cat > "$APPS/odb2vtu-s-cpfem-postprocessor.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=ODB2VTU-S CPFEM Postprocessor
Exec=$PREFIX/postprocess/launch.sh
Icon=$PREFIX/icons/odb2vtu-s-cpfem-postprocessor.png
Terminal=false
Categories=Science;Engineering;
StartupNotify=true
EOF
chmod +x "$APPS/odb2vtu-s-exporter.desktop" "$APPS/odb2vtu-s-cpfem-postprocessor.desktop"
cp "$APPS/odb2vtu-s-exporter.desktop" "$DESKTOP/ODB2VTU-S Exporter.desktop"
cp "$APPS/odb2vtu-s-cpfem-postprocessor.desktop" "$DESKTOP/ODB2VTU-S CPFEM Postprocessor.desktop"
chmod +x "$DESKTOP/ODB2VTU-S Exporter.desktop" "$DESKTOP/ODB2VTU-S CPFEM Postprocessor.desktop"
for f in "$DESKTOP/ODB2VTU-S Exporter.desktop" "$DESKTOP/ODB2VTU-S CPFEM Postprocessor.desktop"; do
  command -v gio >/dev/null 2>&1 && gio set "$f" metadata::trusted true >/dev/null 2>&1 || true
  command -v gvfs-set-attribute >/dev/null 2>&1 && gvfs-set-attribute "$f" metadata::trusted true >/dev/null 2>&1 || true
done
command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$APPS" >/dev/null 2>&1 || true
printf '\nInstalled to: %s\n' "$PREFIX"
printf 'Set ABAQUS_CMD before launching if your Abaqus command is not simply "abaqus".\n'
