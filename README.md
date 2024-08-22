# Zed2API

Zed2API is a Flask-based API that serves as a proxy for the Anthropic Claude AI model. It allows users to interact with the Claude model through a simple HTTP interface.

## Features

- Supports Claude 3.5 Sonnet model (default)
- Customizable model parameters
- Streaming responses
- JWT authentication

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Zed2API.git
   cd Zed2API
   ```

2. Build and run the Docker container:
   ```
   docker build -t zed2api .
   docker run -p 8000:8000 zed2api
   ```

3. The API will be available at `http://localhost:8000/chat`.


## Usage

To use the API, send a POST request to the `/chat` endpoint with your message payload. For example:

3. The API will return a streaming response with the AI's reply.

## Environment Variables

- `HTTP_PROXY`: Set this if you need to use a proxy server for outgoing requests.

## Note

This API uses random GitHub usernames and Zed user IDs for authentication. In a production environment, you should implement proper user authentication and management.

## License

[Your chosen license]