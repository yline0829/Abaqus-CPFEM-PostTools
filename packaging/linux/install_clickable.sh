#!/usr/bin/env bash
set -e
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PREFIX="$HOME/.local/share/abaqus-cpfem-posttools"
APPS="$HOME/.local/share/applications"
DESKTOP=""
if command -v xdg-user-dir >/dev/null 2>&1; then DESKTOP="$(xdg-user-dir DESKTOP 2>/dev/null || true)"; fi
if [ -z "$DESKTOP" ] || [ "$DESKTOP" = "$HOME" ]; then
  if [ -d "$HOME/桌面" ]; then DESKTOP="$HOME/桌面"; else DESKTOP="$HOME/Desktop"; fi
fi
mkdir -p "$PREFIX/data_exporter" "$PREFIX/postprocess" "$APPS" "$DESKTOP"
cp -a "$SRC/src/data_exporter/linux/." "$PREFIX/data_exporter/"
cp -a "$SRC/src/data_exporter/backend/." "$PREFIX/data_exporter/"
cp -a "$SRC/src/postprocess/linux/." "$PREFIX/postprocess/"
cp -a "$SRC/src/postprocess/backend/." "$PREFIX/postprocess/"
chmod +x "$PREFIX/data_exporter/launch.sh" "$PREFIX/postprocess/launch.sh"
cat > "$APPS/abaqus-data-exporter.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Abaqus Data Exporter
Exec=$PREFIX/data_exporter/launch.sh
Icon=applications-science
Terminal=false
Categories=Science;Engineering;
StartupNotify=true
EOF
cat > "$APPS/abaqus-cpfem-postprocess.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Abaqus CPFEM Postprocess
Exec=$PREFIX/postprocess/launch.sh
Icon=applications-science
Terminal=false
Categories=Science;Engineering;
StartupNotify=true
EOF
chmod +x "$APPS/abaqus-data-exporter.desktop" "$APPS/abaqus-cpfem-postprocess.desktop"
cp "$APPS/abaqus-data-exporter.desktop" "$DESKTOP/Abaqus Data Exporter.desktop"
cp "$APPS/abaqus-cpfem-postprocess.desktop" "$DESKTOP/Abaqus CPFEM Postprocess.desktop"
chmod +x "$DESKTOP/Abaqus Data Exporter.desktop" "$DESKTOP/Abaqus CPFEM Postprocess.desktop"
for f in "$DESKTOP/Abaqus Data Exporter.desktop" "$DESKTOP/Abaqus CPFEM Postprocess.desktop"; do
  command -v gio >/dev/null 2>&1 && gio set "$f" metadata::trusted true >/dev/null 2>&1 || true
  command -v gvfs-set-attribute >/dev/null 2>&1 && gvfs-set-attribute "$f" metadata::trusted true >/dev/null 2>&1 || true
done
command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$APPS" >/dev/null 2>&1 || true
printf '\nInstalled to: %s\n' "$PREFIX"
printf 'Set ABAQUS_CMD before launching if your Abaqus command is not simply "abaqus".\n'
