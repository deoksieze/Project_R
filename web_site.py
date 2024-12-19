import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# from api_weather import get_weather_features


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

weather1 = {'dates': ['2024-12-19', '2024-12-20', '2024-12-21', '2024-12-22', '2024-12-23'], 
           'min_temp_c': [-17.2, -8.5, 1.1, -5.8, -4.1], 
           'max_temp_c': [-10.0, -5.9, 3.1, 1.9, -1.6], 
           'humidity_day': [73, 81, 94, 85, 86], 
           'wind_speed_day': [24.1, 14.8, 16.7, 14.8, 13.0], 
           'risk_of_rain': [94, 80, 40, 11, 9]}

weather2 = {'dates': ['2024-12-19', '2024-12-20', '2024-12-21', '2024-12-22', '2024-12-23'], 
            'min_temp_c': [-3.4, -4.6, -8.4, -6.7, -9.3], 
            'max_temp_c': [-0.8, 7.3, -2.5, -3.1, -1.5], 
            'humidity_day': [94, 85, 70, 63, 65], 
            'wind_speed_day': [19.6, 25.4, 9.4, 5.5, 5.2], 
            'risk_of_rain': [48, 14, 53, 47, 33]}

weather3 = [{'dates': ['2024-12-19', '2024-12-20', '2024-12-21', '2024-12-22', '2024-12-23'], 'min_temp_c': [4.4, -8.1, -4.7, -2.9, -15.6], 'max_temp_c': [4.7, -6.6, -9.6, 2.8, 5.3], 'humidity_day': [65, 59, 95, 94, 68], 'wind_speed_day': [17.3, 9.4, 20.3, 29.9, 11.6], 'risk_of_rain': [86, 75, 85, 15, 80]},
             {'dates': ['2024-12-19', '2024-12-20', '2024-12-21', '2024-12-22', '2024-12-23'], 'min_temp_c': [-0.7, -13.0, -11.0, -8.6, -10.6], 'max_temp_c': [6.0, -6.9, 4.5, 7.7, 4.7], 'humidity_day': [88, 95, 86, 83, 55], 'wind_speed_day': [10.5, 7.8, 14.8, 23.2, 6.2], 'risk_of_rain': [81, 22, 69, 68, 88]},
             {'dates': ['2024-12-19', '2024-12-20', '2024-12-21', '2024-12-22', '2024-12-23'], 'min_temp_c': [-17.5, -3.0, -10.7, -12.6, 3.2], 'max_temp_c': [-11.3, 4.5, -14.8, 0.0, -1.1], 'humidity_day': [52, 51, 90, 98, 94], 'wind_speed_day': [15.4, 26.8, 17.3, 7.2, 5.6], 'risk_of_rain': [44, 73, 65, 78, 62]}]

weather = None

# Функция для создания пустого графика
def create_empty_figure():
    return {
        'data': [],
        'layout': {
            'title': 'График не доступен',
            'xaxis': {'title': 'Дата'},
            'yaxis': {'title': 'Значение'},
            'showlegend': False
        }
    }


app.layout = dbc.Container([
    html.H1('График погоды для ваших точек'),
    dbc.Row([
        dbc.Col([
            dbc.CardHeader('Введите Широту начальной точки'),
            dbc.CardBody([
                dbc.Input(id='start-latitude', type='number', placeholder='Введите широту начальной точки'),
                html.Div(id='start-lat-feedback', style={'color': 'red'}),
                dbc.Input(id='end-latitude', type='number', placeholder='Введите широту конечной точки'),
                html.Div(id='end-lat-feedback', style={'color': 'red'}),
            ])
        ]),
        dbc.Col([
            dbc.CardHeader('Введите Долготу начальной точки'),
            dbc.CardBody([
                dbc.Input(id='start-longitude', type='number', placeholder='Введите долготу начальной точки'),
                html.Div(id='start-lon-feedback', style={'color': 'red'}),
                dbc.Input(id='end-longitude', type='number', placeholder='Введите долготу конечной точки'),
                html.Div(id='end-lon-feedback', style={'color': 'red'}),
            ])
        ])
    ]),

    dbc.Row([
       html.Button("Считать координаты", id='read-coordinates-button', n_clicks=0) 
    ]),

    dbc.Row([
        html.Div([
            html.Button("Добавить поля для долготы и широты", id='add-button', n_clicks=0),
            html.Button("Удалить последнее поле", id='remove-button', n_clicks=0),
            html.Div(id='input-container'),
            html.Div(id='add_button_feedback', style={'color': 'red'}),
            dcc.Store(id='clicks-store', data={'add': 0, 'remove': 0, 'remove_was': 0, 'add_clics_was': 0})  # Храним значения кликов
        ]) 
    ]),

    dbc.Row([
        dbc.Col([
            dbc.CardHeader('Фильтр по атрибутам'),
            dbc.CardBody([
                dcc.Dropdown(
                    id='weather-atributes',
                    options=[
                        {'label': 'Минимальная температура', 'value': 'min_temp_c'},
                        {'label': 'Максимальная температура', 'value': 'max_temp_c'},
                        {'label': 'Влажность', 'value': 'humidity_day'},
                        {'label': 'Скорость ветра', 'value': 'wind_speed_day'},
                        {'label': 'Риск дождя', 'value': 'risk_of_rain'}
                    ],
                    value='',
                    placeholder='Выберите нужный вид атрибут',
                    multi=True
                )
            ])
        ]),
    ]),

    dbc.Row([
    dbc.Col(dcc.Graph(id='min_temp_graph'), md=6),
    dbc.Col(dcc.Graph(id='max_temp_graph'), md=6)
    ]),
    dbc.Row([
    dbc.Col(dcc.Graph(id='humidity_graph'), md=6),
    dbc.Col(dcc.Graph(id='wind_speed_graph'), md=6)
    ]),
    dbc.Row([
    dbc.Col(dcc.Graph(id='rain_risk_graph'), md=6)
    ]),
    dcc.Store(id='weather-data-store'),


])

# Функция для валидации широты
def validate_latitude(lat_value):
    if lat_value is None:
        return False, False, ""
    elif -90 <= lat_value <= 90:
        return True, False, ""
    else:
        return False, True, "Некорректный ввод! Пожалуйста, введите число от -90 до 90."

# Функция для валидации долготы
def validate_longitude(long_value):
    if long_value is None:
        return False, False, ""
    elif -180 <= long_value <= 180:
        return True, False, ""
    else:
        return False, True, "Некорректный ввод! Пожалуйста, введите число от -180 до 180."
    

# Колбэк для валидации долготы и широты
@app.callback(
    Output('start-latitude', 'valid'),
    Output('start-latitude', 'invalid'),
    Output('start-lat-feedback', 'children'),
    Output('end-latitude', 'valid'),
    Output('end-latitude', 'invalid'),
    Output('end-lat-feedback', 'children'),

    Output('start-longitude', 'valid'),
    Output('start-longitude', 'invalid'),
    Output('start-lon-feedback', 'children'),
    Output('end-longitude', 'valid'),
    Output('end-longitude', 'invalid'),
    Output('end-lon-feedback', 'children'),

    Input('start-latitude', 'value'),
    Input('end-latitude', 'value'),
    Input('start-longitude', 'value'),
    Input('end-longitude', 'value'),
)
def validate_latitudes(start_lat, end_lat, start_lon, end_lon):
    start_lat_valid, start_lat_invalid, start_lat_message = validate_latitude(start_lat)
    end_lat_valid, end_lat_invalid, end_lat_message = validate_latitude(end_lat)

    start_lon_valid, start_lon_invalid, start_lon_message = validate_longitude(start_lon)
    end_lon_valid, end_lon_invalid, end_lon_message = validate_longitude(end_lon)

    return start_lat_valid, start_lat_invalid, start_lat_message, end_lat_valid, end_lat_invalid, end_lat_message, start_lon_valid, start_lon_invalid, start_lon_message, end_lon_valid, end_lon_invalid, end_lon_message

# Колбэк для удаления и добавления кнопкии
@app.callback(
    Output('input-container', 'children'),
    Output('clicks-store', 'data'),
    Output('add_button_feedback', 'children'),
    Input('add-button', 'n_clicks'),
    Input('remove-button', 'n_clicks'),
    State('input-container', 'children'),
    State('clicks-store', 'data')
)
def update_inputs(add_clicks, remove_clicks, current_inputs, clics_data):

    #Инициализируем переменную для хранения обратного сообщения
    feedback  = ''

    # Инициализируем current_inputs как пустой список, если он None
    if current_inputs is None:
        current_inputs = []


    # Логика добавления полей
    if add_clicks > clics_data['add_clics_was'] and len(current_inputs) <= 4:
        clics_data['add_clics_was'] = add_clicks
        
        # Создаем два поля: одно для долготы, другое для широты
        longitude_input = dbc.Input(
            type='number',
            placeholder='Введите долготу',
            id={'type': 'longitude-input', 'index': add_clicks},
            valid=False,
            invalid=False
        )
        
        latitude_input = dbc.Input(
            type='number',
            placeholder='Введите широту',
            id={'type': 'latitude-input', 'index': add_clicks},
            valid=False,
            invalid=False
        )
        
        # Добавляем их в одну строку с двумя колонками
        current_inputs.append(
            dbc.Row([
                dbc.Col(longitude_input, width=6),
                dbc.Col(latitude_input, width=6)
            ])
        )

    elif add_clicks > clics_data['add_clics_was'] and len(current_inputs) > 4:   
        feedback = 'Вы достигли максимального количества дополнительных полей'

    elif len(current_inputs) <= 4:
        feedback = ''

    # Логика удаления поля
    if remove_clicks > clics_data['remove_was'] and current_inputs:
        clics_data['remove_was'] = remove_clicks
        current_inputs.pop()  # Удаляем последнее поле

    return current_inputs, clics_data, feedback  # Возвращаем обновленные данные

#Валидация в добовляемых полях
@app.callback(
    Output({'type': 'longitude-input', 'index': dash.dependencies.ALL}, 'valid'),
    Output({'type': 'longitude-input', 'index': dash.dependencies.ALL}, 'invalid'),
    Output({'type': 'latitude-input', 'index': dash.dependencies.ALL}, 'valid'),
    Output({'type': 'latitude-input', 'index': dash.dependencies.ALL}, 'invalid'),
    Input({'type': 'longitude-input', 'index': dash.dependencies.ALL}, 'value'),
    Input({'type': 'latitude-input', 'index': dash.dependencies.ALL}, 'value')
)
def validate_inputs(longitude_values, latitude_values):
    valid_longitude_states = []
    invalid_longitude_states = []
    valid_latitude_states = []
    invalid_latitude_states = []
    
    for value in longitude_values:
        if value is None:
            valid_longitude_states.append(False)
            invalid_longitude_states.append(False)
        else:
            try:
                num_value = float(value)
                if -180 <= num_value <= 180:
                    valid_longitude_states.append(True)
                    invalid_longitude_states.append(False)
                else:
                    valid_longitude_states.append(False)
                    invalid_longitude_states.append(True)
            except ValueError:
                valid_longitude_states.append(False)
                invalid_longitude_states.append(True)

    for value in latitude_values:
        if value is None:
            valid_latitude_states.append(False)
            invalid_latitude_states.append(False)
        else:
            try:
                num_value = float(value)
                if -90 <= num_value <= 90:
                    valid_latitude_states.append(True)
                    invalid_latitude_states.append(False)
                else:
                    valid_latitude_states.append(False)
                    invalid_latitude_states.append(True)
            except ValueError:
                valid_latitude_states.append(False)
                invalid_latitude_states.append(True)

    return valid_longitude_states, invalid_longitude_states, valid_latitude_states, invalid_latitude_states


@app.callback(
    Output('min_temp_graph', 'figure'),
    Output('max_temp_graph', 'figure'),
    Output('humidity_graph', 'figure'),
    Output('wind_speed_graph', 'figure'),
    Output('rain_risk_graph', 'figure'),
    Input('weather-atributes', 'value'),
    Input('weather-data-store', 'data')  # Получаем данные из Store
)
def draw_graphs(weather_atributes, weather_data):
    if not weather_data:  # Если данных нет, возвращаем пустые графики
        return (create_empty_figure(),) * 5

    # Создаем DataFrame из данных, полученных из Store
    df = pd.DataFrame(weather_data)

    # Инициализируем графики как пустые
    min_temp_fig = go.Figure()
    max_temp_fig = go.Figure()
    humidity_fig = go.Figure()
    wind_speed_fig = go.Figure()
    rain_risk_fig = go.Figure()

    if weather_atributes:

        color_index = 0
        # Проверяем, какие атрибуты выбраны и создаем соответствующие графики
        for index, point in df.groupby('point_index'):
            if 'min_temp_c' in weather_atributes:
                min_temp_fig.add_trace(go.Scatter(
                    x=point['dates'],
                    y=point['min_temp_c'],
                    mode='lines+markers',
                    name=index,
                    line=dict(color=px.colors.qualitative.Plotly[color_index])
                ))


            if 'max_temp_c' in weather_atributes:
                max_temp_fig.add_trace(go.Scatter(
                    x=point['dates'],
                    y=point['max_temp_c'],
                    mode='lines+markers',
                    name=index,
                ))

            if 'humidity_day' in weather_atributes:
                humidity_fig.add_trace(go.Scatter(
                    x=point['dates'],
                    y=point['humidity_day'],
                    mode='lines+markers',
                    name=index,
                ))

            if 'wind_speed_day' in weather_atributes:
                wind_speed_fig.add_trace(go.Scatter(
                    x=point['dates'],
                    y=point['wind_speed_day'],
                    mode='lines+markers',
                    name=index,
                ))

            if 'risk_of_rain' in weather_atributes:
                rain_risk_fig.add_trace(go.Scatter(
                    x=point['dates'],
                    y=point['risk_of_rain'],
                    mode='lines+markers',
                    name=index,
                ))
            color_index += 1

    # Если атрибут не выбран, возвращаем пустой график
    return (min_temp_fig if 'min_temp_c' in weather_atributes else create_empty_figure(),
            max_temp_fig if 'max_temp_c' in weather_atributes else create_empty_figure(),
            humidity_fig if 'humidity_day' in weather_atributes else create_empty_figure(),
            wind_speed_fig if 'wind_speed_day' in weather_atributes else create_empty_figure(),
            rain_risk_fig if 'risk_of_rain' in weather_atributes else create_empty_figure())

# Преобразование списка словарей в один DataFrame
def combine_weather_data(weathers):
    combined_data = []
    
    for index, weather in enumerate(weathers):
        # Добавляем индекс точки к каждому словарю
        if index == 0:
            weather['point_index'] = f'Первая точка'
            combined_data.append(pd.DataFrame(weather))

        elif index == len(weathers)-1:
            weather['point_index'] = f'Последняя точка'
            combined_data.append(pd.DataFrame(weather))
        
        else:
            weather['point_index'] = f'Точка {index}'
            combined_data.append(pd.DataFrame(weather))
    
    # Объединяем все DataFrame в один
    combined_df = pd.concat(combined_data, ignore_index=True)
    
    return combined_df


@app.callback(
    Output('weather-data-store', 'data'),
    Input('read-coordinates-button', 'n_clicks'),
    Input('start-latitude', 'value'),
    Input('end-latitude', 'value'),
    Input('start-longitude', 'value'),
    Input('end-longitude', 'value'),
    Input({'type': 'latitude-input', 'index': dash.dependencies.ALL}, 'value'),
    Input({'type': 'longitude-input', 'index': dash.dependencies.ALL}, 'value'),
)
def log_coordinates(n_clicks, start_lat, end_lat, start_lon, end_lon, additional_latitudes, additional_longitudes):
    if n_clicks > 0:  # Проверяем, была ли нажата кнопка
        weathers = []
        # Выводим координаты в консоль
        print(f"Начальная широта: {start_lat}, Конечная широта: {end_lat}, "
              f"Начальная долгота: {start_lon}, Конечная долгота: {end_lon}")

        if start_lon != None and start_lat != None:
            weathers.append(weather1)



        # Считываем дополнительные координаты
        i = 0
        for lat, lon in zip(additional_latitudes, additional_longitudes):
            print(f"Дополнительная широта: {lat}, Дополнительная долгота: {lon}")
            
            if lat != None and lon != None:
                weathers.append(weather3[i])
            i+= 1

        if end_lon != None and end_lat != None:
            weathers.append(weather2)

        df = combine_weather_data(weathers)
        return df.to_dict('records')


    # Возвращаем None, так как не нужно обновлять интерфейс
    return dash.no_update




if __name__ == '__main__':
    app.run_server(debug=True)

