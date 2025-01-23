import requests
import time
def get_next_id(collection):
    last_campaign = collection.find_one(sort=[("_id", -1)])
    next_id = 1 if last_campaign is None else last_campaign['_id'] + 1
    return next_id


def send_whatsapp_message(number, first_name, language, country_code, yacht_details, channel_id, api_token):
    """
    Create a contact and send a WhatsApp message via Respond.io API.

    Args:
        number (str): Phone number of the contact.
        first_name (str): First name of the contact.
        language (str): Language code (e.g., 'en').
        country_code (str): Country code (e.g., 'BD').
        yacht_details (dict): Dictionary containing yacht details such as name, guest name, date, time, etc.
        channel_id (int): Channel ID for sending the message.
        api_token (str): Bearer token for API authentication.

    Returns:
        dict: Response from the message sending API.
    """
    # Create contact URL and payload
    contact_url = f"https://api.respond.io/v2/contact/phone:{number}"
    contact_payload = {
        "firstName": first_name,
        "phone": number,
        "language": language,
        "countryCode": country_code,
        "custom_fields": []
    }

    # Headers for the API
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    # Create the contact
    response = requests.post(contact_url, json=contact_payload, headers=headers)
  
    #print("Contact created successfully:", response.json())

    # Wait before sending the message
    time.sleep(2)

    # Message URL and payload
    message_url = f"https://api.respond.io/v2/contact/phone:{number}/message"
    message_payload = {
        "message": {
            "type": "whatsapp_template",
            "template": {
                "name": "inquiry",
                "components": [
                    {
                        "type": "body",
                        "text": "Greetings from *Seven Yachts*\n\nWe would like to acknowledge the receipt of your inquiry:\nYacht Name: {{1}} \nGuest Name: {{2}} \nPhone Number: {{3}} \nDate: {{4}} \nTime: {{5}} \nCharter Length: {{6}} \n\nYou will receive an official quotation shortly.",
                        "parameters": [
                            {"type": "text", "text": yacht_details.get("yacht_name")},
                            {"type": "text", "text": yacht_details.get("name")},
                            {"type": "text", "text": yacht_details.get("phone")},
                            {"type": "text", "text": yacht_details.get("date")},
                            {"type": "text", "text": yacht_details.get("time")},
                            {"type": "text", "text": yacht_details.get("charterLength")}
                        ]
                    }
                ],
                "languageCode": "en"
            }
        },
        "channelId": channel_id
    }

    # Send the message
    message_response = requests.post(message_url, headers=headers, json=message_payload)

    if message_response.status_code == 200:
        #print("Message sent successfully:", message_response.json())
        return message_response.json()
    else:
        #print("Failed to send message:", message_response.json())
        return {"error": "Failed to send message", "details": message_response.json()}
