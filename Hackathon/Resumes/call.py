from flask import Flask, request, redirect, url_for

app = Flask(__name__)

@app.route('/response', methods=['GET', 'POST'])
def extractor():
    if request.method == 'POST':
        verify = request.form.get('verify')
        reason = request.form.get('reason')
        return redirect(url_for('results', status=verify, reason=reason))
    return '''
        <form method="post">
            <button type="submit" name="verify" value="Selected">Selected</button>
            <button type="submit" name="verify" value="Not Selected">Not Selected</button><br>
            <textarea name="reason"></textarea><br>
            <input type="submit" value="Check">
        </form>
    '''

@app.route('/received')
def results():
    status = request.args.get('status')
    reason = request.args.get('reason', 'No reason given')
    return f"<h3>Status: {status}</h3><p>Reason: {reason}</p>"

if __name__ == "__main__":
    app.run(debug=True)
