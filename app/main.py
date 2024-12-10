import random
from flask import Flask, send_file, request, render_template
from mandala_maker import *
from io import BytesIO
import math

app = Flask(__name__)



@app.route('/')
def home():
    default_configs = [
        # Outermost ring
        {"size": 0.15, "stretch": 1.4, "min_dist": 0.40, "enabled": True},
        # Outer ring
        {"size": 0.13, "stretch": 1.4, "min_dist": 0.35, "enabled": True},
        # Upper middle ring
        {"size": 0.12, "stretch": 1.3, "min_dist": 0.25, "enabled": True},
        # Lower middle ring
        {"size": 0.10, "stretch": 1.2, "min_dist": 0.15, "enabled": True},
        # Inner ring
        {"size": 0.08, "stretch": 1.1, "min_dist": 0.05, "enabled": True}
    ]
    return render_template('index.html', default_configs=default_configs)

@app.route('/mandala')
def get_mandala():
    scale_factor = 2
    segments = int(request.args.get('segments', 36))
    fill_petals = request.args.get('fill_petals') == 'on'
    size = 1600
    
    petal_configs = []
    defaults = [
        {"size": 0.15, "stretch": 1.4, "min_dist": 0.40},
        {"size": 0.13, "stretch": 1.4, "min_dist": 0.35},
        {"size": 0.12, "stretch": 1.3, "min_dist": 0.25},
        {"size": 0.10, "stretch": 1.2, "min_dist": 0.15},
        {"size": 0.08, "stretch": 1.1, "min_dist": 0.05}
    ]
    
    for i in range(1, 6):  # Changed to 6 for 5 rings
        # Check if ring is enabled
        if request.args.get(f'enabled_{i}', 'off') == 'on':
            size_factor = float(request.args.get(f'size_{i}', defaults[i-1]["size"]))
            stretch = float(request.args.get(f'stretch_{i}', defaults[i-1]["stretch"]))
            min_dist = float(request.args.get(f'min_dist_{i}', defaults[i-1]["min_dist"]))
            
            petal_configs.append({
                "size": size * scale_factor * size_factor,
                "stretch": stretch,
                "min_dist": size * scale_factor * min_dist
            })

    print("Petal configurations:", petal_configs)
    
    mandala = generate_mandala(size=size,
                             segments=segments, 
                             petal_configs=petal_configs,
                             fill_petals=fill_petals)
    
    img_io = BytesIO()
    mandala.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True) 
