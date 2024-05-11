from flask import request, render_template, jsonify

def handle_survey_submission(request, db):
    survey_data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "age": request.form['age'],
        "marital_status": request.form['marital_status'],
        "other_marital_status": request.form.get('other_marital_status', ''),
        "therapy": request.form['therapy'],
        "medication": request.form['medication'],
        "medication_details": request.form.getlist('medication_name[]')
    }

    existing_survey = db.survey.find_one({"email": survey_data['email']})
    if existing_survey:
        db.survey.update_one({"email": survey_data['email']}, {"$set": survey_data})
    else:
        db.survey.insert_one(survey_data)
    return render_template('thanku.html')

def check_existing_survey(request, db):
    email = request.form.get('email')
    survey = db.survey.find_one({"email": email})
    if survey:
        return jsonify({"exists": True, "message": "Survey data already exists. Do you want to overwrite it?"})
    return jsonify({"exists": False})
