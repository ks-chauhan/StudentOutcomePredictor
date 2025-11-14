import streamlit as st
import pandas as pd
import joblib


st.title("Students Outcome Predictor")

# --- Base Inputs ---
Marital_Status_Code = st.selectbox("Marital Status Code", [0,1,2,3,4,5])
Application_Method = st.selectbox("Application Method", [1,2,3,4,5,6,7,8,9,10])
Application_Sequence = st.number_input("Application Sequence", min_value=1, max_value=20)

Attendance_Type = st.selectbox("Attendance Type", ["Full-time", "Part-time"])

Attendance_Type = 1 if Attendance_Type == 'Full-time' else 0


Prior_Qualification_Code = st.selectbox("Prior Qualification Code", [1,2,3,4,5,6,7,8,9])
Prior_Qualification_Score = st.number_input("Prior Qualification Score", min_value=0.0, max_value=200.0)

Nationality_Code = st.selectbox("Nationality Code", [1,2,3,4,5,6,7,8,9])

Mothers_Education = st.selectbox("Mother's Education Level", [1,2,3,4,5,6])
Fathers_Education = st.selectbox("Father's Education Level", [1,2,3,4,5,6])

Mothers_Job = st.selectbox("Mother's Job Category", [1,2,3,4,5])
Fathers_Job = st.selectbox("Father's Job Category", [1,2,3,4,5])

Admission_Score = st.number_input("Admission Score", min_value=0.0, max_value=200.0)

Student_Displacement_Flag = st.checkbox("Student Displacement Flag")
Special_Educational_Needs = st.checkbox("Special Educational Needs")
Outstanding_Debts_Flag = st.checkbox("Outstanding Debts Flag")
Tuition_Fees_UpToDate_Flag = st.checkbox("Tuition Fees Up-To-Date Flag")
Scholarship_Recipient_Flag = st.checkbox("Scholarship Recipient Flag")

Gender_Code = st.selectbox("Gender Code", ["Male", "Female", "Other"])

if Gender_Code == 'Other':
    Gender_Code = 2
elif Gender_Code == 'Female':
    Gender_Code = 1
else:
    Gender_Code = 0

International_Status = st.checkbox("International Student")
Enrollment_Age = st.number_input("Enrollment Age", min_value=15, max_value=70)

# ------------------------
#   SEMESTER 1
# ------------------------
Enrolled_1st = st.checkbox("Enrolled 1st Semester")

if Enrolled_1st:
    Credits_1st = st.number_input("Credits 1st Semester", min_value=0, max_value=60)
    Evaluations_1st = st.number_input("Evaluations 1st Semester", min_value=0, max_value=20)
    Passed_1st = st.number_input("Passed 1st Semester", min_value=0, max_value=20)
    Grade_1st = st.number_input("Grade 1st Semester", min_value=0.0, max_value=20.0)
    No_Eval_1st = st.number_input("No. Evaluations 1st Semester", min_value=0, max_value=20)
else:
    Credits_1st = Evaluations_1st = Passed_1st = Grade_1st = No_Eval_1st = 0

# ------------------------
#   SEMESTER 2
# ------------------------
Enrolled_2nd = st.checkbox("Enrolled 2nd Semester")

if Enrolled_2nd:
    Credits_2nd = st.number_input("Credits 2nd Semester", min_value=0, max_value=60)
    Evaluations_2nd = st.number_input("Evaluations 2nd Semester", min_value=0, max_value=20)
    Passed_2nd = st.number_input("Passed 2nd Semester", min_value=0, max_value=20)
    Grade_2nd = st.number_input("Grade 2nd Semester", min_value=0.0, max_value=20.0)
    No_Eval_2nd = st.number_input("No. Evaluations 2nd Semester", min_value=0, max_value=20)
else:
    Credits_2nd = Evaluations_2nd = Passed_2nd = Grade_2nd = No_Eval_2nd = 0

# --- Economic Indicators ---
Local_Unemployment_Rate = st.number_input("Local Unemployment Rate (%)", min_value=0.0, max_value=100.0)
Inflation_Rate = st.number_input("Inflation Rate (%)", min_value=0.0, max_value=50.0)
Regional_GDP = st.number_input("Regional GDP (in millions)", min_value=0.0, max_value=1_000_000.0)

# Submit
if st.button("Submit"):
    Enrolled_1st_int = int(Enrolled_1st)
    Enrolled_2nd_int = int(Enrolled_2nd)

    Outstanding_Debts_int = int(Outstanding_Debts_Flag)
    Tuition_UpToDate_int = int(Tuition_Fees_UpToDate_Flag)

    # Derived Features
    Overall_Grade = (Grade_1st + Grade_2nd) / 2
    Grade_Improvement = Grade_2nd - Grade_1st
    Sems_Passed = (Passed_1st + Passed_2nd) / 2
    Total_Credits = Enrolled_1st_int + Enrolled_2nd_int

    # Age Group -> MAPPED to numeric
    if Enrollment_Age <= 20:
        Age_Group = 0
    elif Enrollment_Age <= 23:
        Age_Group = 1
    else:
        Age_Group = 2

    # Financial risk flag
    Tuition_Fees_Flag = 1 if (Tuition_UpToDate_int == 0 or Outstanding_Debts_int == 1) else 0

    # Load scaler
    scaler = joblib.load(r"C:/Kshitij Project/StudentOutcomePredictor/Preprocess/scaler.pkl")

    # Ordered data
    data_ordered = {
        "Marital_Status_Code": Marital_Status_Code,
        "Application_Method": Application_Method,
        "Application_Sequence": Application_Sequence,
        "Attendance_Type": Attendance_Type,
        "Prior_Qualification_Code": Prior_Qualification_Code,
        "Prior_Qualification_Score": Prior_Qualification_Score,
        "Nationality_Code": Nationality_Code,
        "Mother's_Education_Level": Mothers_Education,
        "Father's_Education_Level": Fathers_Education,
        "Mother's_Job_Category": Mothers_Job,
        "Father's_Job_Category": Fathers_Job,
        "Admission_Score": Admission_Score,
        "Student_Displacement_Flag": int(Student_Displacement_Flag),
        "Special_Educational_Needs": int(Special_Educational_Needs),
        "Outstanding_Debts_Flag": Outstanding_Debts_int,
        "Tuition_Fees_UpToDate_Flag": Tuition_UpToDate_int,
        "Gender_Code": Gender_Code,
        "Scholarship_Recipient_Flag": int(Scholarship_Recipient_Flag),
        "Enrollment_Age": Enrollment_Age,
        "International_Status": int(International_Status),

        "Credits_1st_Semester": Credits_1st,
        "Enrolled_1st_Semester": Enrolled_1st_int,
        "Evaluations_1st_Semester": Evaluations_1st,
        "Passed_1st_Semester": Passed_1st,
        "Grade_1st_Semester": Grade_1st,
        "No_Evaluations_1st_Semester": No_Eval_1st,

        "Credits_2nd_Semester": Credits_2nd,
        "Enrolled_2nd_Semester": Enrolled_2nd_int,
        "Evaluations_2nd_Semester": Evaluations_2nd,
        "Passed_2nd_Semester": Passed_2nd,
        "Grade_2nd_Semester": Grade_2nd,
        "No_Evaluations_2nd_Semester": No_Eval_2nd,

        "Local_Unemployment_Rate": Local_Unemployment_Rate,
        "Inflation_Rate": Inflation_Rate,
        "Regional_GDP": Regional_GDP,

        # Derived
        "Overall_Grade": Overall_Grade,
        "Grade_Improvement": Grade_Improvement,
        "Sems_Passed": Sems_Passed,
        "Total_Credits": Total_Credits,
        "Age_Group": Age_Group,
        "Tuition_Fees_Flag": Tuition_Fees_Flag
    }

    # Create DataFrame
    input_df = pd.DataFrame([data_ordered])

    # Scale numeric columns
    num_cols = [
        'Passed_2nd_Semester','Grade_2nd_Semester','Passed_1st_Semester',
        'Grade_1st_Semester','Enrollment_Age','Admission_Score',
        'Prior_Qualification_Score','Overall_Grade','Grade_Improvement',
        'Sems_Passed','Total_Credits', 'Application_Method'
    ]

    input_df[num_cols] = scaler.transform(input_df[num_cols])

    # Load model
    model = joblib.load("C:/Kshitij Project/StudentOutcomePredictor/ML_Models/RandomForest.pkl")

    # Predict
    prediction = model.predict(input_df)

    st.subheader("Predicted Outcome:")
    if prediction[0] == 0:
        st.write("Student has high chances of Dropping Out")
    elif prediction[0] == 1:
        st.write("Student is still enrolled")
    else:
        st.write("Student will be able to Graduate")
