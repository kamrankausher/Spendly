from flask import Flask, render_template, request, redirect, session, url_for, flash, Response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from database.db import get_db
from datetime import datetime, date, timedelta
import calendar, csv, io, json, os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "spendly_v6_dev_fallback_key")
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
def allowed_file(f): return '.' in f and f.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ── Helpers ──────────────────────────────────────────────────────────
@app.context_processor
def inject_user():
    user = None
    if 'user_id' in session:
        conn = get_db()
        row = conn.execute("SELECT * FROM users WHERE id=?",(session['user_id'],)).fetchone()
        conn.close()
        if row: user = dict(row)
    return dict(current_user=user)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*a,**kw):
        if 'user_id' not in session: return redirect(url_for('login'))
        return f(*a,**kw)
    return wrapper

CATEGORIES = [
    ("Food","🍔"),("Transport","🚗"),("Housing","🏠"),("Entertainment","🎬"),
    ("Shopping","🛍️"),("Healthcare","⚕️"),("Education","📚"),("Bills","📃"),("Other","✨")
]
CURRENCY_MAP = {"INR":"₹","USD":"$","EUR":"€","GBP":"£"}

@app.context_processor
def inject_helpers():
    return dict(categories=CATEGORIES, currency_map=CURRENCY_MAP)

# ── Auth ─────────────────────────────────────────────────────────────
@app.route("/")
def landing():
    if 'user_id' in session: return redirect(url_for('dashboard'))
    return render_template("landing.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if 'user_id' in session: return redirect(url_for('dashboard'))
    if request.method=="POST":
        name=request.form.get("name","").strip()
        email=request.form.get("email","").strip()
        password=request.form.get("password","")
        country=request.form.get("country","")
        gender=request.form.get("gender","")
        if not name or not email or not password:
            flash("Name, email, and password are required.","danger")
            return redirect(url_for('register'))
        conn=get_db()
        if conn.execute("SELECT id FROM users WHERE email=?",(email,)).fetchone():
            flash("Email already registered.","danger"); conn.close()
            return redirect(url_for('register'))
        h=generate_password_hash(password)
        cur=conn.execute("INSERT INTO users (name,email,password_hash,country,gender) VALUES (?,?,?,?,?)",(name,email,h,country,gender))
        uid=cur.lastrowid
        conn.execute("INSERT INTO budgets (user_id,amount,period) VALUES (?,?,?)",(uid,5000,"monthly"))
        conn.commit(); conn.close()
        session['user_id']=uid
        flash("Welcome to Spendly! 🎉","success")
        return redirect(url_for('dashboard'))
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if 'user_id' in session: return redirect(url_for('dashboard'))
    if request.method=="POST":
        email=request.form.get("email","").strip()
        password=request.form.get("password","")
        conn=get_db()
        user=conn.execute("SELECT * FROM users WHERE email=?",(email,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password_hash'],password):
            session['user_id']=user['id']
            return redirect(url_for('dashboard'))
        flash("Invalid credentials.","danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('landing'))

# ── Dashboard ────────────────────────────────────────────────────────
@app.route("/dashboard")
@login_required
def dashboard():
    conn=get_db(); uid=session['user_id']; today=date.today()
    
    # Get budget
    budget_row=conn.execute("SELECT amount FROM budgets WHERE user_id=?",(uid,)).fetchone()
    budget=budget_row['amount'] if budget_row else 0
    
    # Define date range
    som=today.replace(day=1).isoformat()
    _,ld=calendar.monthrange(today.year,today.month)
    eom=today.replace(day=ld).isoformat()
    
    # Optimized fetch: Sum directly in SQL
    summary=conn.execute("SELECT COALESCE(SUM(amount),0) as total FROM expenses WHERE user_id=? AND date>=? AND date<=?",(uid,som,eom)).fetchone()
    total_spent=summary['total']
    
    # Recent expenses (limit to 5 for dashboard speed)
    expenses=[dict(r) for r in conn.execute("SELECT * FROM expenses WHERE user_id=? AND date>=? AND date<=? ORDER BY date DESC LIMIT 5",(uid,som,eom)).fetchall()]
    
    # Subscriptions and Goals
    subs=[dict(r) for r in conn.execute("SELECT * FROM subscriptions WHERE user_id=? ORDER BY is_active DESC LIMIT 3",(uid,)).fetchall()]
    goals=[dict(r) for r in conn.execute("SELECT * FROM goals WHERE user_id=? LIMIT 3",(uid,)).fetchall()]
    
    # Category distribution for chart
    cats_query=conn.execute("SELECT category, SUM(amount) as amount FROM expenses WHERE user_id=? AND date>=? AND date<=? GROUP BY category",(uid,som,eom)).fetchall()
    cats={r['category']:r['amount'] for r in cats_query}
    
    conn.close()
    
    remaining=max(0,budget-total_spent)
    pct=min(100,(total_spent/budget)*100) if budget>0 else 0
    
    return render_template("dashboard.html",budget=budget,total_spent=total_spent,remaining=remaining,
        percentage_used=pct,expenses=expenses,subscriptions=subs,goals=goals,cat_data=cats)

# ── Profile ──────────────────────────────────────────────────────────
@app.route("/profile", methods=["GET","POST"])
@login_required
def profile():
    conn=get_db()
    if request.method=="POST":
        f=request.form
        conn.execute("UPDATE users SET name=?,phone=?,age=?,gender=?,country=?,currency=?,language=? WHERE id=?",
            (f.get("name"),f.get("phone"),int(f.get("age") or 0),f.get("gender"),f.get("country"),f.get("currency"),f.get("language"),session['user_id']))
        new_pw=f.get("new_password","").strip()
        if new_pw:
            conn.execute("UPDATE users SET password_hash=? WHERE id=?",(generate_password_hash(new_pw),session['user_id']))
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file and file.filename and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"avatar_{session['user_id']}.{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                conn.execute("UPDATE users SET avatar_url=? WHERE id=?", (f"/static/uploads/{filename}", session['user_id']))
        conn.commit()
        flash("Profile saved.","success")
    user=dict(conn.execute("SELECT * FROM users WHERE id=?",(session['user_id'],)).fetchone())
    conn.close()
    return render_template("profile.html",user=user)

# ── Reports ──────────────────────────────────────────────────────────
@app.route("/reports")
@login_required
def reports():
    conn=get_db(); uid=session['user_id']
    cats=[dict(r) for r in conn.execute("SELECT category,SUM(amount) as total,COUNT(*) as cnt FROM expenses WHERE user_id=? GROUP BY category ORDER BY total DESC",(uid,)).fetchall()]
    expenses=[dict(r) for r in conn.execute("SELECT * FROM expenses WHERE user_id=? ORDER BY date DESC LIMIT 50",(uid,)).fetchall()]
    subs=[dict(r) for r in conn.execute("SELECT * FROM subscriptions WHERE user_id=?",(uid,)).fetchall()]
    budget_row=conn.execute("SELECT amount FROM budgets WHERE user_id=?",(uid,)).fetchone()
    budget=budget_row['amount'] if budget_row else 0
    total=sum(c['total'] for c in cats)
    monthly_raw=conn.execute("SELECT strftime('%Y-%m', date) as month, SUM(amount) as total FROM expenses WHERE user_id=? GROUP BY month ORDER BY month DESC LIMIT 6",(uid,)).fetchall()
    monthly_trends=[dict(r) for r in monthly_raw]; monthly_trends.reverse()
    conn.close()
    return render_template("reports.html",categories=cats,expenses=expenses,subscriptions=subs,budget=budget,total_spent=total,monthly_trends=monthly_trends)

@app.route("/export")
@login_required
def export_csv():
    conn=get_db()
    rows=conn.execute("SELECT date,category,amount,description FROM expenses WHERE user_id=? ORDER BY date DESC",(session['user_id'],)).fetchall()
    conn.close()
    si=io.StringIO(); w=csv.writer(si)
    w.writerow(['Date','Category','Amount','Description'])
    for r in rows: w.writerow([r['date'],r['category'],r['amount'],r['description']])
    return Response(si.getvalue(),mimetype="text/csv",headers={"Content-disposition":"attachment; filename=spendly_report.csv"})

# ── Alerts (Subscriptions) ───────────────────────────────────────────
@app.route("/alerts")
@login_required
def alerts():
    conn=get_db()
    subs=[dict(r) for r in conn.execute("SELECT * FROM subscriptions WHERE user_id=? ORDER BY is_active DESC, end_date ASC",(session['user_id'],)).fetchall()]
    conn.close()
    return render_template("alerts.html",subscriptions=subs)

@app.route("/subscriptions/add", methods=["POST"])
@login_required
def add_subscription():
    f=request.form; conn=get_db()
    conn.execute("INSERT INTO subscriptions (user_id,platform,cost,start_date,end_date,duration_months,is_active) VALUES (?,?,?,?,?,?,1)",
        (session['user_id'],f.get("platform"),float(f.get("cost",0)),f.get("start_date"),f.get("end_date"),int(f.get("duration",1))))
    conn.commit(); conn.close()
    flash("Subscription added.","success")
    return redirect(url_for('alerts'))

@app.route("/subscriptions/<int:sid>/toggle")
@login_required
def toggle_sub(sid):
    conn=get_db()
    row=conn.execute("SELECT is_active FROM subscriptions WHERE id=? AND user_id=?",(sid,session['user_id'])).fetchone()
    if row: conn.execute("UPDATE subscriptions SET is_active=? WHERE id=?",(0 if row['is_active'] else 1,sid)); conn.commit()
    conn.close()
    return redirect(url_for('alerts'))

@app.route("/subscriptions/<int:sid>/delete")
@login_required
def delete_sub(sid):
    conn=get_db()
    conn.execute("DELETE FROM subscriptions WHERE id=? AND user_id=?",(sid,session['user_id']))
    conn.commit(); conn.close()
    flash("Subscription removed.","success")
    return redirect(url_for('alerts'))

# ── Tracking ─────────────────────────────────────────────────────────
@app.route("/tracking")
@login_required
def tracking():
    conn=get_db(); uid=session['user_id']; today=date.today()
    filt=request.args.get('filter','all')
    if filt=='week': sd=(today-timedelta(days=7)).isoformat()
    elif filt=='month': sd=today.replace(day=1).isoformat()
    elif filt=='60days': sd=(today-timedelta(days=60)).isoformat()
    elif filt=='year': sd=date(today.year,1,1).isoformat()
    else: sd="2000-01-01"
    
    # Combined fetching
    expenses=[dict(r) for r in conn.execute("SELECT * FROM expenses WHERE user_id=? AND date>=? ORDER BY date DESC",(uid,sd)).fetchall()]
    subs=[dict(r) for r in conn.execute("SELECT * FROM subscriptions WHERE user_id=?",(uid,)).fetchall()]
    
    # Aggregated category data for tips
    cats_query=conn.execute("SELECT category, SUM(amount) as total FROM expenses WHERE user_id=? AND date>=? GROUP BY category",(uid,sd)).fetchall()
    cats={r['category']:r['total'] for r in cats_query}
    total=sum(cats.values())
    
    suggestions=[]
    for cat in ["Entertainment","Shopping","Food","Other"]:
        if cat in cats and total>0:
            pct=(cats[cat]/total)*100
            if pct>15:
                suggestions.append({"category":cat,"amount":cats[cat],"pct":round(pct,1),
                    "tip":f"You're spending {pct:.0f}% on {cat}. Reducing by 20% could save you ₹{cats[cat]*0.2:,.0f} this period.",
                    "severity":"high" if pct>30 else "medium"})
    if not suggestions and total>0:
        suggestions.append({"category":"General","amount":total,"pct":100,"tip":"Great job! Your spending looks balanced. 🎉","severity":"low"})
    conn.close()
    return render_template("tracking.html",expenses=expenses,subscriptions=subs,suggestions=suggestions,cat_data=cats,current_filter=filt)

@app.route("/expenses/add", methods=["POST"])
@login_required
def add_expense():
    f=request.form; conn=get_db()
    conn.execute("INSERT INTO expenses (user_id,amount,category,date,description) VALUES (?,?,?,?,?)",
        (session['user_id'],float(f.get("amount",0)),f.get("category"),f.get("date"),f.get("description","")))
    conn.commit(); conn.close()
    flash(f"₹{f.get('amount')} recorded for {f.get('category')}.","success")
    return redirect(request.referrer or url_for('dashboard'))

@app.route("/expenses/<int:eid>/edit", methods=["POST"])
@login_required
def edit_expense(eid):
    f=request.form; conn=get_db()
    conn.execute("UPDATE expenses SET amount=?,category=?,date=?,description=? WHERE id=? AND user_id=?",
        (float(f.get("amount",0)),f.get("category"),f.get("date"),f.get("description",""),eid,session['user_id']))
    conn.commit(); conn.close()
    flash("Transaction updated.","success")
    return redirect(url_for('tracking'))

@app.route("/expenses/<int:eid>/delete")
@login_required
def delete_expense(eid):
    conn=get_db()
    conn.execute("DELETE FROM expenses WHERE id=? AND user_id=?",(eid,session['user_id']))
    conn.commit(); conn.close()
    flash("Transaction deleted.","success")
    return redirect(request.referrer or url_for('tracking'))

@app.route("/budget/update", methods=["POST"])
@login_required
def update_budget():
    conn=get_db()
    conn.execute("UPDATE budgets SET amount=? WHERE user_id=?",(float(request.form.get("amount",0)),session['user_id']))
    conn.commit(); conn.close()
    flash("Budget updated.","success")
    return redirect(url_for('dashboard'))

# ── Goals ────────────────────────────────────────────────────────────
@app.route("/goals")
@login_required
def goals_page():
    conn=get_db()
    goals=[dict(r) for r in conn.execute("SELECT * FROM goals WHERE user_id=? ORDER BY deadline ASC",(session['user_id'],)).fetchall()]
    conn.close()
    return render_template("goals.html",goals=goals)

@app.route("/goals/add", methods=["POST"])
@login_required
def add_goal():
    f=request.form; conn=get_db()
    conn.execute("INSERT INTO goals (user_id,title,target_amount,saved_amount,deadline) VALUES (?,?,?,?,?)",
        (session['user_id'],f.get("title"),float(f.get("target",0)),float(f.get("saved",0)),f.get("deadline")))
    conn.commit(); conn.close()
    flash("Goal created! 🎯","success")
    return redirect(url_for('goals_page'))

@app.route("/goals/<int:gid>/update", methods=["POST"])
@login_required
def update_goal(gid):
    conn=get_db()
    conn.execute("UPDATE goals SET saved_amount=? WHERE id=? AND user_id=?",(float(request.form.get("saved",0)),gid,session['user_id']))
    conn.commit(); conn.close()
    flash("Goal progress updated.","success")
    return redirect(url_for('goals_page'))

@app.route("/goals/<int:gid>/delete")
@login_required
def delete_goal(gid):
    conn=get_db()
    conn.execute("DELETE FROM goals WHERE id=? AND user_id=?",(gid,session['user_id']))
    conn.commit(); conn.close()
    flash("Goal removed.","success")
    return redirect(url_for('goals_page'))

# ── Scanner ──────────────────────────────────────────────────────────
@app.route("/scanner")
@login_required
def scanner():
    return render_template("scanner.html")

# ── Analytics ────────────────────────────────────────────────────────
@app.route("/analytics")
@login_required
def analytics():
    conn=get_db(); uid=session['user_id']; today=date.today()
    # Category totals
    cats=[dict(r) for r in conn.execute("SELECT category,SUM(amount) as total,COUNT(*) as cnt FROM expenses WHERE user_id=? GROUP BY category ORDER BY total DESC",(uid,)).fetchall()]
    # Monthly trend
    monthly=[dict(r) for r in conn.execute("SELECT strftime('%Y-%m', date) as month, SUM(amount) as total FROM expenses WHERE user_id=? GROUP BY month ORDER BY month DESC LIMIT 12",(uid,)).fetchall()]
    monthly.reverse()
    # Budget
    budget_row=conn.execute("SELECT amount FROM budgets WHERE user_id=?",(uid,)).fetchone()
    budget=budget_row['amount'] if budget_row else 0
    # This month spending
    som=today.replace(day=1).isoformat()
    total_this_month=conn.execute("SELECT COALESCE(SUM(amount),0) as s FROM expenses WHERE user_id=? AND date>=?",(uid,som)).fetchone()['s']
    # Total all time
    total_all=sum(c['total'] for c in cats)
    # Transaction count
    txn_count=conn.execute("SELECT COUNT(*) as c FROM expenses WHERE user_id=?",(uid,)).fetchone()['c']
    # Avg daily (this month)
    days_elapsed=max(1,(today - today.replace(day=1)).days + 1)
    avg_daily=total_this_month / days_elapsed
    # Highest category
    top_cat=cats[0] if cats else {"category":"None","total":0}
    # Financial Health Score (0-100)
    score=100
    if budget>0:
        spend_ratio=total_this_month/budget
        if spend_ratio>1: score=max(10, int(100-spend_ratio*50))
        elif spend_ratio>0.8: score=int(100-(spend_ratio-0.8)*200)
        else: score=min(100, int(100-(spend_ratio*20)))
    # Insights
    insights=[]
    if budget>0:
        pct_used=(total_this_month/budget)*100
        if pct_used > 90:
            insights.append({"icon":"🚨","text":f"You've used <strong>{pct_used:.0f}%</strong> of your budget. Consider pausing non-essential spending."})
        elif pct_used > 70:
            insights.append({"icon":"⚡","text":f"<strong>{pct_used:.0f}%</strong> of budget used. You're on track but be mindful of big purchases."})
        else:
            insights.append({"icon":"🏆","text":f"Excellent! Only <strong>{pct_used:.0f}%</strong> used. You're well within your budget this month."})
    if top_cat['total']>0:
        insights.append({"icon":"📊","text":f"Your highest spending category is <strong>{top_cat['category']}</strong> at ₹{top_cat['total']:,.0f}."})
    if avg_daily > 0:
        monthly_proj = avg_daily * 30
        insights.append({"icon":"📈","text":f"At your current rate of ₹{avg_daily:,.0f}/day, you'll spend ~₹{monthly_proj:,.0f} by month end."})
    goals=[dict(r) for r in conn.execute("SELECT * FROM goals WHERE user_id=?",(uid,)).fetchall()]
    active_goals=len(goals)
    total_saved=sum(g['saved_amount'] for g in goals)
    conn.close()
    return render_template("analytics.html",cats=cats,monthly=monthly,budget=budget,
        total_month=total_this_month,total_all=total_all,txn_count=txn_count,
        avg_daily=avg_daily,top_cat=top_cat,score=score,insights=insights,
        active_goals=active_goals,total_saved=total_saved)

# ── API ──────────────────────────────────────────────────────────────
@app.route("/api/summary")
@login_required
def api_summary():
    conn=get_db(); uid=session['user_id']; today=date.today()
    budget_row=conn.execute("SELECT amount FROM budgets WHERE user_id=?",(uid,)).fetchone()
    budget=budget_row['amount'] if budget_row else 0
    som=today.replace(day=1).isoformat()
    _,ld=calendar.monthrange(today.year,today.month)
    eom=today.replace(day=ld).isoformat()
    rows=conn.execute("SELECT category,SUM(amount) as total FROM expenses WHERE user_id=? AND date>=? AND date<=? GROUP BY category",(uid,som,eom)).fetchall()
    cats={r['category']:r['total'] for r in rows}
    total_spent=sum(cats.values())
    conn.close()
    return jsonify({"budget":budget,"spent":total_spent,"remaining":max(0,budget-total_spent),"categories":cats})

# ── Initialize DB on first run ───────────────────────────────────────
from database.db import init_db as _idb, seed_db as _sdb
_idb() # Safe now (uses CREATE TABLE IF NOT EXISTS)
_sdb() # Safe now (checks if users exist before seeding)

if __name__=="__main__":
    app.run(debug=True, port=5001)
