import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Определение макета приложения
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
    ])
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


if __name__ == '__main__':
    app.run_server(debug=True)

