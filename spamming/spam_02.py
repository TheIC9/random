from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/prompt_debug', methods=['POST', 'GET'])
def prompt_debug():
    response = ""
    if request.method == "POST":
        try:
            user_input = request.form.get('value', '').strip()
            values = user_input.split()
            my_dict = {}
            for word in values:
                if word in my_dict:
                    my_dict[word] +=1
                else:
                    my_dict[word] = 1
            maximum = max(my_dict,key=len)
            length = len(values)
            


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
