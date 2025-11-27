tell application "Messages"
    set resultText to ""
    repeat with aService in services
        try
            set serviceType to service type of aService
            repeat with aBuddy in buddies of aService
                try
                    set buddyName to name of aBuddy
                    set buddyId to id of aBuddy
                    if buddyName contains "jimmy" or buddyName contains "Jimmy" then
                        set resultText to resultText & buddyName & " | " & buddyId & " | " & serviceType & return
                    end if
                end try
            end repeat
        end try
    end repeat
    return resultText
end tell

