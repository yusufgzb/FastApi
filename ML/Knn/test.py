import json
import requests

url = "http://localhost:8080/predict/"

headers = {'Content-Type': 'application/json', 'accept': 'application/json'}

data = {"Pregnancies": 890, "Glucose": 70, "BloodPressure": 80, "SkinThickness": 8890, "Insulin": 70, "BMI": 70, "DiabetesPedigreeFunction": 70, "Age": 80}


def main():
    thread1 = threading.Thread(target=threadProc1)
    thread2 = threading.Thread(target=threadProc2)
    thread3 = threading.Thread(target=threadProc3)
    thread4 = threading.Thread(target=threadProc4)
    thread5 = threading.Thread(target=threadProc5)
    thread6 = threading.Thread(target=threadProc6)
    thread7 = threading.Thread(target=threadProc7)
    thread8 = threading.Thread(target=threadProc8)
    thread9 = threading.Thread(target=threadProc9)
    thread10 = threading.Thread(target=threadProc10)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()
    thread8.start()
    thread9.start()
    thread10.start()




def threadProc1():
    for i in range(100):
        response = requests.post(url, headers=headers, json=data)
        print("1---",response.json())

def threadProc2():
    for i in range(100):
        response = requests.post(url, headers=headers, json=data)
        print("2---",response.json())

def threadProc3():
    for i in range(100):
        response = requests.post(url, headers=headers, json=data)
        print("3---",response.json())

def threadProc4():
    for i in range(100):
        response = requests.post(url, headers=headers, json=data)
        print("4---",response.json())

def threadProc5():
    for i in range(100):
        response = requests.post(url, headers=headers, json=data)
        print("5---",response.json())


def threadProc6():
    for i in range(100):
        response = requests.post(url, headers=headers, json=data)
        print("6---",response.json())

def threadProc7():
    for i in range(100):
        response = requests.post(url, headers=headers, json=data)
        print("7---",response.json())

def threadProc8():
    for i in range(100):
        response = requests.post(url, headers=headers, json=data)
        print("8---",response.json())

def threadProc9():
    for i in range(100):
        response = requests.post(url, headers=headers, json=data)
        print("9---",response.json())

def threadProc10():
    for i in range(100):
        response = requests.post(url, headers=headers, json=data)
        print("10---",response.json())


main()
