
USB_DEVICE=$(lsusb | grep RTL2838)
if [[ -z $USB_DEVICE ]]; then
    echo "No RTLSDR device found!"
    exit
fi
REGEX="^Bus ([0-9]+)"

echo $USB_DEVICE =~ $REGEX
