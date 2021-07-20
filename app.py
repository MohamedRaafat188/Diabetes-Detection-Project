import tkinter
import joblib

def predict_state():
    signs_inputs = [float(age_entry.get())]
    for entry in entries:
        signs_inputs.append(float(entry.get()))
    sybtoms_inputs = [float(age_entry.get())]
    if gender.get() == "Male":
        sybtoms_inputs.append(1)
    else:
        sybtoms_inputs.append(0)
    for cb in sybtoms_checkboxes:
        if sybtoms_checkboxes[cb].get():
            sybtoms_inputs.append(1)
        else:
            sybtoms_inputs.append(0)


    signs_inputs = vital_signs_scaler.transform([signs_inputs])
    sybtoms_inputs = sybtoms_scaler.transform([sybtoms_inputs])
    signs_predict = vital_signs_model.predict(signs_inputs)
    sybtoms_predict = sybtoms_model.predict(sybtoms_inputs)

    if signs_predict == sybtoms_predict == 1:
        label.set("We are sorry to tell you that but you suffer from diabetes disease. Please consult doctor quickly.")
    elif signs_predict == sybtoms_predict == 0:
        label.set("Congratulations. You don't suffer from diabetes disease.")
    elif signs_predict == 1 and sybtoms_predict == 0:
        label.set("Your vital signs indicate that you suffer from diabetes but your sybtoms indicate that you don't suffer from it. So we advise you to consult a doctor.")
    else:
        label.set("Your sybtoms indicate that you suffer from diabetes but your vital signs indicate that you don't suffer from it. So we advise you to consult a doctor.")

    print(signs_predict, sybtoms_predict)


i = 0
j = 0
genders = ['Male', 'Female']
vital_signs = ["Urea", "HbA1c", "Cholesterol", "Triglycerides", "VLDL", "BMI"]
entries = []
sybtoms = ["POLYURIA", "POLYDIPSIA", "SUDDEN WEIGHT LOSS", "WEAKNESS", "POLYPHAGIA", "GENITAL THRUSH", "VISUAL BLURRING", "ITCHING", "IRRITABILITY", "DELAYED HEALING", "PARTIAL PARESIS", "MUSCLE STIFFNESS", "ALOPECIA", "OBESITY"]
sybtoms_checkboxes = dict()
vital_signs_scaler = joblib.load('signs_scaler.h5')
vital_signs_model = joblib.load('signs_model.h5')
sybtoms_scaler = joblib.load('symptoms_scaler.h5')
sybtoms_model = joblib.load('symptoms_model.h5')

main_window = tkinter.Tk()
main_window.title("Diabetes Detector")
main_window.geometry("640x480")
main_window.state("zoomed")
main_window.configure(padx=20, pady=20)

base_info_frame = tkinter.Frame(main_window)
base_info_frame.grid(row=0, column=0, sticky='nsew')

tkinter.Label(base_info_frame, text="Gender", font=('Comic Sans MS', 20)).grid(row=0, column=0, sticky='w')
gender = tkinter.StringVar(main_window)
gender.set("Select gender")
gender_menu = tkinter.OptionMenu(base_info_frame, gender, *genders)
gender_menu.grid(row=0, column=1, sticky='w')
gender_menu.config(font=('Comic Sans MS', 12))

tkinter.Label(base_info_frame, text="Age", font=('Comic Sans MS', 20)).grid(row=1, column=0, sticky='w')
age_entry = tkinter.Entry(base_info_frame, font=('Comic Sans MS', 12))
age_entry.grid(row=1, column=1, sticky='w', ipadx=5, ipady=3)
age_entry.config(width=10)

vital_signs_frame = tkinter.Frame(main_window)
vital_signs_frame.grid(row=1, column=0, pady=30)

for sign in vital_signs:
    tkinter.Label(vital_signs_frame, text=sign, font=('Comic Sans MS', 20)).grid(row=i, column=j, sticky='w')
    sign_entry = tkinter.Entry(vital_signs_frame, font=('Comic Sans MS', 12))
    sign_entry.grid(row=i, column=j+1, sticky='w', ipadx=5, ipady=3)
    sign_entry.config(width=10)
    entries.append(sign_entry)
    j += 2
    if j == 4:
        i += 1
        j = 0
else:
    i = 1
    j = 0

tkinter.Label(base_info_frame, text="Age", font=('Comic Sans MS', 22)).grid(row=1, column=0, sticky='w')
age_entry = tkinter.Entry(base_info_frame, font=('Comic Sans MS', 12))
age_entry.grid(row=1, column=1, sticky='w', ipadx=5, ipady=5)
age_entry.config(width=10)

sybtoms_frame = tkinter.Frame(main_window)
sybtoms_frame.grid(row=2, column=0, sticky='nsew')

tkinter.Label(sybtoms_frame, text='Choose sybtoms you suffering from', font=('Comic Sans MS', 22)).grid(row=0, column=0, columnspan=2)

for sybtom in sybtoms:
    var = tkinter.IntVar()
    cb = tkinter.Checkbutton(sybtoms_frame, text=sybtom, variable=var, onvalue=1, offvalue=0, font=('Comic Sans MS', 14))
    cb.grid(row=i, column=j, sticky='w')
    i += 1
    if i == 8:
        i = 1
        j = 1
    sybtoms_checkboxes[cb] = var

predict_button = tkinter.Button(main_window, text="Predict", font=('Comic Sans MS', 22), command=predict_state)
predict_button.grid(row=3, column=0, sticky='w', pady=30)
predict_button.config(background='blue')

result_frame = tkinter.LabelFrame(main_window, text="Result", font=('Comic Sans MS', 22))
result_frame.grid(row=1, column=1, sticky='nsew', padx=50, ipadx=4, ipady=4)
result_frame.config(width=200, height=200)
label = tkinter.StringVar()
result_label = tkinter.Label(result_frame, textvariable=label, font=('Comic Sans MS', 22), wraplength=500)
result_label.grid(row=0, column=0, sticky='nsew')

main_window.mainloop()
