(function() {
    // Styles for the chat interface
    const styles = `
        .ai-chat-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 999999;
        }

        .ai-chat-container {
            width: 90%;
            max-width: 900px;
            height: 600px;
            max-height: 800px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .ai-chat-header {
            padding: 20px;
            FONT-WEIGHT: 600;
            font-size: 12px;
            color: black;
            color: black;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .ai-chat-close {
            background: none;
            border: none;
            color: white;
            cursor: pointer;
            padding: 5px;
            font-size: 24px;
            line-height: 1;
        }

        .ai-chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 16px;
            background: #f8f9fa;
        }

        .ai-message {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 12px;
            line-height: 1.4;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }

        .ai-user-message {
            background: #3d3d3d;
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 4px;
        }

        .ai-bot-message {
            background: white;
            color: #333;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
        }

        .ai-chat-input {
            padding: 20px;
            background: white;
            border-top: 1px solid #eee;
            display: flex;
            gap: 12px;
        }

        .ai-chat-input input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #eee;
            border-radius: 8px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }

        .ai-chat-input input:focus {
            border-color: #3d3d3d;
        }

        .ai-chat-input button {
            padding: 12px 24px;
            background: #3d3d3d;
            color: white;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }

        .ai-chat-input button:hover {
            background: #3d3d3d;
        }

        .ai-chat-input button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }

        .ai-typing-indicator {
            display: none;
            align-self: flex-start;
            padding: 12px 16px;
            background: white;
            border-radius: 50px;
            color: #666;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }

        .ai-typing-indicator.active {
            display: block;
        }

        .ai-status-indicator {
            display: none;
            align-items: center;
            gap: 8px;
            font-size: 14px;
        }

        .ai-status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #4CAF50;
        }

        .ai-status-dot.disconnected {
            background: #f44336;
        }
    `;

    // Create and inject styles
    const styleSheet = document.createElement('style');
    styleSheet.textContent = styles;
    document.head.appendChild(styleSheet);

    // Create chat overlay and container
    const chatHTML = `
        <div class="ai-chat-overlay">
            <div class="ai-chat-container">
                <div class="ai-chat-header">
                    <h3 style="padding-top:20px;margin:0px;">HolidayHeroes Assistant</h3>
                    <div class="ai-status-indicator">
                        <span class="ai-status-dot"></span>
                        <span class="ai-status-text">Connecting...</span>
                    </div>
                    <button class="ai-chat-close">&times;</button>
                </div>
                <div class="ai-chat-messages">
                    <div class="ai-message ai-bot-message">
                        Hello, let me help you help your client finding the best holiday for his wishes
                    </div>
                    <div class="ai-typing-indicator">
                        Assistant is typing...
                    </div>
                </div>
                <div class="ai-chat-input">
                    <input type="text" placeholder="Type your message..." />
                    <button>Send</button>
                </div>
            </div>
        </div>
    `;

    // Add chat HTML to body
    document.body.insertAdjacentHTML('beforeend', chatHTML);

    // Get DOM elements
    const elements = {
        overlay: document.querySelector('.ai-chat-overlay'),
        messages: document.querySelector('.ai-chat-messages'),
        input: document.querySelector('.ai-chat-input input'),
        button: document.querySelector('.ai-chat-input button'),
        closeButton: document.querySelector('.ai-chat-close'),
        statusDot: document.querySelector('.ai-status-dot'),
        statusText: document.querySelector('.ai-status-text'),
        typingIndicator: document.querySelector('.ai-typing-indicator')
    };

    let ws = null;

    // Show chat
    function showChat() {
        elements.overlay.style.display = 'flex';
        if (!ws) {
            connectWebSocket();
        }
        elements.input.focus();
    }

    // Hide chat
    function hideChat() {
        elements.overlay.style.display = 'none';
        if (ws) {
            ws.close();
            ws = null;
        }
    }

    // Connect to WebSocket
    function connectWebSocket() {
        const clientId = 'user_' + Math.random().toString(36).substr(2, 9);
        ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);

        ws.onopen = () => {
            elements.statusDot.classList.remove('disconnected');
            elements.statusText.textContent = 'Connected';
            elements.button.disabled = false;
        };

        ws.onclose = () => {
            elements.statusDot.classList.add('disconnected');
            elements.statusText.textContent = 'Disconnected';
            elements.button.disabled = true;
            ws = null;
        };

        ws.onerror = () => {
            elements.statusDot.classList.add('disconnected');
            elements.statusText.textContent = 'Error';
            elements.button.disabled = true;
        };

        ws.onmessage = (event) => {
            elements.typingIndicator.classList.remove('active');
            addMessage(event.data, 'bot');
        };
    }

    // Add message to chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `ai-message ai-${sender}-message`;
        if (text.includes('https')) {
            const urlRegex = /(https?:\/\/[^\s]+)/g;
            messageDiv.innerHTML = text.replace(urlRegex, '<a href="$1" target="_blank">$1</a>');
        } else {
            messageDiv.textContent = text;
        }
        elements.messages.insertBefore(messageDiv, elements.typingIndicator);
        elements.messages.scrollTop = elements.messages.scrollHeight;
    }

    // Send message
    function sendMessage() {
        const message = elements.input.value.trim();
        if (message && ws && ws.readyState === WebSocket.OPEN) {
            addMessage(message, 'user');
            ws.send(message);
            elements.input.value = '';
            elements.typingIndicator.classList.add('active');
        }
    }

    // Event listeners
    document.addEventListener('click', (e) => {
        if (e.target.matches('.btn-start')) {
            showChat();
        }
    });

    elements.closeButton.addEventListener('click', hideChat);
    elements.button.addEventListener('click', sendMessage);
    elements.input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Close on overlay click (optional)
    elements.overlay.addEventListener('click', (e) => {
        if (e.target === elements.overlay) {
            hideChat();
        }
    });
})(); 