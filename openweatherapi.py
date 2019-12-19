import requests,json,time, smtplib, schedule
from email.message import EmailMessage

city_name = 'Tampa'
api_key = 'Your key'
res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name.title()}&units=imperial&APPID={api_key}')


#api returns json file
file = res.json()
def get_data():
    if file['cod'] != '404':   #if 404, no city was found
        x = file['main']

        current_temp = x['temp']
        max_temp = x['temp_max']
        min_temp = x['temp_min']

        y= file['sys']

        sunrise = y['sunrise']
        sunset = y['sunset']

        return current_temp, min_temp, max_temp, sunrise, sunset
    else:
        print('City not found')

a,b,c,d,e = get_data()

def time_converter():

    local_sunrise =  time.ctime(d)
    local_sunrise = time.strptime(local_sunrise)    #making a time object
    local_sunrise = time.strftime('%X', local_sunrise)

    local_sunset =  time.ctime(e)
    local_sunset = time.strptime(local_sunset)    #making a time object
    local_sunset = time.strftime('%X', local_sunset)
    
    if int(d)>= int(time.time()):
        formatted_times = f'Sunrise will be at {local_sunrise}, and sunset will be at {local_sunset}'
        return formatted_times

    elif int(d)<=int(time.time())<int(e):
        formated_times3 = f'Sunrise was at {local_sunrise}, and sunset will be at {local_sunset}'
        return formated_times3
    elif int(e)<=int(time.time()):
        formated_times2 = f'Sunrise was at {local_sunrise}. and sunset was at {local_sunset}'
        return formated_times2

  
f = time_converter()    
    


def send_info():
    email = EmailMessage()
    email['from'] = 'Your name'
    email['to'] = 'Your email'
    email['subject'] = 'Weather report' 
    sunrise_sunset = time_converter()
    email.set_content(f'This is your weather report for {city_name}. The current temperature is {a}, today\'s minmum temperature will be {b}, and the maximum will be {c}. {sunrise_sunset}')

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()  # starts the server
        smtp.starttls()  # this is the encryption
        smtp.login('your email', 'password')
        smtp.send_message(email)

schedule.every().day.at("06:30").do(get_data)
schedule.every().day.at("06:30").do(time_converter)
schedule.every().day.at("06:30").do(send_info)

while True:
    schedule.run_pending()
    time.sleep(1)