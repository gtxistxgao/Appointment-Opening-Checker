#!/bin/sh

sendAlertSMS()
{
    account_sid="xxxxxx"
    auth_token="xxxxxx"

    twilio_number="+14256544791"
    your_number="+15155986420"

    echo $(date -u) "Send SMS to $your_number"
    curl -X POST -d "Body=Dream Router is in stock!" \
        -d "From=${twilio_number}" -d "To=${your_number}" \
        "https://api.twilio.com/2010-04-01/Accounts/${account_sid}/Messages" \
        -u "${account_sid}:${auth_token}"
}

echo $(date -u) "Start to track"

while true
do
    if curl -s 'https://store.ui.com/collections/unifi-network-unifi-os-consoles/products/dream-router' | grep -q 'In Stock</span>'; then
        echo $(date -u) "Yes, in stock!"
        sendAlertSMS
        echo $(date -u) "Check again in 3600 seconds = 60 mins"
        sleep 3600
    else
        echo $(date -u) "No, not in stock. Check again in 60 seconds"
        sleep 60
    fi
done

