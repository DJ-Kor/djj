import requests


def func_post(url=None, data=None):
    r = requests.post(url=url, data=data)
    print(r.headers)
    print(r.status_code, r.reason)
    print(r.text)


TEAMS = 'https://prod2-00.southeastasia.logic.azure.com:443/workflows/91a8df9d12114f1db657f3ca0c74785e/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=HxpRDHG7M_qpIwtxIsC__SAMX0-C6iO5rifsilHkAp8'
data = {
    "type": "object",
    "properties": {
        "type": {
            "type": "string"
        },
        "attachments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "contentType": {
                        "type": "string"
                    },
                    "content": {
                        "type": "object",
                        "properties": {
                            "$schema": {
                                "type": "string"
                            },
                            "type": {
                                "type": "string"
                            },
                            "version": {
                                "type": "string"
                            },
                            "body": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "type": {
                                            "type": "string"
                                        }
                                    },
                                    "required": [
                                        "type"
                                    ]
                                }
                            }
                        }
                    }
                },
                "required": [
                    "contentType",
                    "content"
                ]
            }
        }
    }
}

data2 = {
    "type": "message",
    "attachments": [
        {
            "contentType": "application/json",
            "content": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.0",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": "Hello, World!"
                    }
                ]
            }
        }
    ]
}
func_post(url=TEAMS, data=data2)