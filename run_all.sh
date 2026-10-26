#!/usr/bin/env bash
# Runs every implementation in order.
set -euo pipefail
cd "$(dirname "$0")"

# Prefer the project's venv (where qiskit lives); fall back to python3.
if [ -x ".venv/bin/python" ]; then
  PY=".venv/bin/python"
else
  PY="python3"
fi

echo "=== 01 - Ideal vs noisy Bell state ==="
$PY scripts/01_ideal_vs_noisy.py
echo
echo "=== 02 - Readout-error mitigation ==="
$PY scripts/02_readout_mitigation.py
echo
echo "=== 03 - Depolarizing noise sweep on Grover ==="
$PY scripts/03_noise_sweep.py
echo
echo "All three implementations completed successfully."
