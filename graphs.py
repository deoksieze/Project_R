import plotly.express as px 
weather = {'dates': ['2024-12-18T07:00:00+03:00', '2024-12-19T07:00:00+03:00', '2024-12-20T07:00:00+03:00', '2024-12-21T07:00:00+03:00', '2024-12-22T07:00:00+03:00'], 
           'min_temp_c': [-17.2, -8.5, 1.1, -5.8, -4.1], 
           'max_temp_c': [-10.0, -5.9, 3.1, 1.9, -1.6], 
           'humidity_day': [73, 81, 94, 85, 86], 
           'wind_speed_day': [24.1, 14.8, 16.7, 14.8, 13.0], 
           'risk_of_rain': [94, 80, 40, 11, 9]}

fig = px.line(weather, x='dates', y='max_temp_c', title='Максимальная температура по датам', labels={'x': 'Дата', 'y': 'Температура'})
fig.add_scatter(x=weather['dates'], y=weather['min_temp_c'], mode='lines', name='Средняя температура', line=dict(color='blue', dash='dash'))


# Показываем график
fig.show()

