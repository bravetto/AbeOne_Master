-- Read Messages UI - Get visible text from Messages window
-- Pattern: CLARITY × TRUTH × CONNECTION × ONE
-- ∞ AbëONE ∞

tell application "Messages"
    activate
    delay 0.5
end tell

tell application "System Events"
    tell process "Messages"
        -- Get the front window
        set frontWin to front window
        set winTitle to name of frontWin
        
        set resultText to "📱 Reading Messages Window: " & winTitle & return & return
        
        -- Try to get text from the window
        try
            -- Look for text areas or scroll areas that contain messages
            set textElements to every text field of frontWin
            set resultText to resultText & "Found " & (count of textElements) & " text fields" & return & return
            
            -- Get all text content
            repeat with textElem in textElements
                try
                    set elemText to value of textElem
                    if elemText is not "" then
                        set resultText to resultText & elemText & return & return
                    end if
                end try
            end repeat
            
            -- Also try to get text from static text elements
            set staticTexts to every static text of frontWin
            repeat with staticText in staticTexts
                try
                    set textValue to value of staticText
                    if textValue is not "" and length of textValue > 5 then
                        set resultText to resultText & textValue & return
                    end if
                end try
            end repeat
            
        on error errMsg
            set resultText to resultText & "Error reading UI: " & errMsg & return
        end try
        
        return resultText
    end tell
end tell

