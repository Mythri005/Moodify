from flask import Flask, render_template, request
import os
from deepface import DeepFace
from mood_model.mood_detector import detect_mood  # Adjust import based on your file path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Mood-to-song map (placed globally, outside route)
mood_map = {
    'happy': [
        ('Happy - Pharrell Williams', 'https://www.youtube.com/watch?v=ZbZSe6N_BXs'),
        ('Can’t Stop the Feeling - Justin Timberlake', 'https://www.youtube.com/watch?v=ru0K8uYEZWw'),
        ('Uptown Funk - Mark Ronson ft. Bruno Mars', 'https://www.youtube.com/watch?v=OPf0YbXqDm0'),
        ('Best Day of My Life - American Authors', 'https://www.youtube.com/watch?v=Y66j_BUCBMY'),
        ('Shut Up and Dance - Walk The Moon', 'https://www.youtube.com/watch?v=6JCLY0Rlx6Q'),
        ('I Gotta Feeling - Black Eyed Peas', 'https://www.youtube.com/watch?v=uSD4vsh1zDA'),
        ('Good Time - Owl City & Carly Rae Jepsen', 'https://www.youtube.com/watch?v=H7HmzwI67ec'),
        ('Firework - Katy Perry', 'https://www.youtube.com/watch?v=QGJuMBdaqIw'),
        ('Sugar - Maroon 5', 'https://www.youtube.com/watch?v=09R8_2nJtjg'),
        ('On Top of the World - Imagine Dragons', 'https://www.youtube.com/watch?v=w5tWYmIOWGk')
    ],
    'sad': [
        ('Someone Like You - Adele', 'https://www.youtube.com/watch?v=hLQl3WQQoQ0'),
        ('Let Her Go - Passenger', 'https://www.youtube.com/watch?v=RBumgq5yVrA'),
        ('Fix You - Coldplay', 'https://www.youtube.com/watch?v=k4V3Mo61fJM'),
        ('Stay With Me - Sam Smith', 'https://www.youtube.com/watch?v=pB-5XG-DbAA'),
        ('Skinny Love - Bon Iver', 'https://www.youtube.com/watch?v=ssdgFoHLwnk'),
        ('Say Something - A Great Big World & Christina Aguilera', 'https://www.youtube.com/watch?v=-2U0Ivkn2Ds'),
        ('All I Want - Kodaline', 'https://www.youtube.com/watch?v=mtf7hC17IBM'),
        ('I Will Always Love You - Whitney Houston', 'https://www.youtube.com/watch?v=3JWTaaS7LdU'),
        ('Jealous - Labrinth', 'https://www.youtube.com/watch?v=50VWOBi0VFs'),
        ('Tears Dry On Their Own - Amy Winehouse', 'https://www.youtube.com/watch?v=ojdbDYahiCQ')
    ],
    'angry': [
        ('Breaking the Habit - Linkin Park', 'https://www.youtube.com/watch?v=v2H4l9RpkwM'),
        ('Stronger - Kanye West', 'https://www.youtube.com/watch?v=PsO6ZnUZI0g'),
        ('Killing In The Name - Rage Against The Machine', 'https://www.youtube.com/watch?v=bWXazVhlyxQ'),
        ('Lose Yourself - Eminem', 'https://www.youtube.com/watch?v=_Yhyp-_hX2s'),
        ('Given Up - Linkin Park', 'https://www.youtube.com/watch?v=0xyxtzD54rM'),
        ('Smells Like Teen Spirit - Nirvana', 'https://www.youtube.com/watch?v=hTWKbfoikeg'),
        ('Before I Forget - Slipknot', 'https://www.youtube.com/watch?v=qw2LU1yS7aw'),
        ('Headstrong - Trapt', 'https://www.youtube.com/watch?v=HTvu1Yr3Ohk'),
        ('Bodies - Drowning Pool', 'https://www.youtube.com/watch?v=04F4xlWSFh0'),
        ('Duality - Slipknot', 'https://www.youtube.com/watch?v=6fVE8kSM43I')
    ],
    'calm': [
        ('Weightless - Marconi Union', 'https://www.youtube.com/watch?v=UfcAVejslrU'),
        ('Clair de Lune - Debussy', 'https://www.youtube.com/watch?v=CvFH_6DNRCY'),
        ('River Flows In You - Yiruma', 'https://www.youtube.com/watch?v=7maJOI3QMu0'),
        ('Pure Shores - All Saints', 'https://www.youtube.com/watch?v=HxUuDPNbkJk'),
        ('Holocene - Bon Iver', 'https://www.youtube.com/watch?v=TWcyIpul8OE'),
        ('Breathe Me - Sia', 'https://www.youtube.com/watch?v=wbP0c7f9Owg'),
        ('Sunset Lover - Petit Biscuit', 'https://www.youtube.com/watch?v=wke0RNvWvjc'),
        ('Ocean Eyes - Billie Eilish', 'https://www.youtube.com/watch?v=viimfQi_pUw'),
        ('Bloom - The Paper Kites', 'https://www.youtube.com/watch?v=8inJtTG_DuU'),
        ('Landslide - Fleetwood Mac', 'https://www.youtube.com/watch?v=WM7-PYtXtJM')
    ],
    'surprise': [
        ('Surprise Yourself - Jack Garratt', 'https://www.youtube.com/watch?v=6qZWMNW7GmE'),
        ('Shake It Off - Taylor Swift', 'https://www.youtube.com/watch?v=nfWlot6h_JM'),
        ('Don’t Stop Me Now - Queen', 'https://www.youtube.com/watch?v=HgzGwKwLmgM'),
        ('Feel It Still - Portugal. The Man', 'https://www.youtube.com/watch?v=pBkHHoOIIn8'),
        ('Electric Feel - MGMT', 'https://www.youtube.com/watch?v=MmZexg8sxyk'),
        ('Pompeii - Bastille', 'https://www.youtube.com/watch?v=F90Cw4l-8NY'),
        ('Take On Me - a-ha', 'https://www.youtube.com/watch?v=djV11Xbc914'),
        ('Viva La Vida - Coldplay', 'https://www.youtube.com/watch?v=dvgZkm1xWPE'),
        ('Good as Hell - Lizzo', 'https://www.youtube.com/watch?v=vuq-VAiW9kw'),
        ('Electric Love - BORNS', 'https://www.youtube.com/watch?v=RYr96YYEaZY')
    ],
    'fear': [
        ('Everybody Hurts - R.E.M.', 'https://www.youtube.com/watch?v=ijZRCIrTgQc'),
        ('Creep - Radiohead', 'https://www.youtube.com/watch?v=XFkzRNyygfk'),
        ('The Sound of Silence - Simon & Garfunkel', 'https://www.youtube.com/watch?v=4zLfCnGVeL4'),
        ('Boulevard of Broken Dreams - Green Day', 'https://www.youtube.com/watch?v=Soa3gO7tL-c'),
        ('Mad World - Gary Jules', 'https://www.youtube.com/watch?v=4N3N1MlvVc4'),
        ('Breathe Me - Sia', 'https://www.youtube.com/watch?v=wbP0c7f9Owg'),
        ('Chandelier - Sia', 'https://www.youtube.com/watch?v=2vjPBrBU-TM'),
        ('Demons - Imagine Dragons', 'https://www.youtube.com/watch?v=mWRsgZuwf_8'),
        ('In the End - Linkin Park', 'https://www.youtube.com/watch?v=eVTXPUF4Oz4'),
        ('Everybody’s Got to Learn Sometime - Beck', 'https://www.youtube.com/watch?v=90ZrMuR_EIY')
    ],
    'neutral': [
        ('Let Her Go - Passenger', 'https://www.youtube.com/watch?v=RBumgq5yVrA'),
        ('I’m Yours - Jason Mraz', 'https://www.youtube.com/watch?v=EkHTsc9PU2A'),
        ('Counting Stars - OneRepublic', 'https://www.youtube.com/watch?v=hT_nvWreIhg'),
        ('Budapest - George Ezra', 'https://www.youtube.com/watch?v=VHrLPs3_1Fs'),
        ('Banana Pancakes - Jack Johnson', 'https://www.youtube.com/watch?v=6Graa_Vm5eA'),
        ('Photograph - Ed Sheeran', 'https://www.youtube.com/watch?v=SPKBtZHuzKY'),
        ('Riptide - Vance Joy', 'https://www.youtube.com/watch?v=uJ_1HMAGb4k'),
        ('Ho Hey - The Lumineers', 'https://www.youtube.com/watch?v=zvCBSSwgtg4'),
        ('The A Team - Ed Sheeran', 'https://www.youtube.com/watch?v=UAWcs5H-qgQ'),
        ('Home - Edward Sharpe & The Magnetic Zeros', 'https://www.youtube.com/watch?v=DHEOF_rcND8')
    ],
    'disgust': [
        ('Boulevard of Broken Dreams - Green Day', 'https://www.youtube.com/watch?v=Soa3gO7tL-c'),
        ('Numb - Linkin Park', 'https://www.youtube.com/watch?v=kXYiU_JCYtU'),
        ('Animal I Have Become - Three Days Grace', 'https://www.youtube.com/watch?v=xqds0B_meys'),
        ('Zombie - The Cranberries', 'https://www.youtube.com/watch?v=6Ejga4kJUts'),
        ('Chop Suey! - System Of A Down', 'https://www.youtube.com/watch?v=CSvFpBOe8eY'),
        ('Toxicity - System Of A Down', 'https://www.youtube.com/watch?v=iywaBOMvYLI'),
        ('Faint - Linkin Park', 'https://www.youtube.com/watch?v=LYU-8IFcDPw'),
        ('Behind Blue Eyes - Limp Bizkit', 'https://www.youtube.com/watch?v=qsayW7cLdyA'),
        ('My Immortal - Evanescence', 'https://www.youtube.com/watch?v=5anLPw0Efmo'),
        ('I Hate Everything About You - Three Days Grace', 'https://www.youtube.com/watch?v=d8ekz_CSBVg')
    ]
}


@app.route("/", methods=["GET", "POST"])
def index():
    mood = None
    songs = []

    if request.method == 'POST':
        # Handle image upload
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                image.save(filepath)
                try:
                    # Using DeepFace for emotion analysis
                    analysis = DeepFace.analyze(img_path=filepath, actions=['emotion'], detector_backend='opencv')
                    mood = analysis[0]['dominant_emotion']
                except Exception as e:
                    print("Error in mood detection:", e)
                    mood = "neutral"  # fallback
        else:
            # Manual mood selection fallback
            mood = request.form.get('mood', 'neutral')

        # If mood is still None, you can use your custom detector
        if not mood:
            mood = detect_mood(filepath)  # Using your custom mood detector if no emotion is detected by DeepFace

        # Select songs based on mood
        mood_lower = mood.lower() if mood else 'neutral'
        songs = mood_map.get(mood_lower, mood_map['neutral'])

    return render_template("index.html", mood=mood, songs=songs)

if __name__ == '__main__':
    app.run(debug=False, port=5050)