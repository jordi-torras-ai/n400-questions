on run argv
    set inputFile to POSIX file (item 1 of argv)
    set outputFile to POSIX file (item 2 of argv)

    tell application "Numbers"
        activate
        open inputFile
        try
            set theDocument to front document
        on error errMsg number errNum
            display dialog ("Error opening document: " & errMsg & " (Error number: " & errNum & ")") buttons {"OK"} default button "OK"
            return
        end try

        try
            export theDocument to outputFile as CSV
        on error errMsg number errNum
            display dialog ("Error exporting CSV: " & errMsg & " (Error number: " & errNum & ")") buttons {"OK"} default button "OK"
        end try

        close theDocument without saving
    end tell
    tell application "Terminal"
        activate
    end tell
end run
