; File: humanMimic.ahk
; Jose Carlos Ramirez
; TFG unizar

; This automates some common tasks to mimic a human user
; SOME NAMES ARE IN SPANISH AND WILL NOT WORK IN A NON SPANISH SYSTEM

#A::
	SetDefaultMouseSpeed, 5
	          	
	MsgBox, Human-Mimic running (7 seconds countdown)
	Sleep, 7000 ;Wait until the sample is +- ready
	Click 0,0
	
	useNotepad()	
	mouseMoving(10)
	navigateFolders()		
	mouseMoving(10)	
	fbLogin()
	mouseMoving(10)	
	outlookLogin()
	mouseMoving(10)
	searchGoogle()
	mouseMoving(1000)	
	
return

;;;; Functions
searchGoogle()
{
	web_browser:=ComObjCreate("InternetExplorer.Application")
	web_browser.visible:=true
	web_browser.ToolBar:=false
	url:="https://www.google.es/search?q=hi"
	search:="busqueda de ejemplo"

	web_browser.navigate(url)
	while web_browser.busy
		sleep 100
	return
} 
 
outlookLogin()
{
	web_browser:=ComObjCreate("InternetExplorer.Application")
	web_browser.visible:=true
	web_browser.ToolBar:=false
	user:="petparker55@outlook.es"
	pass:="Ejemplomail"	
	url:="https://login.live.com"
	
	web_browser.navigate(url)
	while web_browser.busy
		sleep 100
		
	user_input:=web_browser.document.getElementById("i0116")
	pass_input:=web_browser.document.getElementById("i0118")
	submit_button:=web_browser.document.getElementById("idSIButton9")
	
	user_input.value:=user
	pass_input.value:=pass
	submit_button.click()	
	while web_browser.busy
		sleep 100
	return
} 
 
fbLogin()
{
	web_browser:=ComObjCreate("InternetExplorer.Application")
	web_browser.visible:=true
	web_browser.ToolBar:=false
	user:="ejemplomail55@gmail.com"
	pass:="mailejemplo"
	url:="https://www.facebook.com/login.php"
	
	web_browser.navigate(url)
	while web_browser.busy
		sleep 100
		
	user_input:=web_browser.document.getElementById("email")
	pass_input:=web_browser.document.getElementById("pass")
	submit_button:=web_browser.document.getElementById("u_0_2")
	
	user_input.value:=user
	pass_input.value:=pass
	submit_button.click()	
	while web_browser.busy
		sleep 100
	return
} 

useNotepad()
{
	Random, ZZ,100,500
	window_name=Sin título - Bloc de notas
	Run, notepad.exe 
	WinWaitActive, %window_name%
	sleep, 1000
	Send, random text{Enter}testtest
	Sleep, 250
	Send, {Control down}g{Control up}
	Sleep, 250
	Send, something%ZZ%.txt
	Sleep, 250
	Send, {Enter}
	WinClose, something%ZZ% - Bloc de notas
	return
} 

navigateFolders()
{
	Run, explorer.exe 
	Sleep, 250
	Send, {Tab}	
	Sleep, 250
	Send, {Down down}{Down up}
	Sleep, 250
	Send, {Down down}{Down up}
	Sleep, 250
	Send, {Down down}{Down up}
	Sleep, 250
	Send, {Down down}{Down up}
	Sleep, 250
	Send, {Right down}{Right up}
	Sleep, 250
	Send, {Control down}c{Control up}
	Sleep, 250
	Send, {Control down}v{Control up}
	Sleep, 250
	Send, {Right down}{Right up}
	Sleep, 250
	Send, {Del}	
	Sleep, 250
	Send, {Enter}
	return
}

;Random mouse moves, left/rigth clicks, and some keystrokes
mouseMoving(loop_size) 
{		
	MouseGetPos, x, y
	increment=True
	
	Loop %loop_size%
	{	
		Random, _x, 10, 30
		Random, _y, 10, 30 
		Random, _sleep, 0,200 
		Random, _loop, 0, 10
		Random, _key, 0, 3
		Random, _press, 0, 10

		;Change the increment to decrement if we are out of the borders
		if x>750
			increment=False
		else if x<50
			increment=True
		if y>750
			increment=False
		else if y<50
			increment=True
		
		if increment=True 
		{	
			x:=x+_x
			y:=y+_y
		}
		else 
		{
			x:=x-_x
			y:=y-_y
		}
		sleep, %_sleep% ;Random sleep between clicks
		Click %x%, %y%, 0
		
		;Clicks sometimes
		if _press=0 
			Click
		if _press=1
			Click right %x%, %y%
		
		;Randomize which key to press between this 4
		if _key=0 					
			Loop %_loop% {
				Send {Up down} ;press up row
				Send {Up up} ;release up row
			}			
		else if _key=1 
			Loop %_loop% {
				Send {Down down} ;press up row
				Send {Down up} ;release up row
			}			
		else if _key=2 
			Loop %_loop% {
				Send {Control down} ;press up row
				Send {Control up} ;release up row
			}		 
		else if _key=3 
			Loop %_loop% {
				Send {LShift down} ;press up row
				Send {LShift up} ;release up row
			}		 
	}
	return
}
