; File: mouseAct.ahk
; Jose Carlos Ramirez
; TFG Unizar

; Triggered when ctrl+j is pressed. Moves the mouse random and the arrow keys up and down. AutoHotKey Unicode - 32bit
; This still don't stop PaFish of "Detecting Sanbox mouse"... but even stoping the human module and moving the mouse by myself it's detected, so...

^j::
    SetDefaultMouseSpeed, 5
    x=0
    y=0
    increment=True
    sleep, 10000
    Loop 500 {	
        Random, _x, 10, 30
        Random, _y, 10, 30 
	Random, _sleep, 0,200 
	Random, _loop, 0, 10
	Random, _key, 0, 3
	Random, _press, 0, 5

	;Change the increment to decrement if we are out of the borders
	if x>800
		increment=False
	else if x<0
		increment=True
	if y>800
		increment=False
	else if y<0
		increment=True
	
	if increment=True {	
		x:=x+_x
		y:=y+_y
	}
	else {
		x:=x-_x
		y:=y-_y
	}
	sleep, %_sleep% ;Random sleep between clicks
        Click %x%, %y%, 0

	;Click sometimes
	if _press=0
		Click

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
