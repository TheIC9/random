from flask import Flask, request, jsonify
import pyjokes

app = Flask(__name__)


@app.route('/prompt_debug', methods=['POST', 'GET'])
def prompt_debug():
    response = ""
    facts = [
    "Bananas are berries, but strawberries aren't.",
    "Octopuses have three hearts.",
    "The Eiffel Tower can grow taller in summer due to heat expansion.",
    "Sharks existed before trees.",
    "The first computer bug was a real bug — a moth stuck in a computer in 1947.",
    "Your brain uses around 20\%\ of your body's total energy.",
    "Water can boil and freeze at the same time at its triple point.",
    "Venus rotates backward, so the Sun rises in the west there.",
    "Honey never spoils — archaeologists found 3000-year-old edible honey in tombs.",
    "All the DNA in your body can stretch from Earth to the Sun about 600 times."
]

    if request.method == "POST":
        try:
            user_input = request.form.get('value', '').strip()
            if "jokes" in user_input.lower():
                response = pyjokes.get_joke()
            elif "fact" in user_input.lower():
                response = any(word in user_input for word in facts)
            else:
                response = "Sorry i m stil learning about it..."


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
