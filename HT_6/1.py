"""
1. Програма-світлофор.
   Створити програму-емулятор світлофора для авто і пішоходів.
   Після запуска програми на екран виводиться в лівій половині - колір автомобільного, а в правій - пішохідного світлофора.
   Кожну секунду виводиться поточні кольори. Через декілька ітерацій - відбувається зміна кольорів - логіка така сама як і в звичайних світлофорах.
   Приблизний результат роботи наступний:
      Red        Green
      Red        Green
      Red        Green
      Red        Green
      Yellow     Green
      Yellow     Green
      Green      Red
      Green      Red
      Green      Red
      Green      Red
      Yellow     Red
      Yellow     Red
      Red        Green
      .......
"""

import time



def traffic_lights_generator():
    index = 0

    car_traffic_lights_colors = ['Red'] * 4 + ['Yellow'] * 2 + ['Green'] * 4 + ['Yellow'] * 2 
    pedestrian_traffic_lights_colors = ['Green'] * 6 + ['Red'] * 6  

    while True:
        if index == len(car_traffic_lights_colors):
            index = 0

        yield car_traffic_lights_colors[index], pedestrian_traffic_lights_colors[index]

        index +=1 


def main():
    lights_generator = traffic_lights_generator()

    while True:
        car_traffic_lights_color, pedestrian_traffic_lights_color = next(lights_generator)

        print(car_traffic_lights_color, pedestrian_traffic_lights_color, sep='\t')

        time.sleep(1)


if __name__ ==  '__main__':
    main()
