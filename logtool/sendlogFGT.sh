#!/bin/bash
#echo -n "please input destination FortiAnalyzer ip:"
#read fazip
#read -p "please input FortiAnalyzer IP:" -e -i 172.0.0.6 fazip
read -p "please input FortiGate S/N(Default FGT1KC0000000001):" -e -i FGVM01TM23001638 fgtsn
fazip=172.16.1.2
# fgtsn=FGVM01TM23001638
speed=20

/fortipoc/logtool/logtool64int send -ip $fazip -dtime-now -input /fortipoc/logtool/FGVM010000097597.elog.txt.log -devid $fgtsn -speed $speed -nmsgs -1 &
/fortipoc/logtool/logtool64int send -ip $fazip -dtime-now -input /fortipoc/logtool/FGVM010000097597.tlog.172.18.0.0.log -devid $fgtsn -speed $speed -nmsgs -1 &
/fortipoc/logtool/logtool64int send -ip $fazip -dtime-now -input /fortipoc/logtool/FGVM010000097597.tlog.10.200.0.0.log -devid $fgtsn -speed $speed -nmsgs -1 &
/fortipoc/logtool/logtool64int send -ip $fazip -dtime-now -input /fortipoc/logtool/FGVM010000097597.tlog.10.100.0.0.log -devid $fgtsn -speed $speed -nmsgs -1 &
/fortipoc/logtool/logtool64int send -ip $fazip -dtime-now -input /fortipoc/logtool/IOC.tlog.txt.log -devid $fgtsn -speed $speed -nmsgs 0 &
/fortipoc/logtool/logtool64int send -ip $fazip -dtime-now -input /fortipoc/logtool/fct_vuln_elog.txt.log -devid $fgtsn -speed $speed -nmsgs 0 &
#/fortipoc/logtool/logtool64int send -ip $fazip -dtime-now -input /fortipoc/logtool/BrutteForcetoSMTP.csv.log -devid $fgtsn -speed $speed -nmsgs -1 &
/fortipoc/logtool/logtool64int send -ip $fazip -dtime-now -input /fortipoc/logtool/FGVM010000166273.tlog.log -devid $fgtsn -speed $speed -nmsgs -1 &
/fortipoc/logtool/logtool64int send -ip $fazip -dtime-now -input /fortipoc/logtool/FGVM010000166273.elog.log -devid $fgtsn -speed $speed -nmsgs -1 &

