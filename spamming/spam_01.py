from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/prompt_debug', methods=['POST', 'GET'])
def prompt_debug():
    response = ""
    if request.method == "POST":
        try:
            user_input = request.form.get('value', '').strip()
            values = user_input.split()
            if "+" in user_input:
                response = int(values[0]) + int(values[1])
            elif "-" in user_input:
                values = user_input.split("-")
                response = int(values[0]) - int(values[1])
            elif "*" in user_input:
                values = user_input.split("*")
                response = int(values[0]) * int(values[1])
            elif "/" in user_input:
                values = user_input.split("/")
                if int(values[1]) == 0:
                    response = "Error: Division by zero"
                else:
                    response = int(values[0]) / int(values[1])
            elif "%" in user_input:
                values = user_input.split("%")
                response = int(values[0]) % int(values[1])
            elif "//" in user_input:
                values = user_input.split("//")
                response = int(values[0]) // int(values[1])
            elif "**" in user_input:
                values = user_input.split("**")
                response = int(values[0]) ** int(values[1])
            else:
                response = "No valid operator found."

        except Exception as e:
            response = {
                "error": "Sorry there is some error....!"
            }

    # Handle GET method, displaying the form
    return f'''
        <h3>I am your simple calculator 🤖</h3>
        <form method="post" target="_blank">
            <input name="value" type="text" placeholder="Ask something..." style="width: 300px;">
            <input type="submit" value="Send">
        </form>
        <div style="margin-top: 20px;">
            <b>Bot:</b> {response}
        </div>
    '''

if __name__ == "__main__":
    app.run(debug=True)
