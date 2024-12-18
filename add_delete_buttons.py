import dash
from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Button("Добавить поля для долготы и широты", id='add-button', n_clicks=0),
    html.Button("Удалить последнее поле", id='remove-button', n_clicks=0),
    html.Div(id='input-container'),
    dcc.Store(id='clicks-store', data={'add': 0, 'remove': 0, 'remove_was': 0, 'add_clics_was': 0})  # Храним значения кликов
])

@app.callback(
    Output('input-container', 'children'),
    Output('clicks-store', 'data'),
    Input('add-button', 'n_clicks'),
    Input('remove-button', 'n_clicks'),
    State('input-container', 'children'),
    State('clicks-store', 'data')
)
def update_inputs(add_clicks, remove_clicks, current_inputs, clics_data):
    # Инициализируем current_inputs как пустой список, если он None
    if current_inputs is None:
        current_inputs = []

    # Логика добавления полей
    if add_clicks > clics_data['add_clics_was']:
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

    # Логика удаления поля
    if remove_clicks > clics_data['remove_was'] and current_inputs:
        clics_data['remove_was'] = remove_clicks
        current_inputs.pop()  # Удаляем последнее поле

    return current_inputs, clics_data  # Возвращаем обновленные данные

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

if __name__ == '__main__':
    app.run_server(debug=True)

