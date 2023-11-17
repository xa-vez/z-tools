#!/bin/bash

set -e 

## Path to devices running Rail Test
SERIAL_RAIL_TEST="/dev/ttyACM2"

FREQ_US_CH0="916000000"
FREQ_US_CH1="908400000"
FREQ_US_CH2="908400000"

CHANNEL=${FREQ_US_CH1}

TOGGLE_TONE_FREQ=5

# Setup rail_test
echo "reset" > "${SERIAL_RAIL_TEST}"
sleep 1
echo "rx 0" > "${SERIAL_RAIL_TEST}"
sleep 0.5
echo "setDebugMode 1" > "${SERIAL_RAIL_TEST}"
sleep 0.5
echo "freqOverride ${CHANNEL}" > "${SERIAL_RAIL_TEST}"
sleep 0.5

function activate_radio_tone {
  echo "$(date): Activating radio tone"
  echo "setTxTone 1" > "${SERIAL_RAIL_TEST}"
}

function deactivate_radio_tone {
  echo "$(date): Deactivating radio tone"
  echo "setTxTone 0" > "${SERIAL_RAIL_TEST}"
}

function loop_radio_tone {
  while true
  do
    echo "$(date): Activating radio tone  ${CHANNEL}"
    echo "setTxTone 1" > "${SERIAL_RAIL_TEST}"
    sleep ${TOGGLE_TONE_FREQ}
    echo "$(date): Deactivating radio tone ${CHANNEL}"
    echo "setTxTone 0" > "${SERIAL_RAIL_TEST}"
    sleep ${TOGGLE_TONE_FREQ}
  done
}

echo -e "Initializing..."
loop_radio_tone
