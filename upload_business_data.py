import sqlite3
import json
from tqdm import tqdm


def sep_opening_time(hours):
    days_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if not hours:
        res = ["Closed" for _ in range(7)]
    else:
        res = []
        for i in days_list:
            if i in hours.keys():
                res.append(hours[i])
            else:
                res.append("Closed")
    return " ".join(res)


# 创建一个访问SQLite数据库的连接，当指定的数据库文件不存在，会自动创建
conn = sqlite3.connect('business.db')
# 创建游标对象cursor，用来调用SQL语句对数据库进行操作
c = conn.cursor()
# 创建数据表,SQLite未实现表的替换功能，若数据库文件不为空，则此句报错
# c.execute('create table business_info (business_id, business_name, address, city, longitude, latitude, stars, is_open, AppointmentOnly, Hours)')
# conn.commit()
error_list = []


with open("D:/GT/CSE 6242/Proj/yelp_dataset/yelp_academic_dataset_business.json", encoding='utf-8') as f:
    for i in tqdm(f.readlines()):
        c = conn.cursor()
        tem_data = json.loads(i)
        # if tem_data["categories"] and "Restaurants" in tem_data["categories"]:
        #     appointmentonly = 0
        #     if tem_data['attributes'] and 'ByAppointmentOnly' in tem_data['attributes'].keys() and tem_data['attributes']['ByAppointmentOnly']:
        #         appointmentonly = 1
        #     sql_sentence = """insert into business_info (business_id, business_name, address, city, longitude, latitude, stars, is_open, AppointmentOnly, Hours) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        #     para = (tem_data['business_id'], tem_data['name'], tem_data['address'], tem_data['city'], tem_data['longitude'], tem_data['latitude'], tem_data['stars'], tem_data['is_open'], appointmentonly, sep_opening_time(tem_data['hours']))
        #     c.execute(sql_sentence, para)
        if tem_data["business_id"] == "9c7MUiE6VI8NesjPdj5FkA":
            print(tem_data["business_id"])

conn.commit()
conn.close()
