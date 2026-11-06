"""Daily 'milk delivered' WhatsApp message in Tamil + a Thirukkural of the day.
No Streamlit here, so it can be tested on its own."""
import json
import random
import urllib.parse
import urllib.request
import urllib.error
from datetime import date

ORDER_NUMBER = "9489002466"   # extra-milk orders
ORDER_BEFORE = "மதியம் 12 மணிக்குள்"
ORDER_LATEST = "மதியம் 3 மணிக்குள்"

# (kural number, line 1, line 2)
KURALS = [
    (1, "அகர முதல எழுத்தெல்லாம் ஆதி", "பகவன் முதற்றே உலகு."),
    (2, "கற்றதனால் ஆய பயனென்கொல் வாலறிவன்", "நற்றாள் தொழாஅர் எனின்."),
    (3, "மலர்மிசை ஏகினான் மாணடி சேர்ந்தார்", "நிலமிசை நீடுவாழ் வார்."),
    (4, "வேண்டுதல் வேண்டாமை இலானடி சேர்ந்தார்க்கு", "யாண்டும் இடும்பை இல."),
    (11, "வான்நின்று உலகம் வழங்கி வருதலால்", "தான்அமிழ்தம் என்றுணரற் பாற்று."),
    (20, "நீரின்று அமையாது உலகெனின் யார்யார்க்கும்", "வானின்று அமையாது ஒழுக்கு."),
    (26, "செயற்கரிய செய்வார் பெரியர் சிறியர்", "செயற்கரிய செய்கலா தார்."),
    (34, "மனத்துக்கண் மாசிலன் ஆதல் அனைத்தறன்", "ஆகுல நீர பிற."),
    (39, "அறத்தான் வருவதே இன்பம் மற்றெல்லாம்", "புறத்த புகழும் இல."),
    (45, "அன்பும் அறனும் உடைத்தாயின் இல்வாழ்க்கை", "பண்பும் பயனும் அது."),
    (51, "மனைத்தக்க மாண்புடையள் ஆகித் தற்கொண்டான்", "வளத்தக்காள் வாழ்க்கைத் துணை."),
    (66, "குழல்இனிது யாழ்இனிது என்பதம் மக்கள்", "மழலைச்சொல் கேளா தவர்."),
    (67, "தந்தை மகற்காற்றும் நன்றி அவையத்து", "முந்தி இருப்பச் செயல்."),
    (72, "அன்பிலார் எல்லாம் தமக்குரியர் அன்புடையார்", "என்பும் உரியர் பிறர்க்கு."),
    (74, "அன்பீனும் ஆர்வமுடைமை அதுஈனும்", "நண்பென்னும் நாடாச் சிறப்பு."),
    (86, "செல்விருந்து ஓம்பி வருவிருந்து பார்த்திருப்பான்", "நல்வருந்து வானத் தவர்க்கு."),
    (91, "இன்சொலால் ஈரம் அளைஇப் படிறிலவாம்", "செம்பொருள் கண்டார்வாய்ச் சொல்."),
    (100, "இனிய உளவாக இன்னாத கூறல்", "கனிஇருப்பக் காய்கவர்ந் தற்று."),
    (101, "செய்யாமல் செய்த உதவிக்கு வையகமும்", "வானகமும் ஆற்றல் அரிது."),
    (108, "நன்றி மறப்பது நன்றன்று நன்றல்லது", "அன்றே மறப்பது நன்று."),
    (114, "தக்கார் தகவிலர் என்பது அவரவர்", "எச்சத்தால் காணப் படும்."),
    (129, "தீயினால் சுட்டபுண் உள்ளாறும் ஆறாதே", "நாவினால் சுட்ட வடு."),
    (131, "ஒழுக்கம் விழுப்பம் தரலான் ஒழுக்கம்", "உயிரினும் ஓம்பப் படும்."),
    (151, "அகழ்வாரைத் தாங்கும் நிலம்போலத் தம்மை", "இகழ்வார்ப் பொறுத்தல் தலை."),
    (156, "ஒறுத்தாற்கு ஒருநாளை இன்பம் பொறுத்தார்க்குப்", "பொன்றுந் துணையும் புகழ்."),
    (200, "சொல்லுக சொல்லில் பயனுடைய சொல்லற்க", "சொல்லில் பயனிலாச் சொல்."),
    (231, "ஈதல் இசைபட வாழ்தல் அதுவல்லது", "ஊதியம் இல்லை உயிர்க்கு."),
    (247, "அருளில்லார்க் கவ்வுலகம் இல்லை பொருளில்லார்க்", "கிவ்வுலகம் இல்லாகி யாங்கு."),
    (319, "பிறர்க்கின்னா முற்பகல் செய்யின் தமக்கின்னா", "பிற்பகல் தானே வரும்."),
    (391, "கற்க கசடறக் கற்பவை கற்றபின்", "நிற்க அதற்குத் தக."),
    (392, "எண்ணென்ப ஏனை எழுத்தென்ப இவ்விரண்டும்", "கண்ணென்ப வாழும் உயிர்க்கு."),
    (396, "தொட்டனைத் தூறும் மணற்கேணி மாந்தர்க்குக்", "கற்றனைத் தூறும் அறிவு."),
    (397, "யாதானும் நாடாமால் ஊராமால் என்னொருவன்", "சாந்துணையுங் கல்லாத வாறு."),
    (400, "கேடில் விழுச்செல்வம் கல்வியொருவற்கு", "மாடல்ல மற்றை யவை."),
    (596, "உள்ளுவ தெல்லாம் உயர்வுள்ளல் மற்றது", "தள்ளினுந் தள்ளாமை நீர்த்து."),
    (616, "முயற்சி திருவினை ஆக்கும் முயற்றின்மை", "இன்மை புகுத்தி விடும்."),
    (666, "எண்ணிய எண்ணியாங் கெய்துப எண்ணியார்", "திண்ணியராகப் பெறின்."),
    (788, "உடுக்கை இழந்தவன் கைபோல ஆங்கே", "இடுக்கண் களைவதாம் நட்பு."),
    (942, "மருந்தென வேண்டாவாம் யாக்கைக்கு அருந்தியது", "அற்றது போற்றி உணின்."),
    (949, "உற்றான் அளவும் பிணியளவும் காலமும்", "கற்றான் கருதிச் செயல்."),
    (1031, "சுழன்றும் ஏர்ப்பின்ன துலகம் அதனால்", "உழந்தும் உழவே தலை."),
]


def kural_of_day(day=None):
    """A random-looking kural per day. Everyone gets the same one on a given day, and
    no kural repeats until all have been used (shuffle is seeded by the year)."""
    day = day or date.today()
    order = list(range(len(KURALS)))
    random.Random(day.year).shuffle(order)
    return KURALS[order[(day.timetuple().tm_yday - 1) % len(order)]]


def kural_text(day=None):
    n, l1, l2 = kural_of_day(day)
    return f"{l1}\n{l2}\n(திருக்குறள் {n})"


def delivery_message(day=None):
    return (
        "🥛 வணக்கம்! இன்றைய பால் டெலிவரி செய்யப்பட்டது.\n"
        "பால் கிடைத்திருக்கும் என்று நம்புகிறோம். தயவுசெய்து பையில் இருந்து பாலை எடுத்துக் கொள்ளவும். 🙏\n\n"
        f"➕ கூடுதல் பால் தேவைப்பட்டால், தினமும் {ORDER_BEFORE} (அதிகபட்சம் {ORDER_LATEST}) "
        f"📞 {ORDER_NUMBER} என்ற எண்ணில் தெரிவிக்கவும். அதற்கேற்ப பால் டெலிவரி செய்யப்படும்.\n\n"
        f"📖 இன்றைய திருக்குறள்:\n{kural_text(day)}"
    )


def whatsapp_url(phone, message):
    return f"https://api.whatsapp.com/send?phone={phone}&text={urllib.parse.quote(message)}"


# ---------------- optional: real one-click sending via WhatsApp Cloud API ----------------
def cloud_send(token, phone_id, to, message, template=None, template_lang="ta", kural=None):
    """Send one message. With `template`, the approved template gets the kural as {{1}}
    (needed for business-initiated messages); otherwise plain text (only works inside the 24 h window)."""
    if template:
        body = {"messaging_product": "whatsapp", "to": to, "type": "template",
                "template": {"name": template, "language": {"code": template_lang},
                             "components": [{"type": "body", "parameters": [
                                 {"type": "text", "text": (kural or "").replace("\n", " / ")}]}]}}
    else:
        body = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": message}}
    req = urllib.request.Request(
        f"https://graph.facebook.com/v20.0/{phone_id}/messages",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return True, ""
    except urllib.error.HTTPError as e:
        try:
            return False, json.loads(e.read().decode())["error"]["message"]
        except Exception:
            return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)


# ---------------- free automatic sending with pywhatkit (controls WhatsApp Web on THIS computer) ----------------
PWK_WAIT_LOAD = 20          # seconds to let each WhatsApp Web chat load before pressing Enter
PWK_GAP = (15, 30)          # random pause (seconds) between customers - looks less like a bot


def pywhatkit_available():
    try:
        import pywhatkit  # noqa: F401
        import pyautogui  # noqa: F401
        return True
    except Exception:
        return False


def pywhatkit_send(phone91, message):
    """phone91 = '91XXXXXXXXXX'. Opens the chat in the browser, types the message and presses Enter."""
    import pywhatkit
    try:
        pywhatkit.sendwhatmsg_instantly("+" + phone91, message, wait_time=PWK_WAIT_LOAD,
                                        tab_close=True, close_time=3)
        return True, ""
    except Exception as e:
        return False, str(e)


def pywhatkit_pause():
    import time
    time.sleep(random.uniform(*PWK_GAP))
