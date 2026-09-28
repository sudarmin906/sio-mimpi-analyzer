
import os, re, csv, json, math, sqlite3, hashlib, io
from datetime import datetime, timezone
from pathlib import Path
from flask import Flask, request, jsonify, Response

BASE=Path(__file__).resolve().parent
DB=Path(os.environ.get("DB_PATH", BASE/"app.db"))
DEFAULT_MAP={'01': 'Setan', '13': 'Mahi', '25': 'Natsu', '37': 'Kecewa', '49': 'Neraka', '61': 'Kalah', '73': 'Imbalan', '85': 'Hangus', '97': 'Besar', '02': 'Iblis', '14': 'Siksa', '26': 'Bahaya', '38': 'Bajingan', '50': 'Serakah', '62': 'Hina', '74': 'Payudara', '86': 'Pujian', '98': 'Birahi', '03': 'Jin', '15': 'Ngeri', '27': 'Tangis', '39': 'Menari', '51': 'Isap Lidah', '63': 'Kabur', '75': 'Bosan', '87': 'Pusing', '99': 'Pasangan', '04': 'Insaf', '16': 'Sengsara', '28': 'Korban', '40': 'Disukai', '52': 'Kubur', '64': 'Cantik', '76': 'Bantah', '88': 'Perbuatan', '00': 'Mati', '12': 'Penyakit', '05': 'Dokter', '17': 'Celaka', '29': 'Terbunuh', '41': 'Kecurian', '53': 'Maut', '65': 'Bregsek', '77': 'Kecewa', '89': 'Takut', '06': 'Sundal', '18': 'Sial', '30': 'Binasa', '42': 'Jurang', '54': 'Draw', '66': 'Nakal', '78': 'Durhaka', '90': 'Langsung', '07': 'Gila', '19': 'Bahagia', '31': 'Penjara', '43': 'Kejam', '55': 'Indah', '67': 'Begal', '79': 'Melempar', '91': 'Telanjang Bulat', '08': 'Penggoda', '20': 'Mampus', '32': 'Hukuman', '44': 'TBC', '56': 'Tertawa', '68': 'Rusak', '80': 'Bingung', '92': 'Dambaan', '09': 'Risau', '21': 'Ikat diri', '33': 'Terbakar', '45': 'Gantung Diri', '57': 'Menjolok', '69': 'Menghajar', '81': 'Merantau', '93': 'Zina', '10': 'Kotor', '22': 'Bunuh Diri', '34': 'Api', '46': 'Telanjang', '58': 'Marah', '70': 'Puji Diri', '82': 'Lancang', '94': 'Perkosa', '11': 'Sipilis', '23': 'Benci', '35': 'Derita', '47': 'Gila Pangkat', '59': 'Tersinggung', '71': 'Berkelana', '83': 'Cinta', '95': 'Hamil', '24': 'Berani', '36': 'Biadab', '48': 'Calon Mati', '60': 'Sakit Hati', '72': 'Keinginan', '84': 'Ciuman', '96': 'Mendapat Malu'}
SEED_CSV='period,result,source\r\n13995,9659,seed_14123\r\n13996,3393,seed_14123\r\n13997,7296,seed_14123\r\n13998,6541,seed_14123\r\n13999,9969,seed_14123\r\n14000,5299,seed_14123\r\n14001,6136,seed_14123\r\n14002,5178,seed_14123\r\n14003,9582,seed_14123\r\n14004,7716,seed_14123\r\n14009,9395,seed_14123\r\n14010,0034,seed_14123\r\n14011,7140,seed_14123\r\n14012,3042,seed_14123\r\n14013,4244,seed_14123\r\n14014,0457,seed_14123\r\n14015,0880,seed_14123\r\n14016,4607,seed_14123\r\n14017,7595,seed_14123\r\n14018,5859,seed_14123\r\n14019,5100,seed_14123\r\n14020,9849,seed_14123\r\n14021,0702,seed_14123\r\n14022,6745,seed_14123\r\n14023,3847,seed_14123\r\n14024,0690,seed_14123\r\n14025,6854,seed_14123\r\n14026,2600,seed_14123\r\n14027,8682,seed_14123\r\n14028,8576,seed_14123\r\n14029,1886,seed_14123\r\n14030,0809,seed_14123\r\n14031,7488,seed_14123\r\n14032,0589,seed_14123\r\n14033,8660,seed_14123\r\n14034,8584,seed_14123\r\n14035,5073,seed_14123\r\n14036,7866,seed_14123\r\n14037,7270,seed_14123\r\n14038,4522,seed_14123\r\n14039,1916,seed_14123\r\n14040,2400,seed_14123\r\n14041,2272,seed_14123\r\n14042,6975,seed_14123\r\n14043,2127,seed_14123\r\n14044,9094,seed_14123\r\n14045,0123,seed_14123\r\n14046,7796,seed_14123\r\n14047,5322,seed_14123\r\n14048,7152,seed_14123\r\n14049,4899,seed_14123\r\n14050,6348,seed_14123\r\n14051,7687,seed_14123\r\n14052,2807,seed_14123\r\n14053,8093,seed_14123\r\n14054,0810,seed_14123\r\n14055,1205,seed_14123\r\n14056,4243,seed_14123\r\n14057,4293,seed_14123\r\n14058,8690,seed_14123\r\n14059,0481,seed_14123\r\n14060,1326,seed_14123\r\n14061,2036,seed_14123\r\n14062,6360,seed_14123\r\n14063,7694,seed_14123\r\n14064,4443,seed_14123\r\n14065,0485,seed_14123\r\n14066,4457,seed_14123\r\n14067,6578,seed_14123\r\n14068,7021,seed_14123\r\n14069,6785,seed_14123\r\n14070,4319,seed_14123\r\n14071,2856,seed_14123\r\n14072,7810,seed_14123\r\n14073,6613,seed_14123\r\n14074,4392,seed_14123\r\n14075,9890,seed_14123\r\n14076,3584,seed_14123\r\n14077,9458,seed_14123\r\n14078,0066,seed_14123\r\n14079,2755,seed_14123\r\n14080,5927,seed_14123\r\n14081,6218,seed_14123\r\n14082,0266,seed_14123\r\n14083,4663,seed_14123\r\n14084,1621,seed_14123\r\n14085,1037,seed_14123\r\n14086,6704,seed_14123\r\n14087,7209,seed_14123\r\n14088,1508,seed_14123\r\n14089,7094,seed_14123\r\n14090,4126,seed_14123\r\n14091,0567,seed_14123\r\n14092,0495,seed_14123\r\n14093,2613,seed_14123\r\n14094,4148,seed_14123\r\n14095,5231,seed_14123\r\n14096,2909,seed_14123\r\n14097,6308,seed_14123\r\n14098,3159,seed_14123\r\n14099,8651,seed_14123\r\n14100,4169,seed_14123\r\n14101,9700,seed_14123\r\n14102,6944,seed_14123\r\n14103,8139,seed_14123\r\n14104,7420,seed_14123\r\n14105,7575,seed_14123\r\n14106,6417,seed_14123\r\n14107,3676,seed_14123\r\n14108,7350,seed_14123\r\n14109,5337,seed_14123\r\n14110,8359,seed_14123\r\n14111,8287,seed_14123\r\n14112,9349,seed_14123\r\n14113,8957,seed_14123\r\n14114,8099,seed_14123\r\n14115,1018,seed_14123\r\n14116,6550,seed_14123\r\n14117,0493,seed_14123\r\n14118,9221,seed_14123\r\n14119,7720,seed_14123\r\n14120,5445,seed_14123\r\n14121,4194,seed_14123\r\n14122,6381,seed_14123\r\n14123,6065,seed_14123\r\n'

app=Flask(__name__)
app.config["MAX_CONTENT_LENGTH"]=25*1024*1024

def now():
    return datetime.now(timezone.utc).isoformat()

def db():
    conn=sqlite3.connect(DB)
    conn.row_factory=sqlite3.Row
    return conn

def init_db():
    conn=db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS history(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      period INTEGER,
      result TEXT NOT NULL,
      source TEXT,
      created_at TEXT NOT NULL,
      UNIQUE(period, result)
    );
    CREATE TABLE IF NOT EXISTS mapping(
      pair TEXT PRIMARY KEY,
      meaning TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS runs(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      cutoff_result TEXT NOT NULL,
      main TEXT NOT NULL,
      backups TEXT NOT NULL,
      bbfs TEXT NOT NULL,
      candidates TEXT NOT NULL,
      created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS audits(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      run_id INTEGER NOT NULL,
      actual TEXT NOT NULL,
      main_exact INTEGER NOT NULL,
      main_reverse INTEGER NOT NULL,
      top3_exact INTEGER NOT NULL,
      top5_exact INTEGER NOT NULL,
      top5_mixed INTEGER NOT NULL,
      head_exact INTEGER NOT NULL,
      tail_exact INTEGER NOT NULL,
      bbfs_hit INTEGER NOT NULL,
      bbfs_unique INTEGER NOT NULL,
      created_at TEXT NOT NULL
    );
    """)
    if conn.execute("SELECT COUNT(*) c FROM mapping").fetchone()["c"]==0:
        conn.executemany("INSERT OR REPLACE INTO mapping(pair,meaning) VALUES(?,?)",DEFAULT_MAP.items())
    if conn.execute("SELECT COUNT(*) c FROM history").fetchone()["c"]==0:
        for row in csv.DictReader(io.StringIO(SEED_CSV)):
            conn.execute("INSERT OR IGNORE INTO history(period,result,source,created_at) VALUES(?,?,?,?)",
                         (int(row["period"]),row["result"],row["source"],now()))
    conn.commit(); conn.close()

def norm4(x):
    s=str(x).strip()
    return s.zfill(4) if re.fullmatch(r"\d{1,4}",s) else None

def rev(p): return p[::-1]
def pairs(r):
    return [r[:2],r[1:3],r[2:4]]
def uniq(seq):
    return list(dict.fromkeys(seq))

def get_history():
    conn=db()
    rows=conn.execute("SELECT period,result FROM history ORDER BY period ASC, id ASC").fetchall()
    conn.close()
    return [(r["period"],r["result"]) for r in rows]

def get_map():
    conn=db(); rows=conn.execute("SELECT pair,meaning FROM mapping").fetchall(); conn.close()
    return {r["pair"]:r["meaning"] for r in rows}

def set_map(m):
    conn=db()
    conn.execute("DELETE FROM mapping")
    conn.executemany("INSERT OR REPLACE INTO mapping(pair,meaning) VALUES(?,?)",m.items())
    conn.commit(); conn.close()

def pair_counts(history, window=100):
    # history is chronological list of (period,result)
    recent=history[-window:]
    counts={}
    for idx,(p,r) in enumerate(recent):
        w=1.0+idx/max(1,len(recent)-1)
        for q in pairs(r)+[rev(x) for x in pairs(r)]:
            counts[q]=counts.get(q,0)+w
    return counts

def semantic_overlap(a,b,mapping):
    ta=set(re.findall(r"[a-zA-ZÀ-ÿ]+",mapping.get(a,"").lower()))
    tb=set(re.findall(r"[a-zA-ZÀ-ÿ]+",mapping.get(b,"").lower()))
    if not ta or not tb: return 0.0
    return len(ta&tb)/max(1,min(len(ta),len(tb)))

def candidate_pool(history, cutoff, mapping):
    # Pair Assembly + Recovery: assemble from digit support of recent results
    counts=pair_counts(history,100)
    latest=cutoff
    seed=pairs(latest)
    seed_rev=[rev(x) for x in seed]
    seed_all=uniq(seed+seed_rev)
    digit_scores={}
    for i,d in enumerate(latest):
        digit_scores[d]=digit_scores.get(d,0)+2.0/(i+1)
    for r in [x[1] for x in history[-30:]]:
        for i,d in enumerate(r):
            digit_scores[d]=digit_scores.get(d,0)+0.25*(1/(i+1))
    ranked_digits=sorted("0123456789",key=lambda d:(-digit_scores.get(d,0),d))
    candidates=set(counts.keys())
    # cross assembly
    for a in ranked_digits[:7]:
        for b in ranked_digits[:7]:
            candidates.add(a+b)
    # recovery around rejected/seed semantic relatives
    for s in seed_all:
        for c in counts:
            if semantic_overlap(s,c,mapping)>0:
                candidates.add(c)
    # score
    scored=[]
    for c in candidates:
        if len(c)!=2 or not c.isdigit(): continue
        freq=math.log1p(counts.get(c,0))
        pos=0
        for j,s in enumerate(seed_all):
            if c==s: pos+=2.2
            elif c==rev(s): pos+=1.6
            elif c[0] in s: pos+=0.35
            if semantic_overlap(c,s,mapping): pos+=0.5*semantic_overlap(c,s,mapping)
        recovery=0.0
        if c[0]==c[1]: recovery+=0.6
        if c[0] in latest or c[1] in latest: recovery+=0.3
        chase=0.0
        if c in seed_all: chase=0.75
        score=freq+pos+recovery-chase
        scored.append((score,c))
    scored.sort(key=lambda x:(-x[0],x[1]))
    # Anti-chasing: keep strongest but don't let latest exact seed pairs dominate
    return [c for _,c in scored[:40]]

def generate(history_before, mapping):
    if not history_before:
        return {"main":"00","backups":["01","02","03","04"],"bbfs":"012345","candidates":["00","01","02","03","04"]}
    cutoff=history_before[-1][1]
    cand=candidate_pool(history_before[:-1],cutoff,mapping)
    cand=uniq(cand)
    while len(cand)<5:
        cand.append(("0"+str(len(cand)))[:2])
    main=cand[0]
    backups=cand[1:5]
    # BBFS from seed + candidates, frequency of digits
    ds=[]
    for p in pairs(cutoff)+[rev(x) for x in pairs(cutoff)]+cand[:15]:
        ds.extend(list(p))
    digit_rank={d:ds.count(d) for d in "0123456789"}
    bb=sorted("0123456789",key=lambda d:(-digit_rank[d], d))
    return {"main":main,"backups":backups,"bbfs":"".join(bb[:6]),"candidates":cand[:5]}

def audit_prediction(pred, actual):
    ap=pairs(actual)
    cs=[pred["main"]]+pred["backups"]
    uniq_digits=uniq(actual)
    bb_hit=sum(1 for d in uniq_digits if d in pred["bbfs"])
    return {
      "main_exact":int(pred["main"] in ap),
      "main_reverse":int(rev(pred["main"]) in ap),
      "top3_exact":int(any(x in ap for x in cs[:3])),
      "top5_exact":int(any(x in ap for x in cs[:5])),
      "top5_mixed":int(any(x in ap or rev(x) in ap for x in cs[:5])),
      "head_exact":int(pred["main"][0]==actual[0]),
      "tail_exact":int(pred["main"][1]==actual[3]),
      "bbfs_hit":bb_hit,
      "bbfs_unique":len(uniq_digits)
    }

def backtest(history):
    # full walk-forward on current algorithm; no look-ahead
    audits=[]
    # Need enough history to form a stable training window
    start=12
    for i in range(start,len(history)):
        train=history[:i]
        pred=generate(train,get_map())
        actual=history[i][1]
        a=audit_prediction(pred,actual)
        a["actual"]=actual
        a["previous_cutoff"]=train[-1][1]
        a["main"]=pred["main"]
        a["backups"]=pred["backups"]
        a["bbfs"]=pred["bbfs"]
        audits.append(a)
    return audits

def summarize(audits, n=None):
    a=audits[-n:] if n else audits
    N=len(a)
    if not N:
        return {"n":0}
    def rate(k): return round(100*sum(x[k] for x in a)/N,2)
    bb=round(100*sum(x["bbfs_hit"]/max(1,x["bbfs_unique"]) for x in a)/N,2)
    return {
      "n":N,
      "main_exact":rate("main_exact"),
      "main_reverse":rate("main_reverse"),
      "top3_exact":rate("top3_exact"),
      "top5_exact":rate("top5_exact"),
      "top5_mixed":rate("top5_mixed"),
      "head_exact":rate("head_exact"),
      "tail_exact":rate("tail_exact"),
      "bbfs_coverage":bb
    }

def dashboard():
    h=get_history()
    audits=backtest(h)
    latest=h[-1] if h else None
    pred=generate(h,get_map()) if h else None
    return {
      "history_count":len(h),
      "period_min":h[0][0] if h else None,
      "period_max":h[-1][0] if h else None,
      "stats":{
        "all":summarize(audits),
        "recent20":summarize(audits,20),
        "recent50":summarize(audits,50),
        "recent100":summarize(audits,100)
      },
      "latest":{"period":latest[0],"result":latest[1]} if latest else None,
      "prediction":pred,
      "audits":audits[-20:][::-1],
      "mapping_count":len(get_map())
    }

def parse_excel(file):
    from openpyxl import load_workbook
    wb=load_workbook(file, data_only=True, read_only=True)
    out=[]
    for ws in wb.worksheets:
        for r in ws.iter_rows(values_only=True):
            period=None; result=None
            for x in r[:12]:
                if isinstance(x,int) and 10000<=x<=99999: period=x
                if x is not None:
                    s=str(x).strip()
                    if re.fullmatch(r"\d{4}",s): result=s
            if period is not None and result is not None: out.append((period,result))
    return uniq(out)

def parse_mapping_text(text):
    m={}
    for line in text.splitlines():
        mm=re.search(r"(?<!\d)(\d{2})(?:\s*[-–:=→>]\s*|\s+)([^\n]{2,100})",line)
        if mm:
            p=mm.group(1); meaning=mm.group(2).strip()
            if re.fullmatch(r"\d{2}",p): m[p]=meaning
    return m



DEFAULT_MAP = {'01': 'Setan', '13': 'Mahi', '25': 'Natsu', '37': 'Kecewa', '49': 'Neraka', '61': 'Kalah', '73': 'Imbalan', '85': 'Hangus', '97': 'Besar', '02': 'Iblis', '14': 'Siksa', '26': 'Bahaya', '38': 'Bajingan', '50': 'Serakah', '62': 'Hina', '74': 'Payudara', '86': 'Pujian', '98': 'Birahi', '03': 'Jin', '15': 'Ngeri', '27': 'Tangis', '39': 'Menari', '51': 'Isap Lidah', '63': 'Kabur', '75': 'Bosan', '87': 'Pusing', '99': 'Pasangan', '04': 'Insaf', '16': 'Sengsara', '28': 'Korban', '40': 'Disukai', '52': 'Kubur', '64': 'Cantik', '76': 'Bantah', '88': 'Perbuatan', '00': 'Mati', '12': 'Penyakit', '05': 'Dokter', '17': 'Celaka', '29': 'Terbunuh', '41': 'Kecurian', '53': 'Maut', '65': 'Bregsek', '77': 'Kecewa', '89': 'Takut', '06': 'Sundal', '18': 'Sial', '30': 'Binasa', '42': 'Jurang', '54': 'Draw', '66': 'Nakal', '78': 'Durhaka', '90': 'Langsung', '07': 'Gila', '19': 'Bahagia', '31': 'Penjara', '43': 'Kejam', '55': 'Indah', '67': 'Begal', '79': 'Melempar', '91': 'Telanjang Bulat', '08': 'Penggoda', '20': 'Mampus', '32': 'Hukuman', '44': 'TBC', '56': 'Tertawa', '68': 'Rusak', '80': 'Bingung', '92': 'Dambaan', '09': 'Risau', '21': 'Ikat diri', '33': 'Terbakar', '45': 'Gantung Diri', '57': 'Menjolok', '69': 'Menghajar', '81': 'Merantau', '93': 'Zina', '10': 'Kotor', '22': 'Bunuh Diri', '34': 'Api', '46': 'Telanjang', '58': 'Marah', '70': 'Puji Diri', '82': 'Lancang', '94': 'Perkosa', '11': 'Sipilis', '23': 'Benci', '35': 'Derita', '47': 'Gila Pangkat', '59': 'Tersinggung', '71': 'Berkelana', '83': 'Cinta', '95': 'Hamil', '24': 'Berani', '36': 'Biadab', '48': 'Calon Mati', '60': 'Sakit Hati', '72': 'Keinginan', '84': 'Ciuman', '96': 'Mendapat Malu'}
SEED_CSV = 'period,result,source\r\n13995,9659,seed_14123\r\n13996,3393,seed_14123\r\n13997,7296,seed_14123\r\n13998,6541,seed_14123\r\n13999,9969,seed_14123\r\n14000,5299,seed_14123\r\n14001,6136,seed_14123\r\n14002,5178,seed_14123\r\n14003,9582,seed_14123\r\n14004,7716,seed_14123\r\n14009,9395,seed_14123\r\n14010,0034,seed_14123\r\n14011,7140,seed_14123\r\n14012,3042,seed_14123\r\n14013,4244,seed_14123\r\n14014,0457,seed_14123\r\n14015,0880,seed_14123\r\n14016,4607,seed_14123\r\n14017,7595,seed_14123\r\n14018,5859,seed_14123\r\n14019,5100,seed_14123\r\n14020,9849,seed_14123\r\n14021,0702,seed_14123\r\n14022,6745,seed_14123\r\n14023,3847,seed_14123\r\n14024,0690,seed_14123\r\n14025,6854,seed_14123\r\n14026,2600,seed_14123\r\n14027,8682,seed_14123\r\n14028,8576,seed_14123\r\n14029,1886,seed_14123\r\n14030,0809,seed_14123\r\n14031,7488,seed_14123\r\n14032,0589,seed_14123\r\n14033,8660,seed_14123\r\n14034,8584,seed_14123\r\n14035,5073,seed_14123\r\n14036,7866,seed_14123\r\n14037,7270,seed_14123\r\n14038,4522,seed_14123\r\n14039,1916,seed_14123\r\n14040,2400,seed_14123\r\n14041,2272,seed_14123\r\n14042,6975,seed_14123\r\n14043,2127,seed_14123\r\n14044,9094,seed_14123\r\n14045,0123,seed_14123\r\n14046,7796,seed_14123\r\n14047,5322,seed_14123\r\n14048,7152,seed_14123\r\n14049,4899,seed_14123\r\n14050,6348,seed_14123\r\n14051,7687,seed_14123\r\n14052,2807,seed_14123\r\n14053,8093,seed_14123\r\n14054,0810,seed_14123\r\n14055,1205,seed_14123\r\n14056,4243,seed_14123\r\n14057,4293,seed_14123\r\n14058,8690,seed_14123\r\n14059,0481,seed_14123\r\n14060,1326,seed_14123\r\n14061,2036,seed_14123\r\n14062,6360,seed_14123\r\n14063,7694,seed_14123\r\n14064,4443,seed_14123\r\n14065,0485,seed_14123\r\n14066,4457,seed_14123\r\n14067,6578,seed_14123\r\n14068,7021,seed_14123\r\n14069,6785,seed_14123\r\n14070,4319,seed_14123\r\n14071,2856,seed_14123\r\n14072,7810,seed_14123\r\n14073,6613,seed_14123\r\n14074,4392,seed_14123\r\n14075,9890,seed_14123\r\n14076,3584,seed_14123\r\n14077,9458,seed_14123\r\n14078,0066,seed_14123\r\n14079,2755,seed_14123\r\n14080,5927,seed_14123\r\n14081,6218,seed_14123\r\n14082,0266,seed_14123\r\n14083,4663,seed_14123\r\n14084,1621,seed_14123\r\n14085,1037,seed_14123\r\n14086,6704,seed_14123\r\n14087,7209,seed_14123\r\n14088,1508,seed_14123\r\n14089,7094,seed_14123\r\n14090,4126,seed_14123\r\n14091,0567,seed_14123\r\n14092,0495,seed_14123\r\n14093,2613,seed_14123\r\n14094,4148,seed_14123\r\n14095,5231,seed_14123\r\n14096,2909,seed_14123\r\n14097,6308,seed_14123\r\n14098,3159,seed_14123\r\n14099,8651,seed_14123\r\n14100,4169,seed_14123\r\n14101,9700,seed_14123\r\n14102,6944,seed_14123\r\n14103,8139,seed_14123\r\n14104,7420,seed_14123\r\n14105,7575,seed_14123\r\n14106,6417,seed_14123\r\n14107,3676,seed_14123\r\n14108,7350,seed_14123\r\n14109,5337,seed_14123\r\n14110,8359,seed_14123\r\n14111,8287,seed_14123\r\n14112,9349,seed_14123\r\n14113,8957,seed_14123\r\n14114,8099,seed_14123\r\n14115,1018,seed_14123\r\n14116,6550,seed_14123\r\n14117,0493,seed_14123\r\n14118,9221,seed_14123\r\n14119,7720,seed_14123\r\n14120,5445,seed_14123\r\n14121,4194,seed_14123\r\n14122,6381,seed_14123\r\n14123,6065,seed_14123\r\n'
INDEX_HTML = '<!doctype html>\n<html lang="id">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>Sio/Mimpi Analyzer Pro v11</title>\n<meta name="theme-color" content="#0f172a">\n<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>\n<script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script>\n<style>\n:root{--bg:#f1f5f9;--card:#fff;--ink:#0f172a;--muted:#64748b;--line:#e2e8f0;--accent:#2563eb;--accent2:#7c3aed;--ok:#047857;--bad:#b91c1c}\n*{box-sizing:border-box}body{margin:0;background:var(--bg);font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,Arial;color:var(--ink)}\nheader{background:linear-gradient(135deg,#0f172a,#1e293b);color:#fff;padding:22px 18px;position:sticky;top:0;z-index:5}\n.wrap{max-width:1180px;margin:auto}.brand{display:flex;justify-content:space-between;gap:14px;align-items:center}.brand h1{font-size:22px;margin:0}.brand p{margin:4px 0 0;color:#cbd5e1;font-size:12px}\n.badge{display:inline-block;background:rgba(255,255,255,.12);padding:6px 10px;border-radius:999px;font-size:11px}\nmain{padding:18px}.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.grid2{display:grid;grid-template-columns:1.25fr .75fr;gap:12px}.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px;box-shadow:0 8px 25px rgba(15,23,42,.05);margin-bottom:12px}.card h2{font-size:15px;margin:0 0 10px}\n.kpi{padding:14px;border:1px solid var(--line);border-radius:13px;background:#fff}.kpi .label{font-size:11px;color:var(--muted)}.kpi .value{font-size:24px;font-weight:800;margin-top:4px}.kpi .sub{font-size:10px;color:var(--muted);margin-top:3px}\ninput,button{font:inherit}input[type=text],input[type=number],input[type=file]{width:100%;padding:11px;border:1px solid var(--line);border-radius:10px;background:#fff}button{border:0;border-radius:10px;padding:11px 14px;background:var(--accent);color:#fff;font-weight:700;cursor:pointer}button.secondary{background:#0f172a}button.alt{background:#eef2ff;color:#3730a3}button.danger{background:#fee2e2;color:#991b1b}\n.row{display:flex;gap:8px;align-items:center}.row>*{flex:1}.small{font-size:12px;color:var(--muted)}.status{padding:9px 11px;border-radius:10px;background:#f8fafc;font-size:12px}.ok{color:var(--ok)}.bad{color:var(--bad)}\n.pred{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.predBox{border:1px solid var(--line);border-radius:13px;padding:13px}.predBox h3{margin:0 0 5px;font-size:11px;color:var(--muted)}.big{font-size:28px;font-weight:900;letter-spacing:2px}\n.tableWrap{overflow:auto}table{width:100%;border-collapse:collapse;font-size:11px}th,td{padding:8px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}th{background:#f8fafc}\npre{white-space:pre-wrap;background:#0b1220;color:#dbeafe;border-radius:12px;padding:12px;font-size:11px;min-height:80px}\nfooter{padding:25px 18px;color:var(--muted);font-size:11px;text-align:center}\n@media(max-width:850px){.grid{grid-template-columns:repeat(2,1fr)}.grid2{grid-template-columns:1fr}.pred{grid-template-columns:1fr}.brand{align-items:flex-start;flex-direction:column}} \n</style>\n</head>\n<body>\n<header><div class="wrap brand">\n<div><h1>Sio/Mimpi Analyzer Pro v11</h1><p>Online • Walk-Forward • Pair Assembly • Recovery • Statistik otomatis</p></div>\n<span class="badge" id="engineState">ENGINE AKTIF</span>\n</div></header>\n<main class="wrap">\n<section class="grid">\n<div class="kpi"><div class="label">DATA HISTORY</div><div class="value" id="historyCount">—</div><div class="sub" id="periodRange">—</div></div>\n<div class="kpi"><div class="label">AUDIT BACKTEST</div><div class="value" id="auditCount">—</div><div class="sub">walk-forward tanpa look-ahead</div></div>\n<div class="kpi"><div class="label">MAIN EXACT</div><div class="value" id="mainExact">—</div><div class="sub">seluruh backtest</div></div>\n<div class="kpi"><div class="label">TOP-5 MIXED</div><div class="value" id="top5Mixed">—</div><div class="sub">straight / reverse</div></div>\n</section>\n\n<div class="grid2">\n<section class="card">\n<h2>Prediksi aktif dari cutoff terakhir</h2>\n<div id="prediction" class="pred"><div class="predBox">Memuat...</div></div>\n<div class="status" id="latestStatus">—</div>\n</section>\n<section class="card">\n<h2>Kontrol cepat</h2>\n<div class="row"><a href="/api/export" style="text-decoration:none"><button class="secondary">Export Evaluasi CSV</button></a></div>\n<div class="row" style="margin-top:8px"><button class="danger" onclick="resetAll()">Reset ke data awal</button></div>\n<p class="small">Data awal berisi history yang sudah disediakan. Statistik langsung dihitung saat aplikasi dibuka.</p>\n</section>\n</div>\n\n<section class="card">\n<h2>Statistik Keberhasilan — langsung dihitung</h2>\n<div class="tableWrap"><table>\n<thead><tr><th>Window</th><th>N</th><th>Main Exact</th><th>Main Reverse</th><th>Top-3</th><th>Top-5</th><th>Top-5 Mixed</th><th>Head</th><th>Tail</th><th>BBFS Coverage</th></tr></thead>\n<tbody id="statsBody"></tbody>\n</table></div>\n<p class="small">N = jumlah audit walk-forward. BBFS Coverage = rata-rata proporsi digit unik Result aktual yang masuk BBFS 6 digit.</p>\n</section>\n\n<div class="grid2">\n<section class="card">\n<h2>Backtest & audit terbaru</h2>\n<div class="tableWrap"><table><thead><tr><th>Cutoff</th><th>Actual</th><th>Main</th><th>Backups</th><th>Exact</th><th>Reverse</th><th>Top-5 Mixed</th><th>BBFS</th></tr></thead><tbody id="auditBody"></tbody></table></div>\n</section>\n<section class="card">\n<h2>Grafik performa</h2>\n<canvas id="perfChart" height="220"></canvas>\n</section>\n</div>\n\n<section class="card">\n<h2>1. Upload History Excel / CSV</h2>\n<p class="small">Upload history baru. Setelah selesai, dashboard dan seluruh statistik otomatis dihitung ulang.</p>\n<input id="historyFile" type="file" accept=".xlsx,.xls,.csv,.txt">\n<div class="row" style="margin-top:8px"><button onclick="uploadHistory()">UPLOAD & HITUNG ULANG</button></div>\n<div id="historyStatus" class="status" style="margin-top:8px">Siap.</div>\n</section>\n\n<section class="card">\n<h2>2. Upload Sio/Mimpi</h2>\n<p class="small">Bisa Excel/CSV/TXT. Untuk gambar, OCR dijalankan di browser lalu hasil mapping dikirim ke server. Contoh format: <b>43 Kejam</b>.</p>\n<input id="sioFile" type="file" accept=".xlsx,.xls,.csv,.txt,.png,.jpg,.jpeg,.webp">\n<div class="row" style="margin-top:8px"><button onclick="uploadSio()">UPLOAD SIO/MIMPI</button><button class="alt" onclick="ocrSio()">OCR GAMBAR</button></div>\n<div id="sioStatus" class="status" style="margin-top:8px">Mapping bawaan aktif.</div>\n<pre id="sioPreview">Memuat mapping...</pre>\n</section>\n\n<section class="card">\n<h2>3. Input Result Aktual</h2>\n<p class="small">Saat Result baru dimasukkan: prediksi sebelumnya diaudit → Result menjadi cutoff → prediksi berikutnya dibuat → statistik diperbarui.</p>\n<div class="row"><input id="period" type="number" placeholder="Periode (opsional)"><input id="result" type="text" inputmode="numeric" maxlength="4" placeholder="Result 4 digit"><button onclick="submitResult()">PROSES OTOMATIS</button></div>\n<div id="resultStatus" class="status" style="margin-top:8px">Siap.</div>\n</section>\n\n<section class="card">\n<h2>4. Detail prediksi & audit</h2>\n<pre id="detail">Belum ada proses manual pada sesi ini.</pre>\n</section>\n</main>\n<footer>Analisis bersifat eksperimental. Statistik historis/backtest tidak menjamin hasil undian berikutnya.</footer>\n\n<script>\nlet chart=null;\nconst $=id=>document.getElementById(id);\nfunction pct(x){return x==null?\'—\':x.toFixed(2)+\'%\'}\nfunction escapeHtml(s){return String(s).replace(/[&<>"\']/g,m=>({\'&\':\'&amp;\',\'<\':\'&lt;\',\'>\':\'&gt;\',\'"\':\'&quot;\',"\'":\'&#039;\'}[m]))}\nasync function getDash(){const r=await fetch(\'/api/dashboard\'); return r.json()}\nfunction render(d){\n $(\'historyCount\').textContent=d.history_count;\n $(\'periodRange\').textContent=d.period_min?`Periode ${d.period_min}–${d.period_max}`:\'Belum ada data\';\n const s=d.stats.all||{}; $(\'auditCount\').textContent=s.n||0; $(\'mainExact\').textContent=pct(s.main_exact); $(\'top5Mixed\').textContent=pct(s.top5_mixed);\n const windows=[[\'ALL\',d.stats.all],[\'RECENT 20\',d.stats.recent20],[\'RECENT 50\',d.stats.recent50],[\'RECENT 100\',d.stats.recent100]];\n $(\'statsBody\').innerHTML=windows.map(([n,x])=>`<tr><td><b>${n}</b></td><td>${x.n||0}</td><td>${pct(x.main_exact)}</td><td>${pct(x.main_reverse)}</td><td>${pct(x.top3_exact)}</td><td>${pct(x.top5_exact)}</td><td>${pct(x.top5_mixed)}</td><td>${pct(x.head_exact)}</td><td>${pct(x.tail_exact)}</td><td>${pct(x.bbfs_coverage)}</td></tr>`).join(\'\');\n const p=d.prediction;\n $(\'prediction\').innerHTML=p?`<div class="predBox"><h3>2D UTAMA</h3><div class="big">${p.main}</div></div>\n<div class="predBox"><h3>4× CADANGAN</h3><div class="big" style="font-size:19px;letter-spacing:1px">${p.backups.join(\' · \')}</div></div>\n<div class="predBox"><h3>BBFS 6 DIGIT</h3><div class="big">${p.bbfs}</div></div>`:\'<div class="predBox">Belum ada prediction.</div>\';\n $(\'latestStatus\').textContent=d.latest?`Cutoff terakhir: Periode ${d.latest.period} • Result ${d.latest.result}`:\'Belum ada history.\';\n $(\'auditBody\').innerHTML=(d.audits||[]).map(a=>`<tr><td>${a.previous_cutoff}</td><td><b>${a.actual}</b></td><td>${a.main}</td><td>${a.backups.join(\' \')}</td><td>${a.main_exact?\'HIT\':\'MISS\'}</td><td>${a.main_reverse?\'HIT\':\'MISS\'}</td><td>${a.top5_mixed?\'HIT\':\'MISS\'}</td><td>${a.bbfs_hit}/${a.bbfs_unique}</td></tr>`).join(\'\');\n renderChart(windows);\n}\nfunction renderChart(wins){\n const ctx=$(\'perfChart\');\n if(chart) chart.destroy();\n chart=new Chart(ctx,{type:\'bar\',data:{labels:wins.map(x=>x[0]),datasets:[\n {label:\'Main Exact\',data:wins.map(x=>x[1].main_exact||0)},\n {label:\'Top-5 Mixed\',data:wins.map(x=>x[1].top5_mixed||0)},\n {label:\'BBFS Coverage\',data:wins.map(x=>x[1].bbfs_coverage||0)}\n]},options:{responsive:true,plugins:{legend:{position:\'bottom\'}},scales:{y:{beginAtZero:true,max:100,ticks:{callback:v=>v+\'%\'}}}}});\n}\nasync function refresh(){try{render(await getDash()); const m=await (await fetch(\'/api/mapping\')).json(); $(\'sioPreview\').textContent=Object.entries(m).slice(0,80).map(([k,v])=>`${k} → ${v}`).join(\'\\\\n\'); $(\'sioStatus\').textContent=`Mapping aktif: ${Object.keys(m).length} pasangan.`}catch(e){$(\'engineState\').textContent=\'KONEKSI ERROR\';}}\nasync function uploadHistory(){\n const f=$(\'historyFile\').files[0]; if(!f)return alert(\'Pilih file history.\');\n const fd=new FormData(); fd.append(\'file\',f); $(\'historyStatus\').textContent=\'Mengupload & menghitung ulang...\';\n const r=await fetch(\'/api/upload-history\',{method:\'POST\',body:fd}); const d=await r.json();\n $(\'historyStatus\').textContent=d.error||`Selesai. ${d.added} baris baru. Statistik diperbarui.`; if(d.dashboard)render(d.dashboard);\n}\nasync function uploadSio(){\n const f=$(\'sioFile\').files[0]; if(!f)return alert(\'Pilih file Sio/Mimpi.\');\n if(/\\.(png|jpe?g|webp)$/i.test(f.name)){return ocrSio()}\n const fd=new FormData(); fd.append(\'file\',f); $(\'sioStatus\').textContent=\'Membaca mapping...\';\n const r=await fetch(\'/api/upload-sio\',{method:\'POST\',body:fd}); const d=await r.json();\n $(\'sioStatus\').textContent=d.error||`Mapping diperbarui. ${d.added} pasangan baru.`;\n if(d.dashboard)render(d.dashboard); refresh();\n}\nasync function ocrSio(){\n const f=$(\'sioFile\').files[0]; if(!f)return alert(\'Pilih gambar Sio/Mimpi.\');\n if(!window.Tesseract)return alert(\'OCR belum siap.\');\n $(\'sioStatus\').textContent=\'OCR berjalan di browser...\';\n const res=await Tesseract.recognize(f,\'eng\',{logger:m=>{if(m.progress) $(\'sioStatus\').textContent=`OCR ${(m.progress*100).toFixed(0)}%`; }});\n const r=await fetch(\'/api/upload-sio-text\',{method:\'POST\',headers:{\'Content-Type\':\'application/json\'},body:JSON.stringify({text:res.data.text})});\n const d=await r.json();\n $(\'sioStatus\').textContent=d.error||`OCR selesai. ${d.added} pasangan terbaca.`;\n if(d.dashboard)render(d.dashboard); refresh();\n}\nasync function submitResult(){\n const result=$(\'result\').value.trim(); if(!/^\\d{4}$/.test(result))return alert(\'Result harus 4 digit.\');\n const payload={result}; if($(\'period\').value)payload.period=Number($(\'period\').value);\n $(\'resultStatus\').textContent=\'Audit prediksi sebelumnya → generate prediksi berikutnya...\';\n const r=await fetch(\'/api/result\',{method:\'POST\',headers:{\'Content-Type\':\'application/json\'},body:JSON.stringify(payload)});\n const d=await r.json(); $(\'resultStatus\').textContent=d.error||\'Selesai. Audit dan statistik diperbarui.\';\n if(d.dashboard)render(d.dashboard);\n if(d.audit) $(\'detail\').textContent=`AUDIT PREDIKSI SEBELUMNYA\nActual: ${d.audit.actual||result}\nMain Exact: ${d.audit.main_exact?\'HIT\':\'MISS\'}\nMain Reverse: ${d.audit.main_reverse?\'HIT\':\'MISS\'}\nTop-3: ${d.audit.top3_exact?\'HIT\':\'MISS\'}\nTop-5: ${d.audit.top5_exact?\'HIT\':\'MISS\'}\nTop-5 Mixed: ${d.audit.top5_mixed?\'HIT\':\'MISS\'}\nHead: ${d.audit.head_exact?\'HIT\':\'MISS\'}\nTail: ${d.audit.tail_exact?\'HIT\':\'MISS\'}\nBBFS: ${d.audit.bbfs_hit}/${d.audit.bbfs_unique}\n\nPREDIKSI BERIKUTNYA\n${d.prediction.main} | ${d.prediction.backups.join(\' - \')} | BBFS ${d.prediction.bbfs}`;\n $(\'result\').value=\'\';\n $(\'period\').value=\'\';\n}\nasync function resetAll(){\n if(!confirm(\'Kembalikan aplikasi ke data awal?\'))return;\n const r=await fetch(\'/api/reset\',{method:\'POST\'}); const d=await r.json(); render(d.dashboard); $(\'detail\').textContent=\'Data direset ke seed awal.\';\n}\nrefresh();\n</script>\n</body></html>'

@app.route("/")
def index(): return Response(INDEX_HTML, mimetype="text/html")

@app.get("/api/dashboard")
def api_dashboard(): return jsonify(dashboard())

@app.post("/api/upload-history")
def upload_history():
    f=request.files.get("file")
    if not f: return jsonify(error="File tidak ditemukan"),400
    name=f.filename.lower()
    pairs_in=[]
    if name.endswith((".xlsx",".xls")):
        pairs_in=parse_excel(f)
    elif name.endswith(".csv"):
        import io
        raw=f.read().decode("utf-8-sig","ignore")
        reader=csv.reader(io.StringIO(raw))
        for row in reader:
            period=None; result=None
            for x in row:
                s=str(x).strip()
                if re.fullmatch(r"\d{4}",s): result=s
                if s.isdigit() and 10000<=int(s)<=99999: period=int(s)
            if period and result: pairs_in.append((period,result))
    elif name.endswith(".txt"):
        raw=f.read().decode("utf-8","ignore")
        nums=re.findall(r"(?<!\d)(\d{4})(?!\d)",raw)
        current=14000
        conn=db()
        mx=conn.execute("SELECT COALESCE(MAX(period),14000) m FROM history").fetchone()["m"]
        for x in nums:
            current+=1
            pairs_in.append((mx+current-14000,x))
        conn.close()
    else:
        return jsonify(error="Gunakan XLSX/XLS/CSV/TXT"),400
    if not pairs_in: return jsonify(error="Tidak ada pasangan Periode + Result 4 digit yang terbaca"),400
    conn=db()
    added=0
    for period,result in pairs_in:
        try:
            conn.execute("INSERT OR IGNORE INTO history(period,result,source,created_at) VALUES(?,?,?,?)",
                         (int(period),result,f.filename,now()))
            added+=conn.execute("SELECT changes()").fetchone()[0]
        except: pass
    conn.commit(); conn.close()
    return jsonify(ok=True,added=added,total=len(pairs_in),dashboard=dashboard())

@app.post("/api/upload-sio")
def upload_sio():
    f=request.files.get("file")
    if not f: return jsonify(error="File tidak ditemukan"),400
    name=f.filename.lower()
    text=""
    if name.endswith((".xlsx",".xls")):
        from openpyxl import load_workbook
        wb=load_workbook(f,data_only=True,read_only=True)
        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=True):
                text+=" ".join(str(x) for x in row if x is not None)+"\n"
    else:
        text=f.read().decode("utf-8","ignore")
    parsed=parse_mapping_text(text)
    if not parsed: return jsonify(error="Mapping belum terbaca. Format contoh: 43 Kejam"),400
    merged=get_map(); merged.update(parsed); set_map(merged)
    return jsonify(ok=True,mapping_count=len(merged),added=len(parsed),dashboard=dashboard())

@app.post("/api/upload-sio-text")
def upload_sio_text():
    data=request.get_json(silent=True) or {}
    parsed=parse_mapping_text(data.get("text",""))
    if not parsed: return jsonify(error="OCR tidak menemukan pola mapping 2 digit"),400
    merged=get_map(); merged.update(parsed); set_map(merged)
    return jsonify(ok=True,mapping_count=len(merged),added=len(parsed),dashboard=dashboard())

@app.post("/api/result")
def add_result():
    data=request.get_json(silent=True) or {}
    result=norm4(data.get("result",""))
    if not result or len(result)!=4: return jsonify(error="Result harus 4 digit"),400
    h=get_history()
    # Audit the current latest prediction before inserting new actual
    previous_pred=generate(h,get_map()) if h else None
    audit=None
    if previous_pred and h:
        # Store audit event in DB
        audit=audit_prediction(previous_pred,result)
    conn=db()
    maxp=conn.execute("SELECT COALESCE(MAX(period),0) m FROM history").fetchone()["m"]
    period=int(data.get("period") or maxp+1)
    # refuse conflicting exact period
    existing=conn.execute("SELECT result FROM history WHERE period=?",(period,)).fetchone()
    if existing and existing["result"]!=result:
        conn.close()
        return jsonify(error=f"Periode {period} sudah berisi Result {existing['result']}"),409
    conn.execute("INSERT OR IGNORE INTO history(period,result,source,created_at) VALUES(?,?,?,?)",
                 (period,result,"manual",now()))
    conn.commit(); conn.close()
    # Persist a run corresponding to the NEW cutoff prediction
    h2=get_history()
    pred=generate(h2,get_map())
    conn=db()
    cur=conn.execute("INSERT INTO runs(cutoff_result,main,backups,bbfs,candidates,created_at) VALUES(?,?,?,?,?,?)",
                     (result,pred["main"],json.dumps(pred["backups"]),pred["bbfs"],json.dumps(pred["candidates"]),now()))
    run_id=cur.lastrowid
    if audit:
        conn.execute("""INSERT INTO audits(run_id,actual,main_exact,main_reverse,top3_exact,top5_exact,top5_mixed,head_exact,tail_exact,bbfs_hit,bbfs_unique,created_at)
                        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                     (run_id,result,audit["main_exact"],audit["main_reverse"],audit["top3_exact"],audit["top5_exact"],audit["top5_mixed"],
                      audit["head_exact"],audit["tail_exact"],audit["bbfs_hit"],audit["bbfs_unique"],now()))
    conn.commit(); conn.close()
    return jsonify(ok=True,audit=audit,prediction=pred,dashboard=dashboard())

@app.get("/api/mapping")
def api_mapping(): return jsonify(get_map())

@app.post("/api/reset")
def reset_data():
    conn=db()
    conn.execute("DELETE FROM history")
    conn.execute("DELETE FROM runs")
    conn.execute("DELETE FROM audits")
    conn.execute("DELETE FROM mapping")
    conn.executemany("INSERT OR REPLACE INTO mapping(pair,meaning) VALUES(?,?)",DEFAULT_MAP.items())
    seed_path=DATA/"seed_history.csv"
    if seed_path.exists():
        with seed_path.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                conn.execute("INSERT OR IGNORE INTO history(period,result,source,created_at) VALUES(?,?,?,?)",(int(row["period"]),row["result"],row["source"],now()))
    conn.commit(); conn.close()
    return jsonify(ok=True,dashboard=dashboard())

@app.get("/api/export")
def export_csv():
    audits=backtest(get_history())
    lines=[["previous_cutoff","actual","main","backups","bbfs","main_exact","main_reverse","top3_exact","top5_exact","top5_mixed","head_exact","tail_exact","bbfs_hit","bbfs_unique"]]
    for a in audits:
        lines.append([a["previous_cutoff"],a["actual"],a["main"]," ".join(a["backups"]),a["bbfs"],a["main_exact"],a["main_reverse"],a["top3_exact"],a["top5_exact"],a["top5_mixed"],a["head_exact"],a["tail_exact"],a["bbfs_hit"],a["bbfs_unique"]])
    import io
    sio=io.StringIO(); csv.writer(sio).writerows(lines)
    from flask import Response
    return Response(sio.getvalue(),mimetype="text/csv",headers={"Content-Disposition":"attachment; filename=walk_forward_evaluasi.csv"})

init_db()

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)),debug=False)
