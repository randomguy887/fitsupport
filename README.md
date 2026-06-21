# FitSupport
## Personalised Nutrition & Supplement Guidance System
### LJMU BSc Computer Science Final Year Project

---

## What This Project Does
FitSupport takes your age, weight, height, activity level, and fitness goal —
and calculates your personalised daily calorie needs, macronutrients, hydration,
and evidence-based supplement recommendations.

---

## Project Structure

```
fitsupport/
│
├── app.py                        ← Main Streamlit UI (run this)
│
├── core/
│   ├── nutrition_engine.py       ← BMR, TDEE, macro, water calculations
│   ├── supplement_engine.py      ← Rule-based supplement recommendations
│   └── data_store.py             ← SQLite anonymous session logging
│
├── data/
│   └── fitsupport.db             ← Auto-created SQLite database
│
├── tests/
│   ├── test_nutrition_engine.py  ← Unit tests for nutrition calculations
│   └── test_supplement_engine.py ← Unit tests for supplement logic
│
├── requirements.txt              ← Python dependencies
└── README.md                     ← This file
```

---

## How to Run

### Step 1 – Install Python
Download Python 3.11 from https://www.python.org/downloads/
✅ Tick "Add Python to PATH" during installation

### Step 2 – Open Terminal / Command Prompt
- Windows: Search "cmd" in Start Menu
- Mac: Search "Terminal" in Spotlight

### Step 3 – Navigate to the project folder
```
cd Desktop/fitsupport
```

### Step 4 – Install dependencies
```
pip install -r requirements.txt
```

### Step 5 – Run the app
```
streamlit run app.py
```

The app will open automatically in your browser at http://localhost:8501

### Step 6 – Run tests
```
python -m pytest tests/ -v
```

---

## Ethics Statement
- No personal identifying information is collected
- Age, weight, height, activity level, and fitness goals only
- All data is anonymous and stored locally
- Used exclusively for academic evaluation purposes
- All supplement advice is educational, not medical advice

---

## References (Key)
- Mifflin MD, St Jeor ST et al. (1990). A new predictive equation for resting energy expenditure. *Am J Clin Nutr.*
- Morton RW et al. (2018). A systematic review, meta-analysis and meta-regression of the effect of protein supplementation on resistance training–induced gains. *Br J Sports Med.*
- Kreider RB et al. (2017). International Society of Sports Nutrition position stand: safety and efficacy of creatine supplementation. *J Int Soc Sports Nutr.*
