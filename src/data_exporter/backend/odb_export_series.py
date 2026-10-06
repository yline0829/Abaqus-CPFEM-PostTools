# -*- coding: utf-8 -*-
from __future__ import print_function

import os, sys, argparse, traceback
from xml.sax.saxutils import escape
from odbAccess import openOdb

from odb_export_vtu import parse_bbox, selected_elements, export_frame


def read_selection_file(path):
    rows = []
    with open(path, "r", encoding="utf-8-sig") as f:
        for lineno, line in enumerate(f, 1):
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            parts = s.split("\t")
            if len(parts) != 2:
                raise RuntimeError("Invalid selection line %d. Expected StepName<TAB>FrameIndex." % lineno)
            rows.append((parts[0], int(parts[1])))
    return rows


def write_pvd(path, datasets):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write('<?xml version="1.0"?>\n')
        f.write('<VTKFile type="Collection" version="0.1" byte_order="LittleEndian">\n')
        f.write('  <Collection>\n')
        for t, rel in datasets:
            f.write('    <DataSet timestep="%.16g" group="" part="0" file="%s"/>\n' % (float(t), escape(rel.replace("\\", "/"))))
        f.write('  </Collection>\n')
        f.write('</VTKFile>\n')
    if os.path.exists(path):
        os.remove(path)
    os.rename(tmp, path)


def step_offsets(odb, step_names):
    offsets = {}
    t = 0.0
    for name in step_names:
        offsets[name] = t
        st = odb.steps[name]
        if len(st.frames):
            t += float(st.frames[-1].frameValue)
    return offsets


def make_signature(a):
    parts = [
        "fields=" + str(a.fields),
        "element_set=" + str(a.element_set),
        "bbox=" + str(a.bbox),
        "delta=" + str(a.delta_field),
        "ref=" + str(a.ref_step) + ":" + str(a.ref_frame),
        "mises=" + str(int(bool(a.mises))),
        "initial_ipf=" + str(int(bool(a.initial_ipf))),
        "inp=" + os.path.abspath(a.inp) if a.inp else "inp=",
        "ipf_dir=" + str(a.ipf_dir),
        "gnd_diff=" + str(int(bool(a.gnd_diff))),
        "gnd_dat=" + (os.path.abspath(a.gnd_dat) if a.gnd_dat else ""),
        "gnd_dat_size=" + (str(os.path.getsize(a.gnd_dat)) if a.gnd_dat and os.path.exists(a.gnd_dat) else ""),
        "gnd_dat_mtime=" + (str(os.path.getmtime(a.gnd_dat)) if a.gnd_dat and os.path.exists(a.gnd_dat) else ""),
        "gnd_diff_mode=" + str(a.gnd_diff_mode),
        "gnd_slide_diff=" + str(int(bool(a.gnd_slide_diff))),
        "gnd_slide_ref=" + str(a.gnd_slide_ref),
    ]
    return "\n".join(parts) + "\n"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--odb", required=True)
    p.add_argument("--instance", required=True)
    p.add_argument("--selection-file", required=True)
    p.add_argument("--out-pvd", required=True)
    p.add_argument("--fields", default="")
    p.add_argument("--element-set", default="")
    p.add_argument("--bbox", default="")
    p.add_argument("--delta-field", default="")
    p.add_argument("--ref-step", default="")
    p.add_argument("--ref-frame", type=int, default=-1)
    p.add_argument("--resume", type=int, default=1)
    p.add_argument("--mises", type=int, default=0)
    p.add_argument("--initial-ipf", type=int, default=0)
    p.add_argument("--inp", default="")
    p.add_argument("--ipf-dir", default="Z", choices=["X","Y","Z"])
    p.add_argument("--gnd-diff", type=int, default=0)
    p.add_argument("--gnd-dat", default="")
    p.add_argument("--gnd-diff-mode", default="slips", choices=["slips"])
    p.add_argument("--gnd-slide-diff", type=int, default=0)
    p.add_argument("--gnd-slide-ref", default="sliding0", choices=["sliding0","previous_last"])
    a = p.parse_args()

    odb = None
    try:
        bbox = parse_bbox(a.bbox)
        fields = [x.strip() for x in a.fields.split(",") if x.strip()]
        if a.initial_ipf and (not a.inp or not os.path.exists(a.inp)):
            raise RuntimeError("Initial IPF requires a valid INP file.")
        if a.gnd_diff and (not a.gnd_dat or not os.path.exists(a.gnd_dat)):
            raise RuntimeError("GND difference requires a valid gnd_field.dat file.")

        raw = read_selection_file(a.selection_file)
        if not raw:
            raise RuntimeError("No Step/Frame states were selected.")

        pvd = os.path.abspath(a.out_pvd)
        pdir = os.path.dirname(pvd) or os.getcwd()
        if not os.path.exists(pdir): os.makedirs(pdir)
        stem = os.path.splitext(os.path.basename(pvd))[0]
        frame_dir = os.path.join(pdir, stem + "_frames")
        if not os.path.exists(frame_dir): os.makedirs(frame_dir)

        signature = make_signature(a)
        sig_path = os.path.join(frame_dir, "_ADE_export_signature.txt")
        signature_matches = False
        if os.path.exists(sig_path):
            try:
                with open(sig_path,"r") as sf:
                    signature_matches = (sf.read() == signature)
            except Exception:
                signature_matches = False
        with open(sig_path,"w") as sf:
            sf.write(signature)

        print("Opening ODB (read-only):", a.odb)
        odb = openOdb(a.odb, readOnly=True)
        print("ODB opened.")

        step_names = list(odb.steps.keys())
        step_index = dict((name, i) for i, name in enumerate(step_names))
        offsets = step_offsets(odb, step_names)

        unique = set(); selected = []
        for sname, fi in raw:
            if sname not in odb.steps:
                raise RuntimeError("Selected Step not found: %s" % sname)
            st = odb.steps[sname]
            if fi < 0 or fi >= len(st.frames):
                raise RuntimeError("Selected frame out of range: %s / %d (frames=%d)" % (sname, fi, len(st.frames)))
            key = (sname, fi)
            if key not in unique:
                unique.add(key); selected.append(key)
        selected.sort(key=lambda x: (step_index[x[0]], x[1]))

        print("Selected states:", len(selected))
        if a.instance not in odb.rootAssembly.instances:
            raise RuntimeError("Instance not found: %s" % a.instance)
        inst = odb.rootAssembly.instances[a.instance]

        elems, node_map, grain_ids = selected_elements(inst, a.element_set, bbox)
        if not elems:
            raise RuntimeError("No elements selected.")
        elem_labels = set(int(e.label) for e in elems)
        node_labels = set(n for e in elems for n in e.connectivity)
        mesh_cache = (elems, node_map, grain_ids, elem_labels, node_labels)

        datasets = []
        ref_cache = None
        ipf_cache = None
        gnd_cache = None
        gnd_slide_cache = None
        last_time = None
        can_resume = bool(a.resume) and signature_matches

        for seq, (sname, fi) in enumerate(selected, 1):
            frame = odb.steps[sname].frames[fi]
            global_t = offsets[sname] + float(frame.frameValue)
            if last_time is not None and global_t <= last_time:
                eps = max(1.0e-12, abs(last_time) * 1.0e-12)
                global_t = last_time + eps

            safe_step = "".join(c if c.isalnum() or c in "_-" else "_" for c in sname)
            vtu_name = "%s_%06d_%s_f%06d.vtu" % (stem, seq, safe_step, fi)
            vtu_path = os.path.join(frame_dir, vtu_name)
            rel = os.path.relpath(vtu_path, pdir)

            if can_resume and os.path.exists(vtu_path) and os.path.getsize(vtu_path) > 0:
                print("[%d/%d] exists -> %s / frame %d" % (seq, len(selected), sname, fi))
            else:
                print("[%d/%d] exporting %s / frame %d ; global_t=%.12g" % (seq, len(selected), sname, fi, global_t))
                mesh_cache, ref_cache, ipf_cache, gnd_cache, gnd_slide_cache = export_frame(
                    odb, a.instance, sname, fi, vtu_path, fields,
                    a.element_set, bbox, a.delta_field, a.ref_step, a.ref_frame,
                    mesh_cache=mesh_cache, ref_cache=ref_cache,
                    derived_mises=bool(a.mises), initial_ipf=bool(a.initial_ipf),
                    inp_path=a.inp, ipf_dir=a.ipf_dir, ipf_cache=ipf_cache,
                    gnd_diff=bool(a.gnd_diff), gnd_dat=a.gnd_dat,
                    gnd_diff_mode=a.gnd_diff_mode, gnd_cache=gnd_cache,
                    gnd_slide_diff=bool(a.gnd_slide_diff), gnd_slide_ref=a.gnd_slide_ref,
                    gnd_slide_cache=gnd_slide_cache
                )

            datasets.append((global_t, rel)); last_time = global_t
            write_pvd(pvd, datasets)

        print("")
        print("SUCCESS")
        print("PVD:", pvd)
        print("Frame folder:", frame_dir)
        print("Exported states:", len(datasets))
        print("Open only the .pvd file in ParaView.")
        return 0
    except Exception:
        print("FATAL EXCEPTION:")
        print(traceback.format_exc())
        return 99
    finally:
        try:
            if odb is not None: odb.close()
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main())
