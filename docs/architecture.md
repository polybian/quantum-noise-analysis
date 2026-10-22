# Architecture

## What this is

Three implementations that characterize **quantum hardware noise**
using realistic Qiskit Aer noise models — depolarizing gate errors and
readout errors — applied to circuits from my earlier work (Bell state,
Grover's search). Everything runs on the local Aer simulator with
seeded randomness: reproducible, inspectable, and honest about what it
is — a *model* of hardware noise, not a hardware run.

## Layout

```
quantum-noise-analysis/
├── README.md
├── requirements.txt           # qiskit + qiskit-aer + numpy
├── run_all.sh
├── scripts/
│   ├── 01_ideal_vs_noisy.py    # Bell state: ideal vs depolarizing+readout noise
│   ├── 02_readout_mitigation.py# calibration matrix + matrix-inversion mitigation
│   └── 03_noise_sweep.py       # Grover success vs depolarizing p (6 points)
├── docs/
│   ├── architecture.md        # this file
│   └── interview-answers.md
└── simplified-explanation.md  # plain-language guide (Spanish)
```

## The noise models

**Depolarizing channel** (gate noise): with probability p, a gate's
qubit is replaced by the maximally mixed state — the standard
first-order model for imperfect gates. Applied at p=1% on 1-qubit gates
(H, X) and p=2% on 2-qubit gates (CX, CZ), in line with the rough
ratios of current superconducting hardware (order-of-magnitude only;
no claim about any specific device).

**Readout error** (measurement noise): a classical bit-flip channel at
measurement time, `P(measure i | prepared j)`. Used asymmetrically
(e.g. 4% for 0->1, 6% for 1->0) because real readout is rarely
symmetric.

Both are *Markovian, time-independent* approximations. Real devices
also suffer T1/T2 decoherence, crosstalk, drift, and leakage — none of
which are modeled here. The README states this plainly.

## How the implementations run

```
┌──────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Python      │     │  Qiskit Aer      │     │  Your terminal  │
│  script      │────▶│  simulator +     │────▶│  histograms,    │
│  builds the  │     │  NoiseModel      │     │  tables,        │
│  circuit     │     │  (seeded)        │     │  assertions     │
└──────────────┘     └──────────────────┘     └─────────────────┘
```

- **01** runs the identical Bell circuit twice — once clean, once with
  the full noise model — and compares the 00/11 correlation.
- **02** builds the 4x4 assignment matrix from calibration circuits
  (prepare each basis state, measure it), then applies its
  least-squares inverse to the raw noisy distribution. Residual
  negatives are clipped and the result renormalized — the standard
  textbook procedure.
- **03** rebuilds the noise model at each p (1-qubit p, 2-qubit 2p)
  and runs Grover's search, recording the |11> success rate.

## Design choices

- **Per-script noise models, no shared magic**: each script declares
  its model at the top so the reader always knows exactly what noise
  is in play. Script 02 deliberately uses readout-only noise so the
  mitigation gain is unambiguous.
- **Seeded everything**: simulator seeds and numpy seeds are fixed;
  the README numbers regenerate bit-for-bit.
- **Assertions as verdicts**: each script encodes its conclusion
  (`ideal == 100%`, `mitigated < raw/2`, `success(p_min) > 90% >
  success(p_max)`), so the physics claim is a passing check.
- **No hardware token required**: the honest next step — porting the
  same circuits to real IBM Quantum backends and comparing measured
  device noise against these models — is documented in the README
  instead of faked.
