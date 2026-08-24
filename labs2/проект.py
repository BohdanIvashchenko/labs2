from flask import Flask, jsonify, render_template_string, request
import random
from collections import Counter

app = Flask(__name__)

ROWS, REELS = 3, 5
PAYLINES = [
    [1,1,1,1,1], [0,0,0,0,0], [2,2,2,2,2],
    [0,1,2,1,0], [2,1,0,1,2], [0,0,1,0,0],
    [2,2,1,2,2], [0,1,1,1,0], [2,1,1,1,2],
    [0,1,1,1,0]
]
MULTIPLIERS = {3: 5, 4: 15, 5: 50}

HTML = r"""
<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Slot Machine — Python Flask</title>
<style>
body{font-family:Arial,sans-serif;background:#111827;color:#eee;margin:0}
main{max-width:1100px;margin:auto;padding:20px}.card{background:#1f2937;border-radius:14px;padding:18px;margin-bottom:18px}
.grid{display:grid;grid-template-columns:300px 1fr;gap:18px}
input,select,button{width:100%;padding:10px;margin:6px 0;border-radius:8px;border:1px solid #4b5563;background:#111827;color:white}
button{background:#2563eb;border:0;font-weight:bold;cursor:pointer}.secondary{background:#4b5563}
.slot{display:grid;grid-template-columns:repeat(5,1fr);gap:7px}
.reel{display:grid;gap:7px}.cell{height:75px;background:#374151;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:bold}
.win{outline:3px solid #facc15}.wild{color:#67e8f9}.bonus{color:#fb923c}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}.stat{background:#111827;padding:12px;border-radius:9px}.stat b{display:block;font-size:22px;margin-top:5px}
#log{max-height:150px;overflow:auto;font-size:13px}
@media(max-width:800px){.grid{grid-template-columns:1fr}.stats{grid-template-columns:repeat(2,1fr)}}
</style>
</head>
<body>
<main>
<h1>🎰 Симулятор «Однорукого бандита»</h1>
<div class="grid">
<div class="card">
<h3>Налаштування</h3>
<label>Звичайні символи</label>
<input id="symbols" value="A,K,Q,J,9">
<label>Wild</label><input id="wild" value="W">
<label>Bonus/Jackpot</label><input id="bonus" value="B">
<label>Тип бонусу</label>
<select id="mode">
<option value="multiplier">Jackpot ×5</option>
<option value="free_spins">+5 free spins</option>
<option value="respin">Respin</option>
</select>
<label>Кількість симуляцій</label>
<input id="simulations" type="number" min="1" max="1000000" value="10000">
<label>Ставка</label><input id="bet" type="number" min=".01" step=".01" value="1">
<button onclick="spin()">ОБЕРТАННЯ</button>
<button onclick="simulate()">СИМУЛЯЦІЯ</button>
<button class="secondary" onclick="resetStats()">СКИНУТИ</button>
<hr>
<b>Фіксовані параметри:</b>
<p>5 барабанів × 3 рядки</p><p>10 ліній виплат</p>
<p>3 символи = ×5<br>4 = ×15<br>5 = ×50</p>
</div>

<div>
<div class="card">
<div id="slot" class="slot"></div>
<h3 id="result">Натисніть «Обертання»</h3>
</div>
<div class="card">
<h3>Статистика</h3>
<div class="stats">
<div class="stat">RTP <b id="rtp">0%</b></div>
<div class="stat">Hit frequency <b id="hit">0%</b></div>
<div class="stat">Bonus frequency <b id="bonusFreq">0%</b></div>
<div class="stat">Виграш <b id="win">0</b></div>
</div>
<p>Спінів: <span id="spins">0</span></p>
<h3>Розподіл виграшів</h3>
<pre id="distribution">—</pre>
</div>
<div class="card"><h3>Журнал</h3><div id="log"></div></div>
</div>
</div>
</main>

<script>
let lastGrid=[];
function params(){
 return {
  symbols:document.getElementById('symbols').value.split(',').map(x=>x.trim()).filter(Boolean),
  wild:document.getElementById('wild').value.trim()||'W',
  bonus:document.getElementById('bonus').value.trim()||'B',
  mode:document.getElementById('mode').value,
  bet:+document.getElementById('bet').value||1
 };
}
function draw(grid,wins=[]){
 let html='';
 for(let r=0;r<3;r++){
  html+='<div class="reel">';
  for(let c=0;c<5;c++){
   let s=grid[c][r], w=wins.some(x=>x.cells.some(p=>p[0]===c&&p[1]===r));
   html+=`<div class="cell ${s===params().wild?'wild':''} ${s===params().bonus?'bonus':''} ${w?'win':''}">${s}</div>`;
  }
  html+='</div>';
 }
 document.getElementById('slot').innerHTML=html;
}
async function spin(){
 const r=await fetch('/spin',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(params())});
 const d=await r.json(); lastGrid=d.grid; draw(d.grid,d.wins);
 document.getElementById('result').innerHTML=d.message;
 update(d.stats);
 log(d.message);
}
async function simulate(){
 const p=params();p.simulations=Math.min(1000000,Math.max(1,+document.getElementById('simulations').value||1));
 const r=await fetch('/simulate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(p)});
 const d=await r.json(); lastGrid=d.grid; draw(d.grid,[]);
 update(d.stats);
 document.getElementById('result').innerHTML=`Виконано ${p.simulations.toLocaleString('uk-UA')} симуляцій.`;
 log(document.getElementById('result').textContent);
}
async function resetStats(){
 const r=await fetch('/reset',{method:'POST'}); const d=await r.json(); update(d.stats);
 document.getElementById('log').innerHTML='';
}
function update(s){
 document.getElementById('rtp').textContent=s.rtp.toFixed(2)+'%';
 document.getElementById('hit').textContent=s.hit_frequency.toFixed(2)+'%';
 document.getElementById('bonusFreq').textContent=s.bonus_frequency.toFixed(2)+'%';
 document.getElementById('win').textContent=s.total_win.toFixed(2);
 document.getElementById('spins').textContent=s.spins.toLocaleString('uk-UA');
 document.getElementById('distribution').textContent=JSON.stringify(s.distribution,null,2);
}
function log(x){
 const e=document.createElement('div');e.textContent=x;document.getElementById('log').prepend(e);
}
fetch('/state').then(r=>r.json()).then(d=>update(d.stats));
draw([['A','K','Q'],['K','Q','J'],['Q','J','9'],['J','9','A'],['9','A','K']]);
</script>
</body>
</html>
"""

state = {
    "spins": 0, "wins": 0, "bonuses": 0,
    "total_bet": 0.0, "total_win": 0.0,
    "distribution": Counter()
}

def get_config(data):
    symbols = data.get("symbols") or ["A","K","Q","J","9"]
    return {
        "symbols": symbols,
        "wild": data.get("wild") or "W",
        "bonus": data.get("bonus") or "B",
        "mode": data.get("mode") or "multiplier",
        "bet": max(0.01, float(data.get("bet", 1)))
    }

def new_grid(c):
    pool = c["symbols"] + [c["wild"], c["bonus"]]
    return [[random.choice(pool) for _ in range(ROWS)] for _ in range(REELS)]

def evaluate(grid, c):
    total = 0
    wins = []
    bonus_count = sum(s == c["bonus"] for col in grid for s in col)

    for line_no, line in enumerate(PAYLINES, 1):
        target = None
        for col in range(REELS):
            s = grid[col][line[col]]
            if s not in (c["wild"], c["bonus"]):
                target = s
                break
        if target is None:
            continue

        count, cells = 0, []
        for col in range(REELS):
            s = grid[col][line[col]]
            if s == target or s == c["wild"]:
                count += 1
                cells.append([col, line[col]])
            else:
                break

        if count >= 3:
            multiplier = MULTIPLIERS[count]
            amount = c["bet"] * multiplier
            total += amount
            wins.append({
                "line": line_no, "count": count,
                "multiplier": multiplier, "amount": amount,
                "cells": cells
            })

    bonus = bonus_count >= 2
    return total, wins, bonus, bonus_count

def respin(grid, c):
    grid = [col[:] for col in grid]
    changed = []
    pool = c["symbols"] + [c["wild"], c["bonus"]]
    for col in range(REELS):
        if random.random() < .5:
            changed.append(col + 1)
            for row in range(ROWS):
                grid[col][row] = random.choice(pool)
    return grid, changed

def stats():
    s = state
    return {
        "spins": s["spins"],
        "rtp": (s["total_win"] / s["total_bet"] * 100) if s["total_bet"] else 0,
        "hit_frequency": (s["wins"] / s["spins"] * 100) if s["spins"] else 0,
        "bonus_frequency": (s["bonuses"] / s["spins"] * 100) if s["spins"] else 0,
        "total_win": s["total_win"],
        "distribution": dict(sorted(s["distribution"].items(), key=lambda x: float(x[0])))
    }

def one_spin(c, count_stats=True):
    grid = new_grid(c)
    total, wins, bonus, bonus_count = evaluate(grid, c)
    bonus_text = ""

    if bonus:
        if count_stats:
            state["bonuses"] += 1

        if c["mode"] == "multiplier":
            total *= 5
            bonus_text = " | Jackpot ×5"
        elif c["mode"] == "free_spins":
            bonus_text = " | Bonus: +5 free spins"
        elif c["mode"] == "respin":
            grid, changed = respin(grid, c)
            extra, extra_wins, _, _ = evaluate(grid, c)
            total += extra
            wins.extend(extra_wins)
            bonus_text = " | Respin барабанів: " + (
                ", ".join(map(str, changed)) if changed else "без змін"
            )

    return grid, total, wins, bonus, bonus_text

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/state")
def current_state():
    return jsonify(stats=stats())

@app.route("/reset", methods=["POST"])
def reset():
    state.update({
        "spins": 0, "wins": 0, "bonuses": 0,
        "total_bet": 0.0, "total_win": 0.0,
        "distribution": Counter()
    })
    return jsonify(stats=stats())

@app.route("/spin", methods=["POST"])
def spin():
    c = get_config(request.json or {})
    state["spins"] += 1
    state["total_bet"] += c["bet"]

    grid, total, wins, bonus, bonus_text = one_spin(c)

    if total > 0:
        state["wins"] += 1
        state["total_win"] += total
        state["distribution"][str(round(total, 2))] += 1

    if total:
        message = f"Виграш: <b>{total:.2f}</b>{bonus_text}"
    else:
        message = f"Виграш: <b>0.00</b>{bonus_text}"

    return jsonify(grid=grid, wins=wins, message=message, stats=stats())

@app.route("/simulate", methods=["POST"])
def simulate():
    c = get_config(request.json or {})
    n = min(1_000_000, max(1, int(request.json.get("simulations", 10000))))

    for _ in range(n):
        state["spins"] += 1
        state["total_bet"] += c["bet"]
        grid, total, wins, bonus, _ = one_spin(c)

        if total > 0:
            state["wins"] += 1
            state["total_win"] += total
            state["distribution"][str(round(total, 2))] += 1

    return jsonify(grid=grid, stats=stats())

if __name__ == "__main__":
    print("Slot Machine запущено: http://127.0.0.1:5000")
    app.run(debug=True)
