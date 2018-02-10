load tclrega.so

array set values [rega_script {
var v1 = dom.GetObject("Anwesenheit").Value();
var v2 = dom.GetObject("Alarmmeldungen").Value();
var v3 = dom.GetObject("Servicemeldungen").Value();
} ]

set v1 $values(v1)
set v2 $values(v2)
set v3 $values(v3)
