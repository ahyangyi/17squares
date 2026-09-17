#!/usr/bin/env bash
# Rejection tests: every engine must REFUSE corrupted certificates.
# (Fort's pattern: positive controls alone prove nothing if the checker
# also accepts garbage.)
set -u
cd "$(dirname "$0")"
PY=${PYTHON:-python3}
CERT=../certificate/cert_4613105_B9998_k92160.json
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
fails=0

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
}

check_refusal() {  # $1 = engine label, $2... = command
  label=$1; shift
  if "$@" > "$TMP/out.log" 2>&1; then
    echo "REJECTION-TEST FAIL: $label ACCEPTED a corrupted certificate"
    fails=1
  else
    echo "ok: $label refused as required"
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
  check_refusal "independent prefix" \
    $PY verify_independent_prefix.py $bad --stride 921 --dirs 0 92161
done

if [ $fails -eq 0 ]; then
  echo "ALL_REJECTION_TESTS_PASSED"
else
  exit 1
fi
