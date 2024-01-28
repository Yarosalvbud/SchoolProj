import asyncio
import time
import random
import os
from sys import platform

import matplotlib.pyplot as plt
import signal
from datetime import datetime
import numpy as np

start_time = time.time()
trains = asyncio.Queue()
trains_ = []
stations = []
people_p = []
people_t = []
time_a = []
average_time = []
count_train = 5


class Train:
    def __init__(self, number):
        self.free_place = 400
        self.time_go = {'Рокоссовская': 6, 'Соборная': 3, 'Кристалл': 2, 'Заречная': 7,
                        'Библиотека имени Пушкина': 0}
        self.time_go_b = {'Библиотека имени Пушкина': 7, 'Заречная': 2, 'Кристалл': 3, 'Соборная': 6, 'Рокоссовская': 0}
        self.st_d = {0: 'Рокоссовская', 1:'Соборная', 2: 'Кристалл', 3:'Заречная', 4:'Библиотека имени Пушкина'}
        self.st_d_b = {0:'Библиотека имени Пушкина', 1:'Заречная', 2:'Кристалл', 3:'Соборная', 4:'Рокоссовская'}
        self.number = number
        self.current = ''
        self.id = 0
        self.sight = 0
        self.state = 0

    async def bring_people(self, st):
        people_on_s = st.people
        self.state = 0
        self.current = st.name
        if self.current == 'Библиотека имени Пушкина':
            self.free_place = 400
            self.sight = 1
            self.id = 0
        else:
            self.free_place += random.randint(0, 400 - self.free_place) if self.id != 0 else 0
            await st.control(self.number, self.free_place)
            self.free_place = 0 if people_on_s > self.free_place else self.free_place - people_on_s
            await asyncio.sleep(0.15)

    async def bring_people_b(self, st):
        people_on_s = st.people_b
        self.state = 0
        self.current = st.name
        if self.current == 'Рокоссовская':
            self.free_place = 400
            self.sight = 0
            self.id = 0
        else:
            self.free_place += random.randint(0, 400 - self.free_place) if self.id != 0 else 0
            await st.control_b(self.number, self.free_place)
            self.free_place = 0 if people_on_s > self.free_place else self.free_place - people_on_s
            await asyncio.sleep(0.15)

    async def train_go(self, st):
        if self.sight == 0:
            await self.bring_people(st)
            self.state = 1
            await asyncio.sleep(self.time_go.get(st.name))
            if st.name != 'Библиотека имени Пушкина':
                self.id += 1
            else:
                self.id = 0
        else:
            await self.bring_people_b(st)
            self.state = 1
            await asyncio.sleep(self.time_go_b.get(st.name))
            if st.name != 'Рокоссовская':
                self.id += 1
            else:
                self.id = 0


class Station:

    def __init__(self, name):
        self.name = name
        self.people = 0
        self.people_b = 0
        self.people_st = 0

    async def control(self, number, free_place):
        self.people = self.people - free_place if self.people > free_place else 0

    async def control_b(self, number, free_place):
        self.people_b = self.people_b - free_place if self.people_b > free_place else 0

    async def passengers(self):
        while True:
            if time.time() - start_time >= 18:
                coin = random.randint(0, 1)
                if coin == 0 and self.name != 'Библиотека имени Пушкина':
                    self.people += 1
                elif coin == 0 and self.name == 'Библиотека имени Пушкина':
                    self.people_b += 1
                elif self.name != 'Рокоссовская' and coin == 1:
                    self.people_b += 1
                elif self.name == 'Рокоссовская' and coin == 1:
                    self.people += 1
                self.people_st = self.people + self.people_b
                await asyncio.sleep(0.016)
            else:
                await asyncio.sleep(18)


async def trains_online():
    num = 0
    for i in range(count_train):
        num += 1
        train = Train(num)
        trains_.append(train)
        await trains.put(train)
        await asyncio.sleep(38 / count_train)


async def main():
    while True:
        train = await trains.get()
        st = stations[train.id] if train.sight == 0 else stations_b[train.id]
        await train.train_go(st)
        await trains.put(train)


Rok = Station('Рокоссовская')
Sob = Station('Соборная')
Cry = Station('Кристалл')
Zar = Station('Заречная')
Lib = Station('Библиотека имени Пушкина')
stations.append(Rok)
stations.append(Sob)
stations.append(Cry)
stations.append(Zar)
stations.append(Lib)
stations_b = stations[::-1]


async def average():
    while True:
        count_p = 0
        people_p.append((Rok.people_st + Sob.people_st + Cry.people_st + Zar.people_st + Lib.people_st) // 5)
        time_a.append(int(time.time() - start_time))
        for i in trains_:
            count_p += 400 - i.free_place
        people_t.append(count_p // 5)
        people_time = np.random.randint(2, 16, 10)
        if time.time() - start_time >= 18:
            average_time.append(sum(people_time) // len(people_time))
        else:
            average_time.append(0)
        await asyncio.sleep(5)


def show_depends(*args, **kwargs):
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 3))
    axes[0].plot(time_a, people_p, marker='o', color='blue')
    axes[0].set_title('Среднее количество людей на станции')
    axes[1].plot(time_a, people_t, marker='o', color='#0ff')
    axes[1].set_title('Среднее количество людей в поезде')
    axes[2].plot(time_a, average_time, marker='o', color='#00bfff')
    axes[2].set_title('Среднее время поездки')
    plt.tight_layout()
    plt.show()


async def show():
    im = "🚈"
    im_s = "🚉"
    while True:
        curr_info = []
        info = []
        trains_one = ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ']
        trains_two = ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ']
        os.system('cls')
        print(datetime.now())
        print(f"{Rok.name}:   {Rok.people_st}")
        print(f"{Sob.name}:   {Sob.people_st}")
        print(f"{Cry.name}:   {Cry.people_st}")
        print(f"{Zar.name}:   {Zar.people_st}")
        print(f"{Lib.name}:   {Lib.people_st}")

        for j in stations:
            curr_info.append(f"{j.name[0]}:{j.people_st}")
            info.append(j.name)
            if j.name != 'Библиотека имени Пушкина':
                info.append('   ')
                curr_info.append('   ')
        for tr in trains_:
            if tr.sight == 0:
                print(f"{tr.number}:  {tr.st_d.get(tr.id)} -> {tr.st_d.get(tr.id + 1)}") if tr.state != 0 else print(f'{tr.number}: {tr.st_d.get(tr.id)} остановка')
                if tr.state != 0:
                    trains_one[info.index(tr.st_d.get(tr.id)) + 1] = f"{tr.number}:{400 - tr.free_place}"
                else:
                    trains_one[info.index(tr.st_d.get(tr.id))] = f"{tr.number}:{400 - tr.free_place}"
            else:
                print(f"{tr.number}:  {tr.st_d_b.get(tr.id)} --> {tr.st_d_b.get(tr.id + 1)}") if tr.state != 0 else print(f'{tr.number}: {tr.st_d_b.get(tr.id)} остановка')
                if tr.state != 0:
                    trains_two[info.index(tr.st_d_b.get(tr.id)) - 1] = f"{tr.number}:{400 - tr.free_place}"
                else:
                    trains_two[info.index(tr.st_d_b.get(tr.id))] = f"{tr.number}:{400 - tr.free_place}"
        print(*curr_info)
        print(*trains_one)
        print(*trains_two)
        await asyncio.sleep(3)

signal.signal(signal.SIGINT, show_depends)
loop = asyncio.get_event_loop()
loop.create_task(Rok.passengers())
loop.create_task(Sob.passengers())
loop.create_task(Cry.passengers())
loop.create_task(Zar.passengers())
loop.create_task(Lib.passengers())
loop.create_task(trains_online())
loop.create_task(average())
loop.create_task(show())
for i in range(count_train):
    loop.create_task(main())
loop.run_forever()
