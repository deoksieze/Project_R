import dash
from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container([
    html.H1('Главный заголовко страницы'),
    html.Div([
    html.Button("Добавить поле", id='add-button', n_clicks=0),
    html.Button("Удалить последнее поле", id='remove-button', n_clicks=0),
    html.Div(id='input-container'),
    dcc.Store(id='clicks-store', data={'add': 0, 'remove': 0, 'remove_was': 0, 'add_clics_was': 0})  # Храним значения кликов
    ])    
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

    # Логика добавления поля
    if add_clicks > clics_data['add_clics_was']:
        clics_data['add_clics_was'] = add_clicks
        new_input = dbc.Input(
            type='number',
            placeholder='Введите долготу промежуточной точки',
            id={'type': 'dynamic-input', 'index': add_clicks},
            valid=False,
            invalid=False
        )
        current_inputs.append(new_input)

    # Логика удаления поля
    if remove_clicks > clics_data['remove_was'] and current_inputs:
        clics_data['remove_was'] = remove_clicks
        current_inputs.pop()  # Удаляем последнее поле

    return current_inputs, clics_data  # Возвращаем обновленные данные

@app.callback(
    Output({'type': 'dynamic-input', 'index': dash.dependencies.ALL}, 'valid'),
    Output({'type': 'dynamic-input', 'index': dash.dependencies.ALL}, 'invalid'),
    Input({'type': 'dynamic-input', 'index': dash.dependencies.ALL}, 'value')
)
def validate_inputs(values):
    valid_states = []
    invalid_states = []
    
    for value in values:
        if value is None:
            valid_states.append(False)
            invalid_states.append(False)
        else:
            try:
                num_value = float(value)
                if -180 <= num_value <= 180:
                    valid_states.append(True)
                    invalid_states.append(False)
                else:
                    valid_states.append(False)
                    invalid_states.append(True)
            except ValueError:
                valid_states.append(False)
                invalid_states.append(True)

    return valid_states, invalid_states

if __name__ == '__main__':
    app.run_server(debug=True)
