cd oo > /dev/null
# STDOUT_OUTPUT_FROM_PROGRAM=`./turbodiag.py`
while true; do
  ./turbodiag.py > /dev/null
  RET_CODE="$?"
  echo "*** RET_CODE = ${RET_CODE}"
  if (("$RET_CODE" != "0")); then
    break
  fi
done

cd -  > /dev/null

if (("$RET_CODE" == "123")); then
  echo "*** ATENCAO: Terminou o processamento de todos os registros"
else
    echo "*** ATENCAO: Ocorreu o erro numero ${RET_CODE}"
fi

# echo ${STDOUT_OUTPUT_FROM_PROGRAM}

exit ${RET_CODE}

