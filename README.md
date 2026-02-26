# Quoridor Bot (EDA Mendoza 2022)

Bot en **Python** para competir en un torneo de **Quoridor** (Engineering Development Academy Mendoza 2022 – Eventbrite). Se conecta por **WebSocket**, acepta desafíos y juega automáticamente (movimientos + colocación de paredes).

## Qué hay en este repo

- `main.py`: cliente WebSocket + lógica de juego del bot
- `test_main.py`: unit tests para helpers de movimiento

## Requisitos

- Python 3.8+ (recomendado)
- Dependencia:
  - `websockets`

## Instalación:

```bash
pip install websockets
```

## Uso

El bot necesita un auth_token provisto por la plataforma/torneo.
```bash
python main.py <AUTH_TOKEN>
```

Qué hace al correr:
- Se conecta al servidor WebSocket
- Imprime mensajes entrantes en consola
- Si recibe `challenge`, lo acepta automáticamente
- Si recibe `your_turn`, decide la jugada y envía: `move` o `wall`

## Tests

Ejecutar unit tests:
```bash
python -m unittest -v
```

Los tests cubren:
	•	move_forward(side, row, col)
	•	move_sideways(row, col)
