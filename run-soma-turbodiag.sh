cd oo
STDOUT_OUTPUT_FROM_PROGRAM=`./turbodiag.py`
RET_CODE="$?"
echo "RET_CODE = $?"
cd -
exit ${RET_CODE}
