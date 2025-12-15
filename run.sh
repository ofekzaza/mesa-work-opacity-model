#!/bin/bash

# Define log file
LOG_FILE="$(pwd)/run_log.txt"

# Loop through specific 30m directories
# "30m-mlt++" "30m-normal" "30m-ours" "30m-supereduction_a=2" "30m-supereduction_a=5"
for dir in "30m-ours" "30m-supereduction_a=2" "30m-supereduction_a=5" "40m-mlt++" "40m-normal" "40m-ours" "40m-supereduction_a=2" "40m-supereduction_a=5"; do
    if [ -d "$dir" ]; then
        echo "Entering $dir" >> "$LOG_FILE"
        cd "$dir" || continue

        # Run ./mk
        CMD="./mk"
        START_TIME=$(date "+%Y-%m-%d %H:%M:%S")
        echo "Running $CMD..." >> "$LOG_FILE"
        $CMD
        MK_EXIT_CODE=$?
        END_TIME=$(date "+%Y-%m-%d %H:%M:%S")
        # Log ./mk
        echo "Folder: $dir, Command: $CMD, Start: $START_TIME, End: $END_TIME, ExitCode: $MK_EXIT_CODE" >> "$LOG_FILE"

        if [ $MK_EXIT_CODE -eq 0 ]; then
            CMD="./rn"
            START_TIME=$(date "+%Y-%m-%d %H:%M:%S")
            echo "Running $CMD..." >> "$LOG_FILE"
            $CMD
            RN_EXIT_CODE=$?
            END_TIME=$(date "+%Y-%m-%d %H:%M:%S")
            # Log ./rn
            echo "Folder: $dir, Command: $CMD, Start: $START_TIME, End: $END_TIME, ExitCode: $RN_EXIT_CODE" >> "$LOG_FILE"
        else
            echo "Skipping ./rn because ./mk failed in $dir" >> "$LOG_FILE"
            echo "Folder: $dir, Command: ./rn, Start: -, End: -, Status: SKIPPED (mk failed)" >> "$LOG_FILE"
        fi

        # Go back to parent directory
        cd ..
    fi
done
