# 🧠 Semantic Color API — For Total Beginners

This is a super simple guide to using the API. You don't need to know much, just follow along!

---

## ✅ What This API Does

You give it a phrase like:
```
"I want something bold and calm"
```
And it gives you back:
- The important words from your phrase
- A color (in RGB format) for each word
- A picture showing your phrase as a color palette with shifting momentum

---

## 🚀 How to Use It (The Easy Way)

### 1. Open the API in your browser:
Go to:
```
https://la_matriz_api.up.railway.app/docs
```
You'll see a pretty page where you can try out the API.

### 2. Click on the `/analyze` POST box
It looks like this:
```
POST /analyze
```

### 3. Click "Try it out" → Paste this into the box:
```json
{
  "phrase": "I want something bold and calm",
  "length": 4,
  "momentum": "original"
}
```

### 4. Click Execute ✅
You’ll see a response like:
```json
{
  "seed_words": ["bold", "calm"],
  "rgb_sequence": [[220, 30, 30], [100, 200, 180]],
  "image_url": "/static/palette.png"
}
```
Then open this in your browser:
```
https://la_matriz_api.up.railway.app/static/palette.png
```
To see your color palette!

---

## 💬 What Do These Inputs Mean?
- `phrase`: A string of words you want turned into colors.
- `length`: How many colors to return.
  - 📏 Must be an integer from **1 to 20** (recommended range)
- `momentum`: Controls how color transitions are computed.
  - Valid values:
    - `original`: (default) direct mapping to seed words
    - `smooth`: blend colors gradually
    - `wave`: applies an oscillating brightness curve
    - `random`: scrambles the color order

---

## 💡 Example Uses
- Designers looking for emotional color palettes
- Artists, poets, product creators
- People who want colors to match their message

---

## 🛠️ Developers
If you're a dev, use this cURL:
```bash
curl -X POST https://la_matriz_api.up.railway.app/analyze \
  -H "Content-Type: application/json" \
  -d '{
        "phrase": "serene but energetic nature",
        "length": 5,
        "momentum": "smooth"
      }'
```

---

## 🤷 Need Help?
DM the creator or open an issue on GitHub.
You got this. 💪
