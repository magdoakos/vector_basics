import dash

from dash import html, dash_callback, Output, Input, State

import dash_bootstrap_components as dbc

 

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

 

app.layout = html.Div([

    html.H2("Draw a Bounding Box on HERE Map"),

    html.Div(

        id='here-map-container',

        style={'width': '100%', 'height': '600px'},

        children=html.Script("""

            const platform = new H.service.Platform({

                'apikey': 'YOUR_API_KEY'

            });

            const defaultLayers = platform.createDefaultLayers();

            const map = new H.Map(

                document.getElementById('here-map-container'),

                defaultLayers.vector.normal.map,

                {

                    zoom: 12,

                    center: { lat: 52.5200, lng: 13.4050 }

                }

            );

 

            const behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));

            const ui = H.ui.UI.createDefault(map, defaultLayers);

 

            let startPoint = null;

            let boundingBox = null;

            let boxObject = null;

 

            map.addEventListener('pointerdown', function (evt) {

                startPoint = evt.currentPointer;

                if (boxObject) {

                    map.removeObject(boxObject);

                    boxObject = null;

                }

            });

 

            map.addEventListener('pointerup', function (evt) {

                if (!startPoint) return;

 

                const endPoint = evt.currentPointer;

                const rect = new H.geo.Rect(

                    Math.min(startPoint.lat, endPoint.lat),

                    Math.max(startPoint.lat, endPoint.lat),

                    Math.min(startPoint.lng, endPoint.lng),

                    Math.max(startPoint.lng, endPoint.lng)

                );

 

                boxObject = new H.map.Rect(rect, {

                    style: {

                        stroke: '#FF0000',

                        strokeWidth: 2,

                        fill: '#0000FF',

                        fillOpacity: 0.2

                    }

                });

 

                map.addObject(boxObject);

                boundingBox = rect;

                startPoint = null;

 

                // Send bounding box to Dash callback

                const coords = {

                    north: rect.getUpperLeft().lat,

                    south: rect.getLowerRight().lat,

                    west: rect.getUpperLeft().lng,

                    east: rect.getLowerRight().lng

                };

                window.parent.postMessage({ type: 'boundingBox', data: coords }, '*');

            });

        """)

    ),

    html.Div(id='bounding-box-output'),

])

 

@app.callback(

    Output('bounding-box-output', 'children'),

    Input('here-map-container', 'n_clicks')

)

def display_bounding_box(n_clicks):

    # This is a placeholder. Real interaction would use window.postMessage

    return "Bounding box coordinates will appear here after drawing."

 

if __name__ == '__main__':

    app.run_server(debug=True)
