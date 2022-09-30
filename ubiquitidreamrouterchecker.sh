#!/bin/sh

twilio_number="+11234567890"
your_number="+11234567890"
account_sid="XXX"
auth_token="XXX"

sendAlertSMS()
{
    echo $(date -u) "Send SMS to $your_number"
    curl -X POST -d "Body=Dream Router is in stock! https://store.ui.com/collections/unifi-network-unifi-os-consoles/products/dream-router" \
        -d "From=${twilio_number}" -d "To=${your_number}" \
        "https://api.twilio.com/2010-04-01/Accounts/${account_sid}/Messages" \
        -u "${account_sid}:${auth_token}"
}

makeAlertCall()
{
    echo $(date -u) "Call $your_number"
    curl -X POST https://api.twilio.com/2010-04-01/Accounts/${account_sid}/Calls.json \
    --data-urlencode "Url=https://handler.twilio.com/twiml/EHcb8906a22908e88b559a0a2f01d896a6" \
    --data-urlencode "To=${your_number}" \
    --data-urlencode "From=${twilio_number}" \
    -u ${account_sid}:${auth_token}
}

echo $(date -u) "Start to track"

while true
do
    if curl -s 'https://store.ui.com/collections/unifi-network-unifi-os-consoles/products/dream-router' | grep -q 'In Stock</span>'; then
        echo $(date -u) "Yes, in stock!"
        sendAlertSMS
        makeAlertCall
        echo $(date -u) "Check again in 3600 seconds = 60 mins"
        sleep 3600
    else
        echo $(date -u) "No, not in stock. Check again in 60 seconds"
        sleep 60
    fi
done