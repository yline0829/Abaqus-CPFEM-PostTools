#!/usr/bin/env python3
from pathlib import Path
import shutil, zipfile
ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
DIST.mkdir(exist_ok=True)
VERSION = (ROOT/'VERSION').read_text().strip()

def reset(path):
    if path.exists(): shutil.rmtree(path)
    path.mkdir(parents=True)

def zipdir(src, dst):
    if dst.exists(): dst.unlink()
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(src.rglob('*')):
            if p.is_file(): z.write(p, p.relative_to(src).as_posix())

def cp_tree(src, dst): shutil.copytree(src, dst, dirs_exist_ok=True)

work = ROOT/'.build'
if work.exists(): shutil.rmtree(work)
work.mkdir()

# Windows Data Exporter
wde = work/'Abaqus_Data_Exporter_Windows_Portable'
reset(wde)
cp_tree(ROOT/'src/data_exporter/windows', wde)
cp_tree(ROOT/'src/data_exporter/backend', wde)
zipdir(wde, DIST/f'Abaqus_Data_Exporter_Windows_Portable_v{VERSION}.zip')

# Windows Postprocess
wpp = work/'Abaqus_Postprocess_Windows_Portable'
reset(wpp)
cp_tree(ROOT/'src/postprocess/windows', wpp)
cp_tree(ROOT/'src/postprocess/backend', wpp)
zipdir(wpp, DIST/f'Abaqus_Postprocess_Windows_Portable_v{VERSION}.zip')

# Linux combined
lin = work/'Abaqus_Linux_Tools'
reset(lin)
(lin/'Abaqus_Data_Exporter_Linux').mkdir()
(lin/'Abaqus_Postprocess_Universal_Linux').mkdir()
cp_tree(ROOT/'src/data_exporter/linux', lin/'Abaqus_Data_Exporter_Linux')
cp_tree(ROOT/'src/data_exporter/backend', lin/'Abaqus_Data_Exporter_Linux')
cp_tree(ROOT/'src/postprocess/linux', lin/'Abaqus_Postprocess_Universal_Linux')
cp_tree(ROOT/'src/postprocess/backend', lin/'Abaqus_Postprocess_Universal_Linux')
shutil.copy2(ROOT/'packaging/linux/install_clickable.sh', lin/'install_clickable.sh')
shutil.copy2(ROOT/'packaging/linux/uninstall_clickable.sh', lin/'uninstall_clickable.sh')
# The combined installer in release root uses its own directory as source root.
text = (lin/'install_clickable.sh').read_text()
text = text.replace('SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"', 'SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"')
text = text.replace('$SRC/src/data_exporter/linux/.', '$SRC/Abaqus_Data_Exporter_Linux/.').replace('$SRC/src/data_exporter/backend/.', '$SRC/Abaqus_Data_Exporter_Linux/.')
text = text.replace('$SRC/src/postprocess/linux/.', '$SRC/Abaqus_Postprocess_Universal_Linux/.').replace('$SRC/src/postprocess/backend/.', '$SRC/Abaqus_Postprocess_Universal_Linux/.')
(lin/'install_clickable.sh').write_text(text)
(lin/'install_clickable.sh').chmod(0o755); (lin/'uninstall_clickable.sh').chmod(0o755)
zipdir(lin, DIST/f'Abaqus_Linux_Tools_v{VERSION}.zip')
print('Built release assets in', DIST)
