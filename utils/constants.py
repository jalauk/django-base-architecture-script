class Constant:

    django_default_codes = {
        "required": 508,
        "blank": 508,
        "null": 508,
        "empty": 508,
    }

    response_messages = {
        500: "Internal server error.",
        501: "The requested API endpoint is not valid.",
        502: "The provided data is not in a valid JSON format.",
        503: "The 'Content-Type' header should be set to 'application/json'.",
        504: "User authentication failed.",
        505: "The requested HTTP method is not allowed.",
        506: "Sorry, you are not authorized to perform this action.",
        507: "Invalid parameter value provided.",
        508: "Required parameter or value is missing.",
        509: "User access token is expired or invalid.",
        510: "Your daily quota has been exhausted. Please try again later.",

        100: "wrking"
    }
