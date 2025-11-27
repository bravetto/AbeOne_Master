-- Read Messages with Jimmy
-- Pattern: CLARITY × TRUTH × CONNECTION × ONE
-- ∞ AbëONE ∞

tell application "Messages"
    set resultText to ""
    set messageCount to 0
    
    -- Find Jimmy's contact
    repeat with aService in services
        try
            repeat with aBuddy in buddies of aService
                try
                    set buddyName to name of aBuddy
                    if buddyName contains "jimmy" or buddyName contains "Jimmy" or buddyName contains "jim" or buddyName contains "Jim" then
                        set buddyId to id of aBuddy
                        set resultText to resultText & "📱 Found: " & buddyName & " (" & buddyId & ")" & return & return
                        
                        -- Get chat with this buddy
                        set targetChat to chat id buddyId of aService
                        
                        -- Get messages from the chat
                        set chatMessages to messages of targetChat
                        set messageCount to count of chatMessages
                        
                        resultText to resultText & "💬 Total messages: " & messageCount & return & return
                        
                        -- Get last 50 messages
                        set messageLimit to 50
                        if messageCount < messageLimit then
                            set messageLimit to messageCount
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
                            end try
                        end repeat
                        
                        return resultText
                    end if
                end try
            end repeat
        end try
    end repeat
    
    return "⚠️ Could not find Jimmy in Messages"
end tell

