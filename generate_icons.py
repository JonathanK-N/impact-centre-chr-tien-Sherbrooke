from PIL import Image, ImageDraw, ImageFont
import os

# Créer le dossier icons s'il n'existe pas
icons_dir = 'app/static/icons'
os.makedirs(icons_dir, exist_ok=True)

# Tailles d'icônes requises pour PWA
sizes = [72, 96, 128, 144, 152, 192, 384, 512]

# Couleurs ICC
bg_color = '#667eea'
text_color = '#ffffff'

for size in sizes:
    # Créer une nouvelle image
    img = Image.new('RGB', (size, size), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Calculer la taille de police proportionnelle
    font_size = int(size * 0.3)
    
    try:
        # Essayer d'utiliser une police système
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Utiliser la police par défaut si arial n'est pas disponible
        font = ImageFont.load_default()
    
    # Texte à afficher
    text = "ICC"
    
    # Calculer la position pour centrer le texte
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # Dessiner le texte
    draw.text((x, y), text, fill=text_color, font=font)
    
    # Sauvegarder l'icône
    filename = f'icon-{size}x{size}.png'
    filepath = os.path.join(icons_dir, filename)
    img.save(filepath, 'PNG')
    print(f'Icône créée: {filename}')

print('Toutes les icônes PWA ont été générées!')