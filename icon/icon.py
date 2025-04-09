import base64

# Function to load and encode SVG as Base64
def encode_svg(svg_path):
    with open(svg_path, "rb") as f:
        return f"data:image/svg+xml;base64,{base64.b64encode(f.read()).decode()}"

# Encode SVG file from 'assets' folder
icon_path = "icon/twitter.svg"
icon_base64 = encode_svg(icon_path)