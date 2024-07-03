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

# Mock data for live555 commands
mock_live555_responses = {
    "OPTIONS": {
        "response": {
            "OPTIONS": "[{ \"OPTIONS\": \"200 OK\\r\\nPublic: OPTIONS, DESCRIBE, SETUP, PLAY, PAUSE, TEARDOWN, ANNOUNCE, GET_PARAMETER, SET_PARAMETER, REDIRECT, RECORD\\r\\n\" }]",
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 16,
                "total_tokens": 21
            }
        }
    },
    "DESCRIBE": {
        "response": {
            "DESCRIBE": "[{ \"DESCRIBE\": \"200 OK\\r\\nContent-Base: rtsp://example.com/media.mp4/\\r\\nContent-Type: application/sdp\\r\\nContent-Length: 460\\r\\n\\r\\nv=0\\r\\no=- 2890844526 2890844526 IN IP4 127.0.0.1\\r\\ns=Example Media Stream\\r\\nt=0 0\\r\\nm=video 49170 RTP/AVP 96\\r\\na=rtpmap:96 H264/90000\\r\\n\" }]",
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 30,
                "total_tokens": 35
            }
        }
    },
    "SETUP": {
        "response": {
            "SETUP": "[{ \"SETUP\": \"200 OK\\r\\nTransport: RTP/AVP;unicast;client_port=8000-8001\\r\\nSession: 12345678\\r\\n\" }]",
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 16,
                "total_tokens": 21
            }
        }
    },
    "PLAY": {
        "response": {
            "PLAY": "[{ \"PLAY\": \"200 OK\\r\\nRTP-Info: url=rtsp://example.com/media.mp4/streamid=0;seq=9810092;rtptime=3450012\\r\\nSession: 12345678\\r\\n\" }]",
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 21,
                "total_tokens": 26
            }
        }
    },
    "PAUSE": {
        "response": {
            "PAUSE": "[{ \"PAUSE\": \"200 OK\\r\\nSession: 12345678\\r\\n\" }]",
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 10,
                "total_tokens": 15
            }
        }
    },
    "TEARDOWN": {
        "response": {
            "TEARDOWN": "[{ \"TEARDOWN\": \"200 OK\\r\\nSession: 12345678\\r\\n\" }]",
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 10,
                "total_tokens": 15
            }
        }
    },
    "ANNOUNCE": {
        "response": {
            "ANNOUNCE": "[{ \"ANNOUNCE\": \"200 OK\\r\\n\" }]",
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 7,
                "total_tokens": 12
            }
        }
    },
    "GET_PARAMETER": {
        "response": {
            "GET_PARAMETER": "[{ \"GET_PARAMETER\": \"200 OK\\r\\n\" }]",
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 7,
                "total_tokens": 12
            }
        }
    },
    "SET_PARAMETER": {
        "response": {
            "SET_PARAMETER": "[{ \"SET_PARAMETER\": \"200 OK\\r\\n\" }]",
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 7,
                "total_tokens": 12
            }
        }
    },
    "REDIRECT": {
        "response": {
            "REDIRECT": "[{ \"REDIRECT\": \"200 OK\\r\\n\" }]",
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 7,
                "total_tokens": 12
            }
        }
    },
    "RECORD": {
        "response": {
            "RECORD": "[{ \"RECORD\": \"200 OK\\r\\n\" }]",
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 7,
                "total_tokens": 12
            }
        }
    }
}

# Mock data for chat/completions endpoint
mock_chat_completions = [
    {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "This is a mock response for /chat/completions."
                },
                "index": 0,
                "finish_reason": "stop"
            }
        ],
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

    # Generate the response with live555 mock responses
    live555_responses = []
    for command, response_data in mock_live555_responses.items():
        live555_responses.append({
            "message": {
                "role": "assistant",
                "content": response_data["response"][command],
            },
            "index": 0,
            "finish_reason": "stop"
        })
   
    mock_chat_completions[0]["choices"] = live555_responses

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
