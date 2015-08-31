; File: humanMimic.ahk
; Jose Carlos Ramirez
; TFG unizar

; This automates some common tasks to mimic a human user, BUT sometimes it crashes a little bit D:
; SOME NAMES ARE IN SPANISH AND WILL NOT WORK IN A NON SPANISH SYSTEM


#A::
    loop_size=1000 ;for the mouse activity       
	;Wait until the sample is ready
	MsgBox, Human-Mimic running (7 seconds countdown)
	Sleep, 7000
	
	;Gmail
	web=http://www.gmail.com
	window_name=Gmail - Mozilla Firefox
	sleep, 1000
	Username=ejemplomail55
	Password=mailejemplo
	
	Run, firefox.exe %web%, ,Max
	WinWaitActive, %window_name%
	sleep, 2000
	StatusBarWait, Done, , , %window_name%
	Send, %Username%{Enter}
	sleep, 3000
	Send, %Password%{Enter}
	
	web=https://mail.google.com/mail/#inbox?compose=new
	window_name=Recibidos - ejemplomail55@gmail.com - Gmail - Mozilla Firefox
	WinWaitActive, %window_name%
	sleep, 1000
	StatusBarWait, Done, , , %window_name%
	Run, firefox.exe %web%, ,Max


	;Facebook
	web=https://www.facebook.com/login.php?email=ejemplomail55@gmail.com
	window_name=Log into Facebook | Facebook - Mozilla Firefox
	sleep, 3000
	Password=mailejemplo
	
	Run, firefox.exe %web%, ,Max
	WinWaitActive, %window_name%
	sleep, 1000
	StatusBarWait, Done, , , %window_name%
	Send, {Tab}{Tab}%Password%{Enter}

	;
	;Youtube
	web=https://www.youtube.com/watch?v=Rb0UmrCXxVA
	Run, firefox.exe %web%, ,Max
	WinWaitActive, %window_name%
	sleep, 1000
	StatusBarWait, Done, , , %window_name%


	;Doc
	Random, ZZ,100,500
	window_name=Sin título - Bloc de notas
	Run, notepad.exe 
	WinWaitActive, %window_name%
	sleep, 1000
	Send, random text{Enter}testtest
	Sleep, 500
	Send, {Control down}g{Control up}
	Sleep, 500
	Send, something%ZZ%.txt
	Sleep, 500
	Send, {Enter}
	WinClose, something%ZZ% - Bloc de notas
	
	;Navigate folders
	Run, explorer.exe 
	Sleep, 500
	Send, {Tab}	
	Sleep, 500
	Send, {Down down}{Down up}
	Sleep, 500
	Send, {Down down}{Down up}
	Sleep, 500
	Send, {Down down}{Down up}
	Sleep, 500
	Send, {Down down}{Down up}
	Sleep, 500
	Send, {Right down}{Right up}
	Sleep, 500
	Send, {Control down}c{Control up}
	Sleep, 500
	Send, {Control down}v{Control up}
	Sleep, 500
	Send, {Right down}{Right up}
	Sleep, 500
	Send, {Del}	
	Sleep, 500
	Send, {Enter}

	;Google search
	window_name=Mozilla Firefox Start Page - Mozilla Firefox
	Run, firefox.exe 
	WinWaitActive, %window_name%
	sleep, 1000
	Send, random search{Enter}
	
	;Random mouse moves, and some keystrokes
	SetDefaultMouseSpeed, 5
        x=0
        y=0
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
            if x>800
                    increment=False
            else if x<0
                    increment=True
            if y>800
                    increment=False
            else if y<0
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
Return 
 
