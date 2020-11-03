from kivy.lang import Builder

colors = {
    'lemon_green': [122/255, 199/255, 12/255, 1],
    'orange': [255/255, 199/255, 21/255, 1],
    'dark_orange': [255/255, 100/255, 10/255, 1],
    'light_gray': [240/255, 240/255, 240/255, 1],
    'yellow': [1, 0.7803921569, 0.0823529412, 1],
    'dark_gray': [207/255, 207/255, 207/255, 1],
    'dark_red': [211/255, 49/255, 49/255, 1],
    'light_red': [1.0, 0.2118, 0.2157, 1], #[229/255, 56/255, 56/255, 1],
    'dark_blue':  [28/255, 176/255, 246/255, 1],
    'light_blue': [0.1098, 0.6902, 0.9647, 1],#[20/255, 212/255, 244/255, 1],
    'dark_purple': [133/255, 73/255, 186/255, 1],
    'light_purple': [165/255, 96/255, 232/255, 1],
}

with open('kivy_modules\\color\\color.kv', 'r', encoding='utf-8') as f:
    Builder.load_string(f.read())