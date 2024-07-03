import time
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Mock data for completions endpoint
mock_completions = [
    {
        "choices": [
            {
                "text": "This is a mock response for /completions.",
                "index": 0,
                "finish_reason": "length"
            }
        ],
        "usage": {
            "prompt_tokens": 5,
            "completion_tokens": 7,
            "total_tokens": 12
        }
    }
]

# Mock data for bftpd commands
mock_bftpd_responses = {
    "USER": {
        "response": {
            "message": {
                "role": "assistant",
                "content": "331 User name okay, need password.\r\n"
            },
            "index": 0,
            "finish_reason": "stop"
        },
        "usage": {
            "prompt_tokens": 5,
            "completion_tokens": 7,
            "total_tokens": 12
        }
    },
    "PASS": {
        "response": {
            "message": {
                "role": "assistant",
                "content": "230 User logged in, proceed.\r\n"
            },
            "index": 0,
            "finish_reason": "stop"
        },
        "usage": {
            "prompt_tokens": 5,
            "completion_tokens": 7,
            "total_tokens": 12
        }
    }
    # Add more bftpd commands as needed
}

# Mock data for chat/completions endpoint
mock_chat_completions = [
    {
        "choices": [],
        "usage": {
            "prompt_tokens": 5,
            "completion_tokens": 7,
            "total_tokens": 12
        }
    }
]

# Helper function to generate mock response with current time
def generate_mock_response(data, mock_choices):
    response = {
        "id": "generated-id",
        "object": "text_completion" if "text" in data else "chat.completion",
        "created": int(time.time()),
        "model": "mock-model",
        "choices": mock_choices['choices'],
        "usage": mock_choices['usage']
    }
    response.update(data)
    return response

# Route for GET /completions endpoint
@app.route('/completions', methods=['GET'])
def get_completions():
    return jsonify(mock_completions)

# Route for POST /completions endpoint
@app.route('/completions', methods=['POST'])
def post_completions():
    data = request.json  # Get JSON data from request body

    # Generate the response
    response = generate_mock_response(data, mock_completions[0])

    return jsonify(response)

# Route for GET /chat/completions endpoint
@app.route('/chat/completions', methods=['GET'])
def get_chat_completions():
    return jsonify(mock_chat_completions)

# Route for POST /chat/completions endpoint
@app.route('/chat/completions', methods=['POST'])
def post_chat_completions():
    data = request.json  # Get JSON data from request body

    # Generate the response with bftpd mock responses
    bftpd_responses = []
    for command, response_data in mock_bftpd_responses.items():
        bftpd_responses.append(response_data["response"])
    
    mock_chat_completions[0]["choices"] = [bftpd_responses]  # Wrap choices in a list

    response = generate_mock_response(data, mock_chat_completions[0])

    return jsonify(response)

# Route to print JSON data received via POST request
@app.route('/print_json', methods=['POST'])
def print_json():
    data = request.json  # Get JSON data from request body
    if not data:
        abort(400, description="No JSON data provided")
    print(data)  # Print the JSON data to the console
    return jsonify(data)  # Return the JSON data as response

# Route to return a sample JSON response for demonstration
@app.route('/view_json', methods=['GET'])
def view_json():
    sample_data = {"message": "This is a sample JSON response"}
    return jsonify(sample_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
