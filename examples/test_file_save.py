# Standard imports:
from os import path
import logging
from threading import Thread
from csv import writer as csv_write
from csv import reader as csv_reader
from time import sleep, perf_counter as precision_timestamp

import numpy as np

csv_file = r'C:\Pypogs\pypogs-master\pypogs\ex_commands.csv'

x_zero =-500
y_zero =-600

wait_time = 3 #sec
x_start = -1200
x_itera = 10
y_start = -2000
y_itera = 10
x_step = 400
y_step = 400

y_list = [-400,400,-800,800,-1200,1200,-1600,1600]

x_end = x_start +x_step * x_itera
y_end = y_start +y_step * y_itera

if path.exists(csv_file):
    parsed_list = []

    for i in y_list:
        for y in np.arange(y_start,y_end,y_step):
            x_offset = x_zero + y
            y_offset = y_zero + i
            parsed_list = (1,
                           "auto_offset",
                           "FALSE",
                           "offsetX",
                           x_offset,
                           "offsetY",
                           y_offset)

            with open(csv_file, 'w+') as file:
                writer = csv_write(file)
                writer.writerow(parsed_list)
                print("X_off", x_offset, "Y_off", y_offset)

            sleep(wait_time)


            # if parsed_list[0]==1:
            #     y = list(parsed_list)
            #     y[0] = 0
            #     parsed_list = tuple(y)