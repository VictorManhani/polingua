from src.helpers.imports import *

Builder.load_string("""
<FlexLayout>:
    bg_color: app.style_color["quarter_body_color"]

<FlexButton>:
    font_size: app.font_size
    bg_color: app.style_color["second_body_color"]
    bg_color_normal: app.style_color["second_body_color"]
    bg_color_press: app.style_color["fifth_body_color"]
    color: app.style_color["first_font_color"]
    border_color: app.style_color["first_body_color"]
    text_size: root.size
    halign: "center"
    valign: "middle"

<IconButton>:
    font_size: app.font_size
    bg_color: app.style_color["second_body_color"]
    bg_color_normal: app.style_color["second_body_color"]
    bg_color_press: app.style_color["fifth_body_color"]
    icon_color: app.style_color["first_body_color"]
    border_color: app.style_color["first_body_color"]
    text_size: root.size
    halign: "center"
    valign: "middle"

<FlexLabel>:
    color: app.style_color["first_font_color"]
    bg_color: app.style_color["terciary_body_color"]

<FlexText>:
    bg_normal_color: app.style_color["second_body_color"]
    bg_active_color: app.style_color["second_body_color"]
    
    border_normal_color: app.style_color["ripple_color"]
    border_active_color: app.style_color["first_body_color"]

    cursor_color: app.style_color["first_body_color"]
""")