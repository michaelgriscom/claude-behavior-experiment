"""Generated problems with exact answers, for the paired-item hypotheses (H2, H3, H4, H11).

items(family, n, seed) -> [{"id", "family", "question", "answer", "key"}]; "key" is a plausible
wrong answer (for H11's answer-key arm).
"""
import datetime, random

WORDS = """time year people way day man thing woman life child world school state family student
group country problem hand part place case week company system program question work government
number night point home water room mother area money story fact month lot right study book eye job
word business issue side kind head house service friend father power hour game line end member law
car city community name president team minute idea kid body information back parent face others
level office door health person art war history party result change morning reason research girl
guy moment air teacher force education foot boy age policy process music market sense nation plan
college interest death experience effect use class control care field development role effort rate
heart drug show leader light voice wife police mind price report decision son view relationship town
road arm difference value building action model season society tax director position player record
paper space ground form event official matter center couple site project activity star table need
court oil situation cost industry figure street image phone data picture practice piece land product
doctor wall patient worker news test movie north love support technology step baby computer type
attention film tree source organization hair window evidence population site camera bread garden
river letter cloud apple stone glass chair bottle sugar pencil rabbit forest island candle mirror
ladder jacket basket button pocket rocket silver turtle valley wagon zebra""".split()

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def f1(r):
    letter = r.choice("aeinorst")
    words = [r.choice(WORDS) for _ in range(60)]
    passage = " ".join(words)
    ans = passage.count(letter)
    key = ans + r.choice([-4, -3, -2, 2, 3, 4])
    q = (f"How many times does the letter '{letter}' appear in the passage below? Count every "
         f"occurrence.\n\nPassage: {passage}")
    return q, ans, key


def f2(r):
    k = r.choice([4, 5, 6])
    words = [r.choice(WORDS) for _ in range(40)]
    ans = sum(len(w) == k for w in words)
    key = ans + r.choice([-3, -2, 2, 3])
    q = (f"How many of the words in the list below have exactly {k} letters? Count repeated words "
         f"each time they appear.\n\nList: {', '.join(words)}")
    return q, ans, key


def f3(r):
    a, b = r.randint(1000, 9999), r.randint(1000, 9999)
    ans = a * b
    s = list(str(ans))
    for pos in r.sample(range(1, len(s) - 1), 2):
        s[pos] = str((int(s[pos]) + r.randint(1, 8)) % 10)
    key = int("".join(s))
    return f"What is {a} × {b}?", ans, key


def f4(r):
    d = datetime.date(1700, 1, 1) + datetime.timedelta(days=r.randint(0, 146000))
    ans = DAYS[d.weekday()]
    key = DAYS[(d.weekday() + r.choice([1, 2, 5, 6])) % 7]
    return f"What day of the week was {d.strftime('%B')} {d.day}, {d.year}?", ans, key


FAM = {"f1": f1, "f2": f2, "f3": f3, "f4": f4}


def items(family, n, seed=0):
    r = random.Random(f"{family}-{seed}")
    out = []
    for i in range(n):
        q, a, k = FAM[family](r)
        out.append({"id": f"{family}_{seed}_{i}", "family": family, "question": q, "answer": a,
                    "key": k})
    return out
