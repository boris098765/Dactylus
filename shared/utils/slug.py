from slugify import slugify

def generate_slug(text: str) -> str:
    slug = slugify(text)
    return slug
