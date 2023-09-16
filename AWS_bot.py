import telebot
import subprocess
from telebot import types
import boto3                          #<---- Імпорт потрібних бібліотек
with open('start.sh', 'r') as file:
    user_data_script = file.read()
    print(user_data_script)           #<---- Відкриваємо файл з bash командами та записуємо у змінну
TOKEN = "6659756402:AAGwYhea35qBozf0nED94U3UVko0BARAyy4"
bot = telebot.TeleBot(TOKEN)          #<---- Токен телеграм бота
aws_access_key_id = 'AKIAQGL7X2SFKYYZNUHV'
aws_secret_access_key = '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' 
region='eu-north-1'                   #<---- Креди і регіон AWS
ec2 = boto3.client('ec2',aws_access_key_id = 'AKIAQGL7X2SFKYYZNUHV',aws_secret_access_key = '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',region_name=region) #<---- оголошуємо клієнт з вище вказаними кредами
@bot.message_handler(commands=["start"])    #<---- клас якій реагує на start і виводить список дій
def start_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)  #<---- змінна для кнопок
    item0 = types.KeyboardButton("Створити EC2 Instance")
    item1 = types.KeyboardButton("Створити Контейнер")
    item2 = types.KeyboardButton("Запустити Контейнер")
    item3 = types.KeyboardButton("Зупинити Контейнер")
    item4 = types.KeyboardButton("Запустити(після зупинки) Контейнер") #<----змінні з кнопками
    item5 = types.KeyboardButton("Видалити Контейнер")
    item6 = types.KeyboardButton("Подивитись стан Контейнера") 
    markup.add(item0,item1, item2, item3,item4,item5,item6) #<---- добавляємо в змінну
    bot.send_message(
        message.chat.id, "Вибери операцію :", reply_markup=markup
    )
@bot.message_handler(func=lambda message: message.text == "Створити EC2 Instance")
def create_ec2(message):                        #<---- функція яка створює EC2 Instance в AWS
    global user_data_script   #<---- глобальна змінна з bash скриптом
    security_group_id = 'sg-0b1bcc8cf9d484e37' #<----змінна з ID security group

    associate_public_ip_address = True  #<---- дозвіл на додавання білих IP
    network_interface = {
    'DeviceIndex': 0,
    'SubnetId': 'subnet-00f6f4779609e38be',   #<----змінна з мережевими налаштуванням
    'Groups': ['sg-0b1bcc8cf9d484e37'],
    'AssociatePublicIpAddress': associate_public_ip_address,
}
    print ("Creating EC2 instance")
    resource_ec2 = boto3.client("ec2") #<---- викликаємо EC2 клієнт
    resource_ec2.run_instances(         
            ImageId="ami-0989fb15ce71ba39e", #<----ID Операційки (ubuntu22.04 LTS)
            MinCount=1,
            MaxCount=1,                              #<---- Налаштування EC2 instance
            InstanceType="t3.micro",         #<----Тип Instance 
            KeyName="kaka",             #<---- Ключи для SSH входу
            NetworkInterfaces=[network_interface],  #<---- Налаштування мережі
            UserData=user_data_script) #<---- змінна з bash скриптом
    print(resource_ec2.describe_instances()["Reservations"][0]["Instances"][0]["InstanceId"]) #<---- Виводить в консоль ID Instance
    bot.send_message(
        message.chat.id, f"EC2 Instance успішно створений!Зайди в t.me/AWStelebot_bot щоб конфігурувати Docker в AWS")
@bot.message_handler(func=lambda message: message.text == "Створити Контейнер")
def create_cont(message):          #<---- функція яка створює Docker Контейнер
    commands = "touch Dockerfile"
    kaka = subprocess.run(commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    commands1 = "echo FROM httpd:latest >> Dockerfile && echo EXPOSE 80 >> Dockerfile && docker build -t telebot_python:v1 ."
    kaka1 = subprocess.run(commands1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    response_message = (f"Стан Контейнера:\nКоманда видала:\n + {kaka1.stdout} +\nПомилка:\n + {kaka1.stderr} +\nВихідний код:  + {str(kaka1.returncode)}")
    bot.send_message(message.chat.id,response_message)
@bot.message_handler(func=lambda message: message.text == "Запустити Контейнер")
def run_cont(message):       #<---- функція яка запускає контейнер
    commands1 = "docker run -d -p 80:80 --name my-apache telebot_python:v1"
    kaka1 = subprocess.run(commands1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    response_message = (f"Стан Контейнера:\nКоманда видала:\n + {kaka1.stdout} +\nПомилка:\n + {kaka1.stderr} +\nВихідний код:  + {str(kaka1.returncode)}")
    bot.send_message(message.chat.id,response_message)
@bot.message_handler(func=lambda message: message.text == "Зупинити Контейнер")
def stop_cont(message):         #<---- зупиняє контейнер
    commands1 = "docker stop my-apache"
    kaka1 = subprocess.run(commands1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    response_message = (f"Стан Контейнера:\nКоманда видала:\n + {kaka1.stdout} +\nПомилка:\n + {kaka1.stderr} +\nВихідний код:  + {str(kaka1.returncode)}")
    bot.send_message(message.chat.id,response_message)
@bot.message_handler(func=lambda message: message.text == "Запустити(після зупинки) Контейнер")
def again_cont(message):     #<---- запускає після зупинки
    commands1 = "docker start my-apache"
    kaka1 = subprocess.run(commands1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    response_message = (f"Стан Контейнера:\nКоманда видала:\n + {kaka1.stdout} +\nПомилка:\n + {kaka1.stderr} +\nВихідний код:  + {str(kaka1.returncode)}")
    bot.send_message(message.chat.id,response_message)
@bot.message_handler(func=lambda message: message.text == "Видалити Контейнер")
def del_cont(message):       #<---- видаляє контейнер
    commands1 = "docker rm -f my-apache"
    kaka1 = subprocess.run(commands1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    response_message = (f"Стан Контейнера:\nКоманда видала:\n + {kaka1.stdout} +\nПомилка:\n + {kaka1.stderr} +\nВихідний код:  + {str(kaka1.returncode)}")
    bot.send_message(message.chat.id,response_message)
@bot.message_handler(func=lambda message: message.text == "Подивитись стан Контейнера")
def check_cont(message):     #<---- виводить стан контейнера
    commands1 = "docker ps"
    kaka1 = subprocess.run(commands1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    response_message = (f"Стан Контейнера:\nКоманда видала:\n + {kaka1.stdout} +\nПомилка:\n + {kaka1.stderr} +\nВихідний код:  + {str(kaka1.returncode)}")
    bot.send_message(message.chat.id,response_message)


bot.infinity_polling()
