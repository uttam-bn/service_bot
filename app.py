from flask import Flask, request, jsonify, render_template, redirect, url_for
import random
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from model import verify_image, class_indices
from database import init_db, store_complaint, check_infotaiment_serial, get_complaint_by_id

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def generate_complaint_id():
    return f"{random.randint(1000, 9999)}"

init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/file_complaint', methods=['POST'])
def file_complaint():
    try:
        if 'file' not in request.files:
            return jsonify({'fulfillmentText': 'No file part in the request'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'fulfillmentText': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Verify image and get the company and accuracy
            company, accuracy = verify_image(filepath, class_indices)

            if company == "Leaf":
                response_text = "Kindly upload a proper infotainment image. Leaf images are not allowed."
                return jsonify({'fulfillmentText': response_text, 'is_leaf': True})

            dealer_name = request.form['dealer_name']
            vehicle_name = request.form['vehicle_name']
            odometer_reading = request.form['odometer_reading']
            sale_date = request.form['sale_date']
            dealer_address = request.form['dealer_address']
            city = request.form['city']
            company = request.form['company']
            infotainment_serial_no = request.form['infotainment_serial_no']
            image_url = filepath

            # Validate odometer reading
            if int(odometer_reading) > 40000:
                return jsonify({'fulfillmentText': 'Sorry, your warranty has expired. Currently, we are not able to register your complaint.'}), 400

            # Validate sale date
            sale_date_obj = datetime.strptime(sale_date, '%Y-%m-%d')
            if sale_date_obj < datetime.now() - timedelta(days=730):  # 2 years = 730 days
                return jsonify({'fulfillmentText': 'Sorry, your warranty has expired. Currently, we are not able to register your complaint.'}), 400

            # Check infotainment serial number
            existing_complaint = check_infotaiment_serial(infotainment_serial_no)
            if existing_complaint:
                return jsonify({'fulfillmentText': f'Your complaint has already been registered with Complaint ID: {existing_complaint}', 'complaint_id': existing_complaint, 'view_complaint_url': url_for('result', complaint_id=existing_complaint)}), 200

            complaint_id = generate_complaint_id()
            store_complaint(complaint_id, dealer_name, company, vehicle_name, odometer_reading, sale_date, dealer_address, city, image_url, infotainment_serial_no)

            response_text = f'Your complaint has been filed. Complaint ID: {complaint_id}, Dealer Name: {dealer_name}, Vehicle Name: {vehicle_name}, Company: {company}, Dealer Address: {dealer_address}'

            return jsonify({
                'fulfillmentText': response_text,
                'complaint_id': complaint_id,
                'dealer_name': dealer_name,
                'vehicle_name': vehicle_name,
                'company': company,
                'dealer_address': dealer_address,
                'city': city,
                'view_complaint_url': url_for('result', complaint_id=complaint_id),
                'is_leaf': False
            })
        else:
            return jsonify({'fulfillmentText': 'File type not allowed'}), 400
    except Exception as e:
        return jsonify({'fulfillmentText': f'An error occurred while filing the complaint: {str(e)}'}), 500

@app.route('/result')
def result():
    complaint_id = request.args.get('complaint_id')
    if complaint_id:
        complaint = get_complaint_by_id(complaint_id)
        if complaint:
            return render_template('result.html', **complaint)
        else:
            return "Complaint not found", 404
    else:
        return "No complaint ID provided", 400

if __name__ == '__main__':
    app.run(debug=True)
