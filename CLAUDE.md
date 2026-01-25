# L5R NPC Generator - Project Persona

## System Role
You are an expert Python developer.  You are assisting in building a webapp to
generate NPCs for the Rokugan setting.

## Environment & Commands
- **Python Version**: 3.10
- **Virtual Env**: `./env`
- **Install**: `./env/bin/pip install -r requirements.txt` (Note: Use pip-compile via requirements.in)
- **Run Server**: `./env/bin/cherryd --import chargen` (Runs at http://127.0.0.1:8080)
- **Tests**: `./env/bin/pytest` (Standard location: /tests)

## Technical Constraints
- **Configuration**: Use `ConfigObj`. Validation is in `chargen/configspec.ini`. Never hardcode constants that belong in config.
- **Naming**: Use `chargen/constants.py` for gendered names. Use the `unused_name` logic to avoid duplicates.
- **Image Generation (Art)**: When generating image prompts for NPCs:
  - **Style**: Photo-realistic, colored, life-like rendering.
  - **Setting**: Edo-period Japan / Rokugan appropriate.
  - **Subject**: Single NPC with period-appropriate clothing (Kimono, Armor, etc.).
  - **Background**: MUST be completely blank/solid white with no features.

## Coding Style
- Follow the existing pattern in `character.py` for class inheritance (`Samurai`, `Monk`, `Peasant`).
- Use the `weighted_choice` utility for randomizing attributes based on config weights.
- Ensure `to_dict()` is updated if new character attributes are added.
- Use single quotes for strings and triple-double-quotes for docstrings.

## Project Status & Roadmap
- [x] Basic character generation logic (Samurai, Monk, Peasant).
- [x] Web frontend (CherryPy + Jinja2 + jQuery).
- [ ] **OAuth 1.0 Implementation**: The skeleton exists in `op.py` but is non-functional. 
  - Use the Obsidian Portal API docs as a reference.
  - Secrets should be stored in `development-secrets.ini` via ConfigObj.
- [ ] **Character Upload**: The `create_character` function in `op.py` needs to map the `Character` object to the OP API schema.
- [ ] **Art Pipeline**: Currently no art generation. Future goal is to add a button to the UI that calls an image API and saves the result to the NPC's description.  I want to be able to approve the generated art prior to saving it to Obsidian Portal and have the option to tweak the prompt manually.
