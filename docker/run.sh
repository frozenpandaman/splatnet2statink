#!/bin/bash

# Parameters (DO NOT MODIFIY!)

INTERVAL=120            # Interval (min) for running
RETRY_INTERVAL=5        # Interval (min) for temporary errors.  
RETRIES=3               # Maximum retry count for temporary errors
UPDATE_INTERVAL=86400   # Inerval (sec) for automatic update. one time/day
WORKDIR=`dirname $0`

# Initialization
last_update_time=0

cd $WORKDIR
[ -e ./run.conf ] && source ./run.conf


# Create config.txt
write_config() {
    cat > config.txt <<__EOF__
{
    "api_key": "${STATINK_API_KEY}",
    "cookie": "${IKSM_SESSION}",
    "user_lang": "${USER_LANG}"
}
__EOF__
}


# Get latest splatnet2statink from git origin
self_update() {
    local current_time
    local d

    [ -e .git ] || return

    current_time=`/bin/date +%s`

    d=$((${current_time} - ${last_update_time}))
    [ ${d} -lt ${UPDATE_INTERVAL} ] && return

    echo Updating splatnet2statink
    git pull
    last_update_time=${current_time}
}


# Main
main() {
    local errorcode
    local retry
    retry=0

    # Write config once.
    write_config

    while true; do
        # Try self-update
        self_update

        # Run!
        python splatnet2statink.py -r
        errorcode=$?

        if [ ${errorcode} -eq 1 ]; then
            # permanent error
            echo "Permanent error. Exiting"

            exit 1

        elif [ ${errorcode} -eq 2 ]; then
            # temporary error

            retry=$((${retry} + 1))
            echo "try ${retry} of ${RETRIES}"

                if [ ${retry} -ge ${RETRIES} ]; then
                    echo "maximum retry count exceeded."

                else
                    echo "Next retry run in ${RETRY_INTERVAL} minutes later"
                    sleep $((${RETRY_INTERVAL} * 60))
                    continue
                fi

        elif [ ${errorcode} -eq 3 ]; then
            echo "stat.ink API key is invalid"

            # ToDo: stop running, until the user provides the new IKSM session
            # Now we finish the container
            exit 1

        elif [ ${errorcode} -eq 4 ]; then
            echo "stat.ink API key is invalid"

            # ToDo: stop running, until the user provides the new IKSM session
            # Now we finish the container
            exit 1
            
        elif [ ${errorcode} -ne 0 ]; then
            # unexpected exitcode.
            echo "Unexpected exitcode. Exiting"
            exit 1

        fi
        retry=0
        echo "Next run in ${INTERVAL} minutes later"
        sleep $((${INTERVAL} * 60))
    done
}


main
