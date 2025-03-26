# OpenAI Assistant Bot

This is a WebSocket-based bot that integrates with OpenAI's Assistant API to process client messages and trigger functions when needed.

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   ```
4. Edit the `.env` file with your OpenAI API key and Assistant ID

## Running the Bot

To start the bot, run:
```bash
python bot.py
```

The bot will start on `http://localhost:8000` and listen for WebSocket connections.

## WebSocket Connection

Connect to the WebSocket endpoint using:
```
ws://localhost:8000/ws/{client_id}
```

Where `{client_id}` is a unique identifier for each client session.

## How it Works

1. When a client connects, a new conversation thread is created
2. Each message from the client is sent to the OpenAI Assistant
3. The Assistant processes the message and can:
   - Respond with text
   - Trigger functions (tools) when needed
4. The response is sent back to the client through the WebSocket connection

## Example Client Usage

Here's a simple example of how to connect to the bot using JavaScript:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/user123');

ws.onopen = () => {
    console.log('Connected to bot');
    ws.send('Hello, how can you help me?');
};

ws.onmessage = (event) => {
    console.log('Received:', event.data);
};

ws.onerror = (error) => {
    console.error('WebSocket error:', error);
};
``` 