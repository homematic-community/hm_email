load tclrega.so

array set values [rega_script {
var v1 = dom.GetObject("EmailEmpfaenger").Value();
var v2 = dom.GetObject("EmailBetreff").Value();
var v3 = dom.GetObject("EmailText").Value();
} ]

set v1 $values(v1)
set v2 $values(v2)
set v3 $values(v3)
