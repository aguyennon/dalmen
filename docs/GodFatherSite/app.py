from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

PROGRAMS = {
    'Optimizer App': r'G:\Alexis\Soufflage - Optimizer\Dalmen Orders App.exe',
    'Barcode Generator': r'G:\Alexis\Barcode Generator\BarcodeGenerator.exe',
    'Purchase Order': r'G:\Alexis\PurchaseOrder\PurchaseOrder.exe',
    'Diagonal Cut Optimizer': r'G:\Alexis\DiagonalCutOptimizer.exe'
}

@app.route('/')
def index():
    return render_template('index.html')  # Flask looks in templates/ folder


@app.route('/launch', methods=['POST'])  # Changed from /launch_program to /launch
def launch_program():
    try:
        data = request.json
        program_type = data.get('program')

        if program_type not in PROGRAMS:
            return jsonify({'status': 'error', 'message': 'Invalid program type.'}), 400

        program_path = PROGRAMS[program_type]

        if not os.path.exists(program_path):
            return jsonify({'status': 'error', 'message': f'Program not found: {program_path}'}), 404

        subprocess.Popen([program_path], shell=True)

        return jsonify({'message': f'{program_type} launched successfully!'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    
@app.route('/exit', methods=['POST'])
def exit_application():
    try:
        return jsonify({'message': 'Shutting down...'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/programs')
def list_programs():
    """List available programs and their status"""
    program_status = {}
    for name, path in PROGRAMS.items():
        program_status[name] = {
            'path': path,
            'exists': os.path.exists(path)
        }
    return jsonify(program_status)


if __name__ == '__main__':
    print("Starting GodFather Web Launcher...")
    print("Available programs:")
    for name, path in PROGRAMS.items():
        status = "✓" if os.path.exists(path) else "✗"
        print(f"  {status} {name}: {path}")

    print("\nWeb launcher available at: http://localhost:5500")
    print("Open your browser and go to: http://localhost:5500")
    app.run(debug=True, host='0.0.0.0', port=5500)