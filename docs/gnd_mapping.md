# ODB2VTU-S — GND mapping used by the current CPFEM workflow

The GND feature is **not a generic Abaqus convention**. It follows the current UMAT/data layout used by this project.

`gnd_field.dat`:

- column 1: Abaqus element label
- columns 2–10: nine initial GND direction densities `rho1 ... rho9`

Each initial direction is split equally between two slip systems:

| DAT column | Direction label | Slip systems | SDV fields |
|---|---|---:|---|
| 2 | `[11-20]` | 3, 6 | SDV13, SDV16 |
| 3 | `[1-210]` | 1, 5 | SDV11, SDV15 |
| 4 | `[2-1-10]` | 2, 4 | SDV12, SDV14 |
| 5 | `[-2113]` | 7, 17 | SDV17, SDV27 |
| 6 | `[-1-123]` | 8, 10 | SDV18, SDV20 |
| 7 | `[1-213]` | 9, 11 | SDV19, SDV21 |
| 8 | `[2-1-13]` | 12, 14 | SDV22, SDV24 |
| 9 | `[11-23]` | 13, 15 | SDV23, SDV25 |
| 10 | `[-12-13]` | 16, 18 | SDV26, SDV28 |

For a slip system `alpha`, the DAT-referenced increment is

```text
DGND_Slip(alpha) = current SDV(10+alpha) - initial slip GND(alpha)
```

where the initial slip value is one half of its paired DAT direction.

The exporter also supports a sliding-reference increment:

```text
DGND_Slide_Slip(alpha, t)
  = SDV(10+alpha, t) - SDV(10+alpha, sliding reference)
```

The reference may be the first frame of the first sliding step or the last frame of the preceding step.

Do not use this mapping with another UMAT until the SDV definitions have been verified.
