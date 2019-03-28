#!/bin/bash

#insdf="job_crossspectrum_1230044418.sdf"
insdf="job_coherence_1230044418.sdf"

jobnumber=15718
processnumber=0

outsdf=retry_$(basename $insdf)

echo " " > $outsdf

ok="Successfully finished !"

edit=True

while read x; do

    testarray=(${x})
    if test "${testarray[0]}" != "Arguments" ; then
	if [ $edit ]; then
	    echo $x >> $outsdf
	fi    
	continue
    fi

    edit=False

    log=log/out_${jobnumber}.${processnumber}.txt

    ((processnumber++))

    checkword=$(tail -n 1 $log)
    output=$(tail -n 2 $log | head -n 1)

    outls=`ls -s ${output}`
    badls="0 ${output}"
    if test "$outls" = "$badls" ;then
	echo $output " is broken !"
	ls -l ${output}
	#rm -rf ${output}
	echo $x >> $outsdf
	edit=True
    elif test "$ok" = "$checkword" ;then
	if [ -e ${output} ];then
	    echo $log " successfully finished."
	else
	    echo $output " is not found !"
	    echo $x >> $outsdf
	    edit=True
	fi
    else	
	echo $log " is not processed !"
	#rm -rf ${output}
	echo $x >> $outsdf
	edit=True
    fi
done < $insdf
