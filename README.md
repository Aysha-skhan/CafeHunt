# CafeHunt ☕

Find good cafés nearby for a lunch or dinner outing  — rating, outdoor seating, distance, and travel time, all in one place instead of flipping between three apps.

Django app backed by the Google Maps Platform APIs (Places + Routes).

## Stack

Python · Django · SQLite · Google Maps Platform (Places API New, Routes API)

## Run it locally

```bash
# activate the virtualenv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # macOS / Linux

pip install -r requirements.txt

# create a .env file in the project root with:
#   GOOGLE_API_KEY=your_key_here

python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000/

## Notes to self

- `.env` (API key) and `db.sqlite3` (local data) are gitignored — supply your own `.env`.
- Needs a Google Cloud key with **Places API (New)** and **Routes API** enabled. Keep the billing budget cap set.
- Outdoor seating comes from Place Details and can be `true` / `false` / missing — modelled as a nullable boolean.

## Roadmap

- [x] Data spike — Places, outdoor seating, routing all proven
- [x] `Cafe` model + migration
- [ ] Search view + caching
- [ ] Map + results UI
- [ ] Deploy
- [ ] Stretch: menu/price extraction (OCR + LLM)
