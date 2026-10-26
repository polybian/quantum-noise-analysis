"""
02 - Readout-error mitigation on a noisy Bell state.

Readout errors flip classical bits at measurement time, independent of
the quantum computation itself. Because they are classical and stable,
they can be characterized once and undone:

  1. Calibration: prepare each computational basis state
     (|00>, |01>, |10>, |11>) and measure it -> the 4x4 assignment
     matrix A, where A[i,j] = P(measure i | prepared j).
  2. Correction: p_mitigated = A^-1 @ p_raw (least-squares, clipped
     to [0,1] and renormalized).

The script prints the calibration matrix, the raw noisy distribution,
and the mitigated distribution. Mitigation must cut the readout error
rate at least in half.

Noise model: readout error only, so any improvement is unambiguously
attributable to mitigation. (Gate noise would leave a residual floor
that readout mitigation cannot remove - noted, not hidden.)

Run:
    python3 scripts/02_readout_mitigation.py [--shots 8192]
"""

import argparse

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError

READOUT = [[0.95, 0.05],
           [0.05, 0.95]]
STATES = ["00", "01", "10", "11"]


def build_noise_model() -> NoiseModel:
    nm = NoiseModel()
    nm.add_all_qubit_readout_error(ReadoutError(READOUT))
    return nm


def bell_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc


def run(counts_circuit: QuantumCircuit, shots: int, seed: int,
        noise_model: NoiseModel) -> dict:
    return (
        AerSimulator(seed_simulator=seed)
        .run(counts_circuit, shots=shots, noise_model=noise_model)
        .result()
        .get_counts()
    )


def assignment_matrix(noise_model: NoiseModel, shots: int) -> np.ndarray:
    """A[i,j] = P(measure STATES[i] | prepared STATES[j])."""
    A = np.zeros((4, 4))
    for j, s in enumerate(STATES):
        qc = QuantumCircuit(2, 2)
        # Qiskit bitstrings are big-endian: left char = qubit 1.
        if s[1] == "1":
            qc.x(0)
        if s[0] == "1":
            qc.x(1)
        qc.measure([0, 1], [0, 1])
        counts = run(qc, shots, seed=100 + j, noise_model=noise_model)
        for i, t in enumerate(STATES):
            A[i, j] = counts.get(t, 0) / shots
    return A


def mitigate(counts: dict, shots: int, A: np.ndarray) -> np.ndarray:
    p_raw = np.array([counts.get(s, 0) / shots for s in STATES])
    p_mit, *_ = np.linalg.lstsq(A, p_raw, rcond=None)
    p_mit = np.clip(p_mit, 0, None)
    return p_mit / p_mit.sum()


def error_rate(probs) -> float:
    """Fraction of forbidden 01/10 outcomes for a Bell state."""
    if isinstance(probs, dict):
        total = sum(probs.values())
        return (probs.get("01", 0) + probs.get("10", 0)) / total
    return float(probs[1] + probs[2])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shots", type=int, default=8192)
    args = parser.parse_args()

    nm = build_noise_model()
    A = assignment_matrix(nm, shots=4096)
    print("Calibration (assignment) matrix A  [rows=measured, cols=prepared]:")
    for row in A:
        print("   " + "  ".join(f"{v:.3f}" for v in row))
    print()

    raw_counts = run(bell_circuit(), args.shots, seed=7, noise_model=nm)
    raw_err = error_rate(raw_counts)
    print(f"Raw noisy Bell distribution ({args.shots} shots):")
    for s in STATES:
        print(f"  {s}: {raw_counts.get(s, 0) / args.shots:6.2%}")
    print(f"  readout error rate (01+10): {raw_err:.2%}\n")

    p_mit = mitigate(raw_counts, args.shots, A)
    mit_err = error_rate(p_mit)
    print("Mitigated distribution (A^-1 applied):")
    for s, p in zip(STATES, p_mit):
        print(f"  {s}: {p:6.2%}")
    print(f"  readout error rate (01+10): {mit_err:.2%}\n")

    print(f"Error reduction: {raw_err:.2%} -> {mit_err:.2%} "
          f"({raw_err / max(mit_err, 1e-9):.1f}x lower)")
    assert mit_err < raw_err / 2, (
        f"Mitigation failed to halve the error: {raw_err:.3f} -> {mit_err:.3f}")
    print("OK - measurement-error mitigation cut the readout error "
          "by more than half.")


if __name__ == "__main__":
    main()
