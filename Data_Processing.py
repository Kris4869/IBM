import os
import serial
import pynmea2
# 后两个为采集GPS数据所需要的库

block_count = 0  # 为每个扫描的block编号


def flight_control():
    # 1.飞行控制 运行在无人机/热气球上
    # 此处调用无人机/热气球飞控的API实现操控
    global block_count
    block_count += 1  # 每执行一次飞行动作，更新block编号


def data_collect(interface, root):
    # 2.数据采集 调用树莓派WiFi和GPS模块 存储数据到树莓派
    # 运行在无人机/热气球上
    save_path = os.path.join(root, str(block_count))
    os.system("iwlist {} scanning > {}".format(interface, save_path))  # 存储当前位置扫描到的AP列表
    ser = serial.Serial("/dev/ttyAMA0", 9600)  # 读取GPS信息并写入AP列表末尾，便于调用
    line = ser.readline()
    if line.startswith('$GNRMC'):
        rmc = pynmea2.parse(line)
        lat = float(rmc.lat) / 100
        lon = float(rmc.lon) / 100
        f = open(save_path, "a")
        f.write("{} {}".format(lat, lon))
        f.close()
    # 为每一个block生成独自的数据文件


def data_process(root):
    # 3.每个无人机的数据处理
    # 运行于服务器端
    ap_lst = []
    lst = os.listdir(root)
    for i in range(len(lst)):
        path = os.path.join(root, lst[i])
        f = open(path, "r")
        for j in f.readlines():
            if "Signal level" in j:
                line_lst = j.strip(" dBm \n").split("=-")
                ap_lst.append(int(line_lst[-1]))
        relative_energy = (len(str)*100 - sum(ap_lst))/len(ap_lst)
        # 计算每个监测点的相对信号强度
        lat, lon = f.readlines()[-2].split(" ")
        data = [relative_energy, lat, lon]
        return data


def data_merge(root):
    # 4.对每个block进行数据汇总
    # 运行于服务器端
    block_count = 100  # 指定Block的总数 假定100
    # 接下来对每个Block的不同无人机数据进行汇总
    for i in range(block_count):
        current_block = i + 1
        lst = []
        lst.append(["drone data"])
        path = os.path.join(root, "blockdata", str(current_block))
        file = open(path, "w")
        file.close()