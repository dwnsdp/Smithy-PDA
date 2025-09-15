from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Store the current pending command globally (in a real app, use a proper database)
pending_command = None

@app.route('/')
def serve_html():
    """Serve the main HTML file"""
    return send_from_directory('.', 'smithy.html')

@app.route('/run', methods=['POST'])
def run():
    """Main endpoint that processes user input and returns JSON response"""
    global pending_command

    try:
        data = request.get_json()
        user_input = data.get('user_input', '').strip()

        if not user_input:
            return jsonify({
                "Message": "Please enter a message",
                "Command": None
            })

        # Simple example logic - you'd replace this with your actual AI/processing
        if 'email' in user_input.lower():
            # Extract email details (this is just a simple example)
            pending_command = {
                "Command": "email",
                "Action": "send",
                "To": ["user@example.com"],  # You'd extract this from user_input
                "Subject": "Message from Smithy",
                "Body": f"User said: {user_input}"
            }

            response = {
                "Message": f"I'll help you send an email: {user_input}",
                "Command": pending_command
            }

        elif 'weather' in user_input.lower():
            pending_command = {
                "Command": "weather",
                "Action": "get",
                "Location": "London",  # You'd extract this from user_input
                "Units": "celsius"
            }

            response = {
                "Message": f"I'll check the weather for you: {user_input}",
                "Command": pending_command
            }

        elif 'file' in user_input.lower() and 'create' in user_input.lower():
            pending_command = {
                "Command": "file",
                "Action": "create",
                "Path": "/tmp/example.txt",  # You'd extract this from user_input
                "Content": user_input
            }

            response = {
                "Message": f"I'll create a file: {user_input}",
                "Command": pending_command
            }

        else:
            # No command needed, just a response
            response = {
                "Message": f"I understand you said: {user_input}",
                "Command": None
            }

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "Message": f"Error processing request: {str(e)}",
            "Command": None
        }), 500

@app.route('/confirm', methods=['POST'])
def confirm():
    """Handle command confirmation"""
    global pending_command

    try:
        if not pending_command:
            return jsonify({
                "Message": "No command to confirm",
                "Command": None
            })

        # Execute the command (this is where you'd do the actual work)
        command_type = pending_command.get('Command')
        action = pending_command.get('Action')

        if command_type == 'email' and action == 'send':
            # Here you'd actually send the email
            to_address = ', '.join(pending_command.get('To', []))
            subject = pending_command.get('Subject', '')
            body = pending_command.get('Body', '')

            # Simulate sending email (replace with actual email sending code)
            print(f"SENDING EMAIL:")
            print(f"To: {to_address}")
            print(f"Subject: {subject}")
            print(f"Body: {body}")

            message = f"✅ Email sent successfully to {to_address}"

        elif command_type == 'weather' and action == 'get':
            # Here you'd actually fetch weather data
            location = pending_command.get('Location', '')

            # Simulate weather API call (replace with actual weather API)
            print(f"FETCHING WEATHER FOR: {location}")

            message = f"🌤️ Weather for {location}: 22°C, partly cloudy"

        elif command_type == 'file' and action == 'create':
            # Here you'd actually create the file
            path = pending_command.get('Path', '')
            content = pending_command.get('Content', '')

            # Simulate file creation (replace with actual file operations)
            print(f"CREATING FILE: {path}")
            print(f"Content: {content}")

            message = f"📁 File created successfully at {path}"

        else:
            message = f"✅ Command executed: {command_type} {action}"

        # Clear the pending command
        pending_command = None

        return jsonify({
            "Message": message,
            "Command": None
        })

    except Exception as e:
        return jsonify({
            "Message": f"Error executing command: {str(e)}",
            "Command": None
        }), 500

@app.route('/deny', methods=['POST'])
def deny():
    """Handle command denial"""
    global pending_command

    try:
        if not pending_command:
            return jsonify({
                "Message": "No command to deny",
                "Command": None
            })

        command_type = pending_command.get('Command')
        action = pending_command.get('Action')

        # Clear the pending command
        pending_command = None

        return jsonify({
            "Message": f"❌ Command cancelled: {command_type} {action}",
            "Command": None
        })

    except Exception as e:
        return jsonify({
            "Message": f"Error cancelling command: {str(e)}",
            "Command": None
        }), 500

if __name__ == '__main__':
    print("🔧 Smithy Server Starting...")
    print("📱 Open your browser to: http://localhost:5000")
    print("🚀 Ready to process commands!")

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True  # Remove this in production
    )
