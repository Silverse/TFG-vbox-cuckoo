	
#B::	
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
	
	;Google search
	window_name=Mozilla Firefox Start Page - Mozilla Firefox
	Run, firefox.exe 
	WinWaitActive, %window_name%
	sleep, 1000
	Send, random search{Enter}
R
