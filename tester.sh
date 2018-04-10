#!/bin/bash

port=/dev/pts/26

sendcode(){
  echo "$1 $2" 
  echo "$1 $2" > $3;
  sleep 0.2 
}

sendcode 'LS' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'UV' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'VP' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'HP' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'AC' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'MV' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'NV' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'MH' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'NH' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'WD' $(cut -f1 -d. /proc/uptime) $port
sendcode 'FS' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'PS' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'PO' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'TI' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'TO' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'WL' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'RS' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'ST' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'HI' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'OP' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'RS' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'IN' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'VN' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'DI' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'BO' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'AI' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'U1' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'U2' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'U3' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'RP' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'CP' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'CV' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'RA' $(( ( RANDOM % 10 )  + 1 )) $port
sendcode 'IP' '1.11.1.1' $port
sendcode 'GW' '2.2.2.2' $port
sendcode 'DT' '21.3.2014' $port
sendcode 'TM' '12:23' $port
sendcode 'RT' '12:34' $port
sendcode 'RD' '2.3.2018' $port


