-- Read Current Jimmy Conversation from Messages App
-- Pattern: CLARITY × TRUTH × CONNECTION × ONE
-- ∞ AbëONE ∞

tell application "Messages"
    activate
    delay 0.5
    
    -- Get the frontmost window (should be Jimmy's conversation)
    set frontWindow to front window
    
    -- Try to get messages from the current chat
    try
        set currentChat to frontWindow's chat
        set chatMessages to messages of currentChat
        
        set resultText to "💬 Current Conversation with Jimmy:" & return & return
        set resultText to resultText & "Total messages in view: " & (count of chatMessages) & return & return
        set resultText to resultText & "=" & return & return
        
        -- Get all visible messages (or last 100)
        set messageLimit to 100
        if (count of chatMessages) < messageLimit then
            set messageLimit to count of chatMessages
        end if
        
        repeat with i from 1 to messageLimit
            try
                set msg to item i of chatMessages
                set msgText to content of msg
                set msgDate to date sent of msg
                set msgSender to name of sender of msg
                
                set resultText to resultText & "[" & msgDate & "] " & msgSender & ":" & return
                set resultText to resultText & "  " & msgText & return
                set resultText to resultText & return
            on error errMsg
                -- Skip messages we can't read
            end try
        end repeat
        
        return resultText
    on error errMsg
        return "⚠️ Could not read conversation: " & errMsg
    end try
end tell

