# quantum-noise-analysis

Three implementations that characterize **quantum hardware noise**
using realistic Qiskit Aer noise models — depolarizing gate errors and
readout errors — applied to the Bell state and Grover's search. No
hardware token needed: everything runs on the local simulator, seeded
and reproducible.

I love molecular engineering, and above all QUANTUM.
Quantum engineering starts with measuring the machine: gate fidelities, readout matrices, and how
fast noise erodes an algorithm's advantage.

## The three implementations

| # | Script | What it demonstrates |
|---|--------|----------------------|
| 1 | `01_ideal_vs_noisy.py` | **Ideal vs noisy Bell state** — the same circuit run clean and under a depolarizing + readout-error noise model |
| 2 | `02_readout_mitigation.py` | **Readout-error mitigation** — calibration matrix + matrix inversion cuts the measurement error 42x |
| 3 | `03_noise_sweep.py` | **Depolarizing noise sweep** — Grover success rate vs gate error p, from 99.2% down to 67.2% |

## Architecture

```
┌──────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Python      │     │  Qiskit Aer      │     │  Your terminal  │
│  script      │────▶│  simulator +     │────▶│  histograms,    │
│  builds the  │     │  NoiseModel      │     │  tables,        │
│  circuit     │     │  (seeded)        │     │  assertions     │
└──────────────┘     └──────────────────┘     └─────────────────┘
```

Each script declares its noise model up front, runs seeded simulations,
prints the results, and **asserts its conclusion** — so the claim is a
passing check, not commentary. See [docs/architecture.md](docs/architecture.md)
for the models, the math, and what is deliberately left out.

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

bash run_all.sh
```

## Validation

Measured on Qiskit Aer 2.6.0 (seeded simulator), 2026-10-21.
These are **simulator noise models**, not real hardware runs.

| Implementation | Prediction | Measured |
|---------------|-----------|----------|
| Ideal vs noisy Bell (4096 shots) | ideal 100% correlation; noisy degraded | ideal **100.00%**; noisy **90.28%** (9.72 points lost to depolarizing 1q=1%/2q=2% + 4–6% readout) — assertion passed |
| Readout mitigation (8192 shots) | mitigation at least halves the readout error | raw error **9.50%** → mitigated **0.22%** (**42.4x** lower) — assertion passed. Scope note: this 42x comes from a **readout-error-only model** where the same calibration matrix is used to calibrate and to measure, so the correction is near-ideal. On real hardware, gate errors and drift shrink the gain substantially |
| Noise sweep, Grover (2048 shots × 6) | success >90% at smallest p, decaying with p | p=0.001: **99.2%** · 0.005: **95.4%** · 0.01: **90.9%** · 0.02: **83.4%** · 0.03: **78.2%** · 0.05: **67.2%** — assertion passed |

## Why this matters (the one-paragraph version)

Algorithms don't run on math — they run on hardware, and hardware is
noisy. A Bell state that correlates perfectly in theory drops to 90%
under modest noise; Grover's speedup visibly erodes as gate error
grows. Characterizing that degradation — and mitigating what can be
mitigated — is the daily work of quantum engineering. These
implementations do it in a controlled, reproducible setting: models you
can inspect, numbers you can regenerate, and a documented path to the
real thing.

## Honest scope

Modeled: depolarizing gate errors, readout bit-flips. **Not modeled:**
T1/T2 decoherence, crosstalk, drift, leakage — real devices have all of
those. The models are order-of-magnitude realistic, not calibrated
against any specific device. The next step is running these same
circuits on real IBM Quantum hardware (free tier) and comparing
measured device noise against these model predictions.

## Plain-language guide

[simplified-explanation.md](simplified-explanation.md) — quantum noise
explained plainly: the radio with static, the bell that sometimes
lies, and turning up the static little by little (Spanish).
