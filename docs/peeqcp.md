# ODB2VTU-S — PEEQCP reconstruction and Q5 target states

## Fp mapping

The current CPFEM UMAT stores the plastic deformation gradient in `SDV1–SDV9` using Fortran column-major order:

```text
SDV1 = Fp11   SDV4 = Fp12   SDV7 = Fp13
SDV2 = Fp21   SDV5 = Fp22   SDV8 = Fp23
SDV3 = Fp31   SDV6 = Fp32   SDV9 = Fp33
```

## Incremental equivalent plastic strain

For consecutive frames:

```text
Delta Lp ~= (Fp[n+1] - Fp[n]) * inv(Fp[n])
Delta ep = sym(Delta Lp)
Delta ep_dev = Delta ep - tr(Delta ep)/3 * I
Delta PEEQCP = sqrt(2/3 * Delta ep_dev : Delta ep_dev)
```

The code accumulates this quantity over **all stored ODB frames**. It is therefore a frame-based reconstructed J2-equivalent plastic strain, not an exact UMAT-subincrement state variable.

## Q5 output schedule

The calculation still traverses every frame for accumulation, but snapshots are saved at selected physical states:

- indentation / normal-loading step: first frame and last frame
- each sliding cycle: target StepTime fractions 0%, 25%, 50%, 75%, 100%

If the target time is not stored exactly, the nearest actual ODB frame is chosen using binary search on `frameValue`.

This provides consistent state matching with VTU/PVD and GND analyses while preserving full-frame PEEQCP accumulation.
