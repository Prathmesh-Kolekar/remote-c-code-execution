from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_code():
    code = request.form.get('code')

    # Compile and run the received C code
    try:
        result = subprocess.run(['gcc', '-xc', '-', '-o', 'temp.out'], input=code, text=True, capture_output=True)
        if result.returncode == 0:
            execution_result = subprocess.run(['./temp.out'], capture_output=True, text=True)
            output = execution_result.stdout
            return jsonify({'status': 'success', 'output': output})
        else:
            return jsonify({'status': 'error', 'message': result.stderr})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'message': 'Compilation or execution failed'})

if __name__ == '__main__':
    app.run(debug=True)
