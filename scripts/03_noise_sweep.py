"""
03 — Noise sweep: how depolarizing noise erodes Grover's advantage.

Runs the 2-qubit Grover circuit (marked state |11>) under depolarizing
gate noise at six error probabilities p from 0.001 to 0.05, and prints
an ASCII table of success rate vs p.

Expected shape: near-ideal success at tiny p, decaying toward the
random-guess floor (25%) as p grows. Success must stay above 90% at the
smallest p and be strictly lower at the largest p.

Readout error is excluded on purpose: this sweep isolates gate noise.

Run:
    python3 scripts/03_noise_sweep.py [--shots 2048]
"""

import argparse

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

P_VALUES = [0.001, 0.005, 0.01, 0.02, 0.03, 0.05]


def build_noise_model(p: float) -> NoiseModel:
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(depolarizing_error(p, 1), ["h", "x"])
    nm.add_all_qubit_quantum_error(depolarizing_error(2 * p, 2), ["cz"])
    return nm


def grover_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(2, 2)
    qc.h([0, 1])       # uniform superposition
    qc.cz(0, 1)        # oracle: mark |11>
    qc.h([0, 1])       # diffuser: inversion about the mean
    qc.x([0, 1])
    qc.cz(0, 1)
    qc.x([0, 1])
    qc.h([0, 1])
    qc.measure([0, 1], [0, 1])
    return qc


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shots", type=int, default=2048)
    args = parser.parse_args()

    qc = grover_circuit()
    results = []
    for k, p in enumerate(P_VALUES):
        counts = (
            AerSimulator(seed_simulator=500 + k)
            .run(qc, shots=args.shots, noise_model=build_noise_model(p))
            .result()
            .get_counts()
        )
        success = counts.get("11", 0) / args.shots
        results.append((p, success))

    print(f"Grover success rate vs depolarizing p ({args.shots} shots each):")
    print(f"  {'p':>7}   {'success':>8}   distribution")
    for p, success in results:
        bar = "#" * int(40 * success)
        print(f"  {p:>7.3f}   {success:>7.1%}   {bar}")
    print("  (random guessing would give 25%)\n")

    first = results[0][1]
    last = results[-1][1]
    assert first > 0.90, f"Too noisy at p={P_VALUES[0]}: {first:.1%}"
    assert last < first, (
        f"Success did not decay: p={P_VALUES[0]} -> {first:.1%}, "
        f"p={P_VALUES[-1]} -> {last:.1%}")
    print(f"OK — success holds at {first:.1%} for p={P_VALUES[0]} and falls "
          f"to {last:.1%} at p={P_VALUES[-1]}: noise erodes the speedup.")


if __name__ == "__main__":
    main()
