"""
Art generation for NPC portraits using Google Gemini's image generation API.

This module generates character portrait prompts based on NPC attributes and
uses Gemini 2.5 Flash Image to create the artwork.
"""
import base64

from google import genai
from google.genai import types

from chargen import config
from chargen import constants as c


def _get_client():
    """Get a configured Gemini API client."""
    api_key = config.get('gemini', {}).get('api_key', '')
    if not api_key:
        raise ValueError(
            'Gemini API key not configured. Add api_key to [gemini] in '
            'development-secrets.ini. Get your API key from '
            'https://aistudio.google.com/app/apikey'
        )
    return genai.Client(api_key=api_key)


def generate_prompt(character: dict) -> str:
    """
    Generate an art prompt based on character attributes.

    Args:
        character: A dict containing character attributes (from Character.to_dict())

    Returns:
        str: A prompt suitable for image generation
    """
    # Determine gender pronouns
    gender = character.get('gender', 'male')
    pronoun = 'he' if gender == 'male' else 'she'
    possessive = 'his' if gender == 'male' else 'her'

    # Get clan colors if available
    clan = character.get('clan', '').title()
    clan_colors = c.CLAN_COLORS.get(clan, '')

    # Estimate age based on XP (rough heuristic)
    xp = character.get('xp', 150)
    if xp < 175:
        age_desc = 'early 20s'
    elif xp < 225:
        age_desc = 'late 20s'
    elif xp < 275:
        age_desc = '30s'
    elif xp < 350:
        age_desc = '40s'
    else:
        age_desc = '50s or older'

    # Build character description from traits
    traits = character.get('traits', [])
    trait_descriptions = []
    for trait in traits:
        trait_lower = trait.lower()
        if trait_lower in ['balding', 'bearded', 'long beard', 'bushy beard', 'mustachioed']:
            trait_descriptions.append(f'{pronoun} has {trait_lower} features')
        elif trait_lower in ['thin', 'fat', 'short', 'tall']:
            trait_descriptions.append(f'{pronoun} is {trait_lower}')
        elif trait_lower == 'scarred':
            trait_descriptions.append(f'{pronoun} has visible scars')
        elif trait_lower == 'tattooed':
            trait_descriptions.append(f'{pronoun} has visible tattoos')
        elif trait_lower == 'permanent wound':
            trait_descriptions.append(f'{pronoun} shows signs of an old injury')
        elif trait_lower == 'garishly dressed':
            trait_descriptions.append(f'{pronoun} wears flamboyant, eye-catching clothing')
        elif trait_lower in ['jolly', 'happy', 'lighthearted', 'mirthful', 'upbeat']:
            trait_descriptions.append(f'{pronoun} has a warm, cheerful expression')
        elif trait_lower in ['dour', 'scowling', 'furrowed', 'frowny', 'squinty']:
            trait_descriptions.append(f'{pronoun} has a stern, serious expression')
        elif trait_lower == 'fine makeup':
            trait_descriptions.append(f'{pronoun} wears elegant makeup')
        elif trait_lower == 'jewelried':
            trait_descriptions.append(f'{pronoun} wears fine jewelry')

    # Determine clothing/role - always use kimono for samurai to avoid armor
    school = character.get('school', '').lower()
    if 'bushi' in school:
        clothing = 'a formal kimono'
    elif 'courtier' in school or 'diplomat' in school or 'artisan' in school:
        clothing = 'elegant formal court robes'
    elif 'merchant' in school:
        clothing = 'practical but quality merchant attire'
    else:
        clothing = 'a traditional kimono'

    # Check if character has fine makeup trait
    has_fine_makeup = 'fine makeup' in [t.lower() for t in traits]

    # Build the prompt
    lines = [
        f'A portrait of a {"samurai" if clan else "person"} from {"the " + clan + " clan" if clan else "Rokugan"}.',
        '',
        f'-> {pronoun.title()} is in {possessive} {age_desc}',
    ]

    if clan_colors:
        lines.append(f'-> {pronoun.title()} is wearing {clan} clan colors of {clan_colors}')

    lines.append(f'-> {pronoun.title()} is dressed in {clothing}')

    # For women, specify no makeup unless they have the fine makeup trait
    if gender == 'female' and not has_fine_makeup:
        lines.append(f'-> {pronoun.title()} is not wearing any makeup')

    if trait_descriptions:
        lines.append(f'-> {"; ".join(trait_descriptions)}')

    lines.extend([
        '',
        'Make a colored, photo-realistic, life-like rendering, matching the Legend of '
        'the Five Rings setting of Rokugan, based on Edo-period Japan with period-appropriate '
        'clothing and possessions being shown. The background must be completely blank '
        'without any features - use a solid white background.',
    ])

    return '\n'.join(lines)


def generate_image(prompt: str) -> bytes:
    """
    Generate an image from a prompt using Google Imagen 4.

    Args:
        prompt: The text prompt describing the image to generate

    Returns:
        bytes: The PNG image data
    """
    from io import BytesIO

    client = _get_client()

    response = client.models.generate_images(
        model='imagen-4.0-generate-001',
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio='1:1',  # Square for portraits
        )
    )

    if not response.generated_images:
        raise ValueError('No image was generated. The model may have refused the prompt.')

    # Get the PIL image and convert to PNG bytes
    img = response.generated_images[0].image
    buffer = BytesIO()
    img._pil_image.save(buffer, format='PNG')
    return buffer.getvalue()


def generate_image_base64(prompt: str) -> str:
    """
    Generate an image and return it as a base64-encoded string.

    Args:
        prompt: The text prompt describing the image to generate

    Returns:
        str: Base64-encoded PNG image data (suitable for data: URLs)
    """
    image_bytes = generate_image(prompt)
    return base64.b64encode(image_bytes).decode('utf-8')
