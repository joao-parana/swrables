cd oo
# STDOUT_OUTPUT_FROM_PROGRAM=`./turbodiag.py`
while true; do
  ./turbodiag.py
  RET_CODE="$?"
  echo "RET_CODE = $?"
  if (("$RET_CODE" != "0")); then
    echo "Ocorreu um erro ou terminou o processamento de todos os registros"
    break
  fi
done

cd -

if (("$RET_CODE" != "127")); then
  echo "Terminou o processamento de todos os registros"
  break
fi

# echo ${STDOUT_OUTPUT_FROM_PROGRAM}

exit ${RET_CODE}

