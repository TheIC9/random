from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/prompt_debug', methods=['POST', 'GET'])
def prompt_debug():
    response = ""
    if request.method == "POST":
        try:
            user_input = request.form.get('value', '').strip()
            if "memory" in user_input:
                with open("file.txt") as f:
                    content = f.readlines()[-10:]
                    response = content
            


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
