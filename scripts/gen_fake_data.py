import random
import string

from app import db, models

# List of male, female, and gender neutral first names from multiple cultures
names = [
    "Ayden",
    "Aisha",
    "Akira",
    "Alonso",
    "Amina",
    "Anahi",
    "Anaya",
    "Angel",
    "Ari",
    "Aria",
    "Asa",
    "Avery",
    "Ayaan",
    "Bella",
    "Brayden",
    "Caleb",
    "Camila",
    "Carlos",
    "Chase",
    "Christian",
    "Claire",
    "Daniel",
    "Daphne",
    "Diego",
    "Eli",
    "Ella",
    "Elliot",
    "Eloise",
    "Emiliano",
    "Emma",
    "Esperanza",
    "Ethan",
    "Evelyn",
    "Finn",
    "Gabriel",
    "Gia",
    "Giovanni",
    "Grace",
    "Hazel",
    "Hudson",
    "Ingrid",
    "Isaac",
    "Isabella",
    "Ivan",
    "Jaden",
    "Jasmine",
    "Jasper",
    "Jayden",
    "Jocelyn",
    "Jorge",
    "Josiah",
    "Julia",
    "Kai",
    "Kian",
    "Kiera",
    "Koa",
    "Kyrie",
    "Landon",
    "Layla",
    "Leo",
    "Liliana",
    "Lola",
    "Lucas",
    "Luciana",
    "Luna",
    "Lydia",
    "Maddox",
    "Makayla",
    "Malakai",
    "Malia",
    "Marcelo",
    "Maria",
    "Mateo",
    "Maya",
    "Mia",
    "Miles",
    "Milena",
    "Nadia",
    "Nash",
    "Natalie",
    "Nathaniel",
    "Nia",
    "Nina",
    "Nora",
    "Oliver",
    "Oscar",
    "Paloma",
    "Penelope",
    "Rafael",
    "Rayaan",
    "Reyansh",
    "Riley",
    "River",
    "Robert",
    "Rosalie",
    "Ryder",
    "Santiago",
    "Sasha",
    "Sebastian",
    "Selena",
    "Sienna",
    "Sofia",
    "Solomon",
    "Sophia",
    "Stella",
    "Talia",
    "Theo",
    "Valeria",
    "Victoria",
    "Xavier",
    "Yahir",
    "Yara",
    "Zaid",
    "Zara",
    "Zion",
]

# Create list of tuples with name and email address
name_email_tuples = [(name, f"{name.lower()}@example.com") for name in names]

contents = [
    "Just had the best sandwich of my life! #foodie",
    "Can't believe I finished my first half marathon! #runner",
    "so excited to be heading to the beach for vacation ☀️🏖️",
    "Just got a promotion at work! Hard work pays off 💪",
    "Why does it take so long to get through airport security? 🤔 #travel",
    "Can't wait to see my favorite band in concert tonight! 🎶🤘",
    "sometimes I wonder if anyone is really listening...",
    "Trying out a new recipe tonight. Fingers crossed it's good! #chef",
    "so glad it's Friday! Time to relax and enjoy the weekend 🍹🌴",
    "Feeling grateful for my friends and family ❤️ #blessed",
    "Why do some people drive so slowly in the fast lane? 🚗💨 #roadrage",
    "Excited to start my new job next week! #career",
    "Does anyone else hate getting up early as much as I do? 😴 #notamorningperson",
    "Can't believe how quickly time is flying by! #timeflies",
    "Just finished reading an amazing book. Highly recommend! 📖",
    "Why do some people feel the need to talk during movies? 🤫 #annoying",
    "Feeling a bit under the weather today. Hope I'm not getting sick 🤒",
    "Can't believe it's already been a year since my wedding! #anniversary",
    "Finally finished that project I've been working on for months! #success",
    "Why is it so hard to find good help these days? 🤔 #frustrating",
    "so excited for the start of football season! Let's go team! 🏈🙌",
    "Just tried sushi for the first time. Surprisingly delicious! 🍣",
    "Why is it so hard to get motivated to exercise? 😩 #lazy",
    "Feeling overwhelmed with everything I have to do. #stressed",
    "Can't wait to see my favorite comedian perform tonight! 😂🤣",
    "Why do some people have to be so negative all the time? 🙄 #positivity",
    "Feeling inspired after attending a great conference this weekend! #motivated",
    "Just finished a tough workout. Feeling great! 💪🏋️‍♀️",
    "Why is it so hard to make new friends as an adult? 😕 #lonely",
    "So excited for pumpkin spice latte season! 🎃☕️",
    "Just saw the most beautiful sunset. Nature is amazing 🌅",
    "Why is it so hard to find a good work-life balance? 🤔 #workaholic",
    "Feeling proud of myself for stepping out of my comfort zone today. #courage",
    "Can't believe how fast my kids are growing up! #parenting",
    "Finally got around to cleaning out my closet. Feels good to declutter! #minimalism",
    "Why does it always rain on the weekends? ☔️ #badluck",
    "Excited to try out the new restaurant that just opened up in town! #foodie",
    "Just got back from an amazing vacation. Wish I could stay there forever! 🌴☀️",
    "Why do some people feel the need to constantly one up each other ¯\_ (ツ)_/¯",
    "Just finished a great workout!",
    "I'm so excited for the weekend",
    "Feeling productive today",
    "Can't wait to see my friends tonight",
    "This book is amazing, highly recommend",
    "Love this new restaurant I discovered",
    "Had a long day, time to relax",
    "I'm finally starting to get the hang of this",
    "Feeling inspired by the people around me",
    "New year, new opportunities",
    "Never stop learning",
    "Happiness is a choice, make it every day",
    "Small steps can lead to big changes",
    "Grateful for my friends and family",
    "Trying to stay positive, even on tough days",
    "Excited for what's to come",
]


# Define a function to generate random titles
def generate_title():
    words = [
        "Lorem",
        "Ipsum",
        "Dolor",
        "sit",
        "Amet",
        "Consectetur",
        "Adipiscing",
        "Elit",
        "sed",
        "Eget",
    ]
    title = (
        " ".join(random.choice(words) for _ in range(3))
        + " "
        + "".join(random.choice(string.ascii_letters) for _ in range(5))
    )
    return title


users = [
    models.User(username=name, username_lower=name.lower(), email=email)
    for name, email in name_email_tuples
]
# users = models.User.query.all()
[user.set_password("password") for user in users]
for user in users:
    settings = models.UserSettings(user=user)


def is_draft(pct: float = 1 / 3) -> bool:
    return random.random() < pct


articles = [
    models.Article(
        title=generate_title(),
        content=random.choice(contents),
        is_draft=is_draft(),
        user=random.choice(users),
    )
    for _ in range(5000)
]

with open("/usr/share/dict/words", "r") as f:
    words = random.sample([line for line in f.read().split("\n")], k=25)

keywords = [models.ArticleData(key="keyword", value=word) for word in words]

for article in articles:
    article.data = random.sample(keywords, k=5)

db.session.add_all(articles)
db.session.commit()
