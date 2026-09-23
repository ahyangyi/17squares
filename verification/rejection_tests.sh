#!/usr/bin/env bash
# Rejection tests: every engine must REFUSE corrupted certificates.
# (Fort's pattern: positive controls alone prove nothing if the checker
# also accepts garbage.)
#
# Prerequisites (VERIFY.md): the two C++ binaries must be built in this
# directory (./exact_sweep and ./exact_sweep_dp), and $PYTHON must have
# numpy for engine 1 (default: python3).
#
# Expected runtime: the global-gate corruptions (mass17, vacuousB) are
# refused within seconds by every engine; engine 1's undercapture smoke
# (stride 921) takes ~10 min; engine 3's undercapture leg is targeted at
# the zeroed atom's binding directions (~45 min); the kernel aborts at
# the FIRST underweight direction, which for this corruption is already
# direction 0, so its undercapture legs take seconds.  Total ~1 hour.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PYTHON:-python3}
CERT=../certificate/cert_4613_B99985_k184320_dipfix.json
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
fails=0

[ -f "$CERT" ] || { echo "FATAL: certificate not found: $CERT"; exit 2; }
for bin in ./exact_sweep ./exact_sweep_dp; do
  [ -x "$bin" ] || { echo "FATAL: missing $bin -- build it first (VERIFY.md section 2)"; exit 2; }
done

make_bad() {  # $1 = mode, $2 = output
  $PY - "$CERT" "$1" "$2" <<'PYCODE'
import json, sys
cert = json.load(open(sys.argv[1]))
mode, out = sys.argv[2], sys.argv[3]
if mode == "mass17":            # total weight >= 17
    cert["atoms"][0][2] = int(cert["atoms"][0][2]) + 10**10
elif mode == "vacuousB":        # B failing strict containment
    cert["B"] = "999999/1000000"
elif mode == "undercapture":    # zero out the largest weight
    i = max(range(len(cert["atoms"])), key=lambda j: int(cert["atoms"][j][2]))
    cert["atoms"][i][2] = 0
json.dump(cert, open(out, "w"))
PYCODE
  [ -f "$2" ] || { echo "FATAL: make_bad $1 produced nothing"; exit 2; }
}

check_refusal() {  # $1 = engine label, $2... = command
  label=$1; shift
  set +e
  "$@" > "$TMP/out.log" 2>&1
  rc=$?
  set -e
  if [ $rc -eq 0 ]; then
    echo "REJECTION-TEST FAIL: $label ACCEPTED a corrupted certificate"
    fails=1
  else
    echo "ok: $label refused as required (exit $rc)"
  fi
}

for mode in mass17 vacuousB undercapture; do
  bad=$TMP/bad_$mode.json
  make_bad $mode $bad
  echo "--- corrupted variant: $mode ---"
  check_refusal "engine1 (verify.py)" \
    $PY verify.py $bad --stride 921
  $PY make_kernel_input.py $bad $TMP/bad_$mode.txt >/dev/null
  check_refusal "mira-acc segment tree" ./exact_sweep $TMP/bad_$mode.txt
  check_refusal "mira-acc direct prefix" ./exact_sweep_dp $TMP/bad_$mode.txt
  if [ "$mode" = undercapture ]; then
    # The zeroed (largest-weight) atom binds at directions around
    # k = 95440 (the ~25 deg razor dip): min capture there drops from
    # 1000000002/1e9 to 878019132/1e9.  A targeted window keeps this leg
    # at ~45 min instead of a full sweep.
    check_refusal "independent prefix" \
      $PY verify_independent_prefix.py $bad --dirs 95435 95445
  else
    # Global-gate corruptions are refused before any sweeping.
    check_refusal "independent prefix" \
      $PY verify_independent_prefix.py $bad --dirs 0 1
  fi
done

if [ $fails -eq 0 ]; then
  echo "ALL_REJECTION_TESTS_PASSED"
else
  exit 1
fi
