from django import template
import re

register = template.Library()

@register.filter
def youtube_embed(url):
    """
    Convierte una URL de YouTube en un enlace de inserción (embed).
    - Convierte "https://www.youtube.com/watch?v=ABC123&t=1s" → "https://www.youtube.com/embed/ABC123"
    - Convierte "https://youtu.be/ABC123" → "https://www.youtube.com/embed/ABC123"
    """
    # Si la URL es del formato largo (youtube.com/watch?v=...)
    if "youtube.com/watch?v=" in url:
        video_id = url.split("watch?v=")[-1].split("&")[0]  # Extraer solo el ID del video
        return f"https://www.youtube.com/embed/{video_id}"

    # Si la URL es del formato corto (youtu.be/...)
    elif "youtu.be/" in url:
        video_id = url.split("/")[-1].split("?")[0]  # Extraer solo el ID del video
        return f"https://www.youtube.com/embed/{video_id}"

    return url  # Si no es YouTube, devuelve la misma URL sin cambios
