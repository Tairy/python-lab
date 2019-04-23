#!/bin/bash
# {70,760},{70,820},{70, 890}
# click at {70, 890}
# if(class of UIelement = static text) and (((value of UIelement) as text) = "Edit: ") then
# display dialog winPosition
# open -a WeChat
# cliclick c:70,760 t:chiyao kp:space kp:enter

osascript <<-EOF
tell application "System Events"
  set position of first window of application process "WeChat" to {-80, 670}
  copy (click at {70, 760}) to UIelement
  if ((value of UIelement) as text) = "👶" then
    set winPosition to "70,760"
  else
    copy (click at {70, 820}) to UIelement
    if ((value of UIelement) as text) = "👶" then
      set winPosition to "70,820"
    else
      copy (click at {70, 890}) to UIelement
      if ((value of UIelement) as text) = "👶" then
        set winPosition to "70,890"
      end if
    end if
  end if
  do shell script "export WINPOSITION=" & quoted form of winPosition
end tell
EOF

echo $WINPOSITION