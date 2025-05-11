import requests
import datetime
import smtplib
import time

MY_LAT = 28.419411
MY_LONG = --81.581200

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0
}

now = datetime.datetime.now()
response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
# response = requests.get(url="https://api.sunrise-sunset.org/json?lat=42.887691&lng=-78.879372")

sunrise = response.json()["results"]["sunrise"].split("T")[1].split(":")[0]
sunset = response.json()["results"]["sunset"].split("T")[1].split(":")[0]
comparer = now.time().hour

print(sunrise)
print(sunset)
print(comparer)
is_night = False
iss_is_overhead = False

if comparer < int(sunset):
    print("Daytime")
    is_night = False
else:
    print("Night")
    is_night = True



iss_response = requests.get("http://api.open-notify.org/iss-now.json")
iss_response.raise_for_status()
iss_lat = iss_response.json()["iss_position"]["latitude"]
iss_long = iss_response.json()["iss_position"]["longitude"]

print(type(float(iss_lat)))
print(f"HELP{abs(MY_LAT-float(iss_lat))}")

if abs(MY_LAT-float(iss_lat)) <= 5 and abs(MY_LONG-float(iss_long)) <= 5:
    iss_is_overhead = True
    print(int(iss_lat.split(".")[0]))
    print(round(MY_LAT))
    print("ISS is overhead")

else:
    iss_is_overhead = False
    print(int(iss_lat.split(".")[0]))
    print(round(MY_LAT))
    print("ISS NOT overhead")



print(f"My Latitude = {MY_LAT}\n"
      f"My Longitude = {MY_LONG}\n"
      f"ISS Latitude = {iss_lat}\n"
      f"ISS Longitude = {iss_long}")


email = "your email here"
password = "your smtp email here"

while True:
    time.sleep(60)
    print("check")
    if is_night and iss_is_overhead:
        print("ISS Is Overhead")
        with smtplib.SMTP("smtp.your email provider.com") as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(from_addr=email,
                                to_addrs=email,
                                msg=f"Subject:ISS is overhead\n\n The ISS is nearby. \nLatitude : {iss_lat}\n "
                                    f"Longitude : {iss_long}")
