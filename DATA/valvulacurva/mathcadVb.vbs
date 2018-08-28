Set sh = WScript.CreateObject("WScript.Shell")
sh.AppActivate("Mathcad - [flu_valvulacurva.xmcd]")
sh.SendKeys "{F10}"
sh.SendKeys "W"
sh.SendKeys "1"
WScript.Sleep(3000)
sh.SendKeys "{F10}"
sh.SendKeys "T"
sh.SendKeys "C"
sh.SendKeys "W"
