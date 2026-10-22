"""
01 — Ideal vs noisy: what quantum noise does to a Bell state.

Runs the same Bell-state circuit twice on Qiskit Aer:
  * ideal: noise-free simulator -> perfect 00/11 correlation.
  * noisy: a realistic noise model (depolarizing gate errors +
    readout errors) -> correlation degrades and 01/10 outcomes appear.

This is a simulator noise model, not a real hardware run: it shows the
kind of degradation real devices exhibit, in a controlled,
reproducible setting.

Run:
    python3 scripts/01_ideal_vs_noisy.py [--shots 4096]
"""

import argparse

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError

P_1Q = 0.01          # depolarizing probability, 1-qubit gates
P_2Q = 0.02          # depolarizing probability, 2-qubit gates
READOUT = [[0.96, 0.04],   # P(measure 0|prepared 0)=0.96 ...
           [0.06, 0.94]]   # P(measure 1|prepared 1)=0.94


def build_noise_model() -> NoiseModel:
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(depolarizing_error(P_1Q, 1), ["h", "x"])
    nm.add_all_qubit_quantum_error(depolarizing_error(P_2Q, 2), ["cx"])
    nm.add_all_qubit_readout_error(ReadoutError(READOUT))
    return nm


def bell_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc


def histogram(counts: dict, shots: int) -> str:
    lines = []
    for outcome in sorted(counts):
        bar = "#" * int(40 * counts[outcome] / shots)
        lines.append(f"  {outcome}  {counts[outcome]:>5}  {bar}")
    return "\n".join(lines)


def correlation(counts: dict, shots: int) -> float:
    return (counts.get("00", 0) + counts.get("11", 0)) / shots


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shots", type=int, default=4096)
    args = parser.parse_args()

    qc = bell_circuit()

    ideal_counts = (
        AerSimulator(seed_simulator=1).run(qc, shots=args.shots).result().get_counts()
    )
    noisy_counts = (
        AerSimulator(seed_simulator=2)
        .run(qc, shots=args.shots, noise_model=build_noise_model())
        .result()
        .get_counts()
    )

    ideal_corr = correlation(ideal_counts, args.shots)
    noisy_corr = correlation(noisy_counts, args.shots)

    print(f"Ideal Bell state ({args.shots} shots):")
    print(histogram(ideal_counts, args.shots))
    print(f"  correlation: {100 * ideal_corr:.2f}%\n")

    print(f"Noisy Bell state ({args.shots} shots, "
          f"depolarizing 1q={P_1Q} 2q={P_2Q}, readout 4-6%):")
    print(histogram(noisy_counts, args.shots))
    print(f"  correlation: {100 * noisy_corr:.2f}% "
          f"(degraded by {100 * (ideal_corr - noisy_corr):.2f} points)\n")

    assert ideal_corr == 1.0, "Ideal simulator should correlate perfectly!"
    assert noisy_corr < 1.0, "Noise model had no effect?!"
    assert noisy_corr > 0.80, f"Noise unrealistically strong: {noisy_corr}"
    print("OK — ideal correlation is 100%; the noise model degrades it, "
          "as real hardware would.")


if __name__ == "__main__":
    main()
