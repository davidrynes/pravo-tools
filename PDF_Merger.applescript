#!/usr/bin/env osascript -l AppleScript
-- PDF Merger GUI Launcher
-- Autor: David Rynes
-- Popis: Spouští PDF Merger GUI aplikaci

tell application "Finder"
    set scriptPath to POSIX path of (path to me)
    set scriptDir to POSIX path of (parent of (path to me))
end tell

-- Změnit na adresář se skriptem
do shell script "cd '" & scriptDir & "'"

-- Spustit Python aplikaci
do shell script "python3 '" & scriptDir & "PDF_Merger.py'"
