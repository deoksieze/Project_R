# import plotly.express as px 
# import pandas as pd
# weather = {'dates': ['2024-12-19', '2024-12-20', '2024-12-21', '2024-12-22', '2024-12-23'], 
#            'min_temp_c': [-17.2, -8.5, 1.1, -5.8, -4.1], 
#            'max_temp_c': [-10.0, -5.9, 3.1, 1.9, -1.6], 
#            'humidity_day': [73, 81, 94, 85, 86], 
#            'wind_speed_day': [24.1, 14.8, 16.7, 14.8, 13.0], 
#            'risk_of_rain': [94, 80, 40, 11, 9]}


# df = pd.DataFrame(weather)
# df_long = df.melt(id_vars='dates', value_vars=['min_temp_c', 'max_temp_c'], var_name='var', value_name='temperature')

# color = ['blue', 'red']

# # Создаем график
# fig = px.line(df_long, x='dates', y='temperature', title='Температура по датам', 
#               labels={'dates': 'Дата', 'temperature': 'Температура (C°)'}, 
#               color='var', color_discrete_sequence=color, markers=True)

# # Показываем график
# fig.show()

import random
import pandas as pd

# Задаем фиксированные даты
dates = ['2024-12-19', '2024-12-20', '2024-12-21', '2024-12-22', '2024-12-23']

# Функция для генерации случайных данных
def generate_weather_data():
    return {
        'dates': dates,
        'min_temp_c': [round(random.uniform(-20, 5), 1) for _ in dates],
        'max_temp_c': [round(random.uniform(-15, 10), 1) for _ in dates],
        'humidity_day': [random.randint(50, 100) for _ in dates],
        'wind_speed_day': [round(random.uniform(0, 30), 1) for _ in dates],
        'risk_of_rain': [random.randint(0, 100) for _ in dates]
    }

# Генерируем 5 датасетов
weather_datasets = [generate_weather_data() for _ in range(5)]

# Пример вывода
for i, weather in enumerate(weather_datasets):
    print(f"Dataset {i + 1}:")
    print(weather)
    print()
