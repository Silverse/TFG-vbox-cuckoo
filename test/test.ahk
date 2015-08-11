;Test AutoHotKey file, triggered with ctrl+j

^j::
	MouseGetPos, _x, _y
	Loop 5 {
		Loop 5
			Click WheelUp
		_x:=_x+100
		_y:=_y+100
		Click %_x%, %_y%, 0 ;0 clicks, just move it
		sleep, 1000 ;1sec	
	}
