import csv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from io import StringIO


questions = [
    {
        "question": "Ako sa voláte?",
        "options": [("Som z Mexika", "a"), ("Som rád", "b"), ("Som Juraj", "c")],
        "answer": "c"
    },
    {
        "question": "Kde je tabuľa?",
        "options": [("Je pod zemou", "a"), ("Je vpredu", "b"), ("Je neskoro", "c")],
        "answer": "b"
    },
    {
        "question": "Je ten muž ...?",
        "options": [("mladá", "a"), ("mladé", "b"), ("mladý", "c")],
        "answer": "c"
    },
    {
        "question": "Emil sa ... každé ráno",
        "options": [("vstáva", "a"), ("umýva", "b"), ("cvičí", "c")],
        "answer": "b"
    },
    {
        "question": "Ja neviem spievať, ale kamaráti ...",
        "options": [("vedia", "a"), ("vidia", "b"), ("vedú", "c")],
        "answer": "a"
    },
    {
        "question": "Som chorý ... ležať v posteli",
        "options": [("Smiem", "a"), ("Musím", "b"), ("Nemusím", "c")],
        "answer": "b"
    },
    {
        "question": "Eva pracuje ako novinárka v ...  časopise",
        "options": [("jednom", "a"), ("jednu", "b"), ("jednej", "c")],
        "answer": "a"
    },
    {
        "question": "V kuchyni na stole boli ...",
        "options": [("naše noví taniere", "a"), ("naši nové taniere", "b"), ("naše nové taniere", "c")],
        "answer": "c"
    },
    {
        "question": "Ideme na návštevu k ...",
        "options": [("nášho veselého spolužiaka", "a"), ("nášmu veselému spolužiakovi", "b"), ("našom veselom spolužiakovi", "c")],
        "answer": "b"
    },
    {
        "question": "Pani Nováková, máte ... zmrzlinu?",
        "options": [("radi", "a"), ("rada", "b"), ("rady", "c")],
        "answer": "b"
    },
    {
        "question": "Brat mi daroval tablet. ... mám tablet.",
        "options": [("Voči bratovi", "a"), ("Vďaka bratovi", "b"), ("Napriek bratovi", "c")],
        "answer": "b"
    },
    {
        "question": "V chladničke máme fľašu ...",
        "options": [("minerálne vody", "a"), ("minerálnu vodu", "b"), ("minerálnej vody", "c")],
        "answer": "c"
    },
    {
        "question": "Čím cestuje Martin? Martin cestuje do práce ... .",
        "options": [["trolejbusom", "a"], ["trolejbusu", "b"], ["trolejbus", "c"]],
        "answer": "a"
    },
    {
        "question": "Jej manžel nerád čaká. Je ... .",
        "options": [["netrpezlivý", "a"], ["nepohodlný", "b"], ["nesmelý", "c"]],
        "answer": "a"
    },
    {
        "question": "Ulož si moju adresu do ... telefónu.",
        "options": [["pamäti", "a"], ["pamäte", "b"], ["pamätí", "c"]],
        "answer": "b"
    },
    {
        "question": "Máme bežecký tréning a beháme ... štadióna.",
        "options": [["po", "a"], ["okolo", "b"], ["cez", "c"]],
        "answer": "b"
    },
    {
        "question": "Všetky moje knihy sú už v ... .",
        "options": [["skrine", "a"], ["skrini", "b"], ["skriniam", "c"]],
        "answer": "b"
    },
    {
        "question": "... tu veľa študentov.",
        "options": [["Sú", "a"], ["Sme", "b"], ["Je", "c"]],
        "answer": "c"
    },
    {
        "question": "Obed bol ... dobrý.",
        "options": [["veľmi", "a"], ["veľa", "b"], ["viac", "c"]],
        "answer": "a"
    },
    {
        "question": "Kto je váš nový riaditeľ? Neviem, ja ešte ... nášho nového riaditeľa.",
        "options": [["nemám", "a"], ["nepoznám", "b"], ["neviem", "c"]],
        "answer": "b"
    },
    {
        "question": "Večer ... kávu. (negat.)",
        "options": [["nikto nepijem", "a"], ["nikdy nepijem", "b"], ["pijem nikdy", "c"]],
        "answer": "b"
    },
    {
        "question": "... šunková pizza?",
        "options": [["Dáš si", "a"], ["Si rád", "b"], ["Chutí ti", "c"]],
        "answer": "с"
    },
    {
        "question": "... sa vráti otec z práce, budeme večerať.",
        "options": [["Keď", "a"], ["Kedy", "b"], ["Odkedy", "c"]],
        "answer": "a"
    },
    {
        "question": "Kam idú susedia na dovolenku? Idú ... Paríža.",
        "options": [["z", "a"], ["do", "b"], ["na", "c"]],
        "answer": "b"
    },
    {
        "question": "... rok som pracoval v Anglicku.",
        "options": [["Minulý", "a"], ["Minule", "b"], ["Vlani", "c"]],
        "answer": "a"
    },
    {
        "question": "Prepáčte, ale tu ... parkovať. Tu je zakázané parkovať.",
        "options": [["neviete", "a"], ["nesmiete", "b"], ["nemusíte", "c"]],
        "answer": "b"
    },
    {
        "question": "- Čo si robil cez víkend? - Cez víkend ... v záhrade.",
        "options": [["som pracoval", "a"], ["pracujem", "b"], ["pracoval som", "c"]],
        "answer": "a"
    },
    {
        "question": "Aké bolo vlani počasie v apríli? V apríli veľmi často ... .",
        "options": [["prší", "a"], ["pršalo", "b"], ["išiel dážď", "c"]],
        "answer": "b"
    },
    {
        "question": "Poznáte moju novú kolegyňu Marínu? Nie, ešte ... nepoznám.",
        "options": [["jej", "a"], ["ju", "b"], ["ňu", "c"]],
        "answer": "b"
    },
    {
        "question": "Keď som mala tri roky, ... čítať ani písať.",
        "options": [["nepoznala som", "a"], ["nevedela som", "b"], ["neviem", "c"]],
        "answer": "b"
    },
    {
        "question": "Viem hrať na klavíri a na flaute. A ty? ... .",
        "options": [["A ja", "a"], ["Ani ja", "b"], ["Aj ja", "c"]],
        "answer": "c"
    },
    {
        "question": "Mohol by si mi ... ten návrh emailom?",
        "options": [["dostať", "a"], ["poslať", "b"], ["pozvať", "c"]],
        "answer": "b"
    },
    {
        "question": "... sa nehovorí, to je tajomstvo.",
        "options": [["O tom", "a"], ["O to", "b"], ["Na to", "c"]],
        "answer": "a"
    },
    {
        "question": "Cez víkend ... relaxujem.",
        "options": [["väčšinou", "a"], ["nikdy", "b"], ["vôbec", "c"]],
        "answer": "a"
    },
    {
        "question": "Mal som veľa práce, ... som na to zabudol.",
        "options": [["ale", "a"], ["a preto", "b"], ["kedy", "c"]],
        "answer": "a"
    },
    {
        "question": "... si to prečítam, ty môžeš pripraviť večeru.",
        "options": [["Kedy", "a"], ["Kým", "b"], ["Počas", "c"]],
        "answer": "b"
    },
    {
        "question": "Prepáčte, že ... .",
        "options": [["meškám", "a"], ["zmeškám", "b"], ["som neskoro", "c"]],
        "answer": "a"
    },
    {
        "question": "Ešte neviem, ... budem mať zajtra čas.",
        "options": [["či", "a"], ["ak", "b"], ["keď", "c"]],
        "answer": "a"
    },
    {
        "question": "Chcel by som, ... si prišiel ku mne.",
        "options": [["aby", "a"], ["že", "b"], ["keby", "c"]],
        "answer": "a"
    },
    {
        "question": "V jedálni ... veľa študentov.",
        "options": [["jedia", "a"], ["jedli", "b"], ["jedlo", "c"]],
        "answer": "c"
    },
    {
        "question": "Rodičia sa starajú ... deti.",
        "options": [["o", "a"], ["pre", "b"], ["na", "c"]],
        "answer": "a"
    },
    {
        "question": "Bola si už na Ukrajine? - Nie, ... som nebola, ale bola som ... v Rakusku.",
        "options": [["už - ešte", "a"], ["ešte nie - už", "b"], ["ešte - už", "c"]],
        "answer": "c"
    },
    {
        "question": "Tvrdohlavý ako ... . Pracovitý ako ... . Hladný ako ... .",
        "options": [["vlk - ryba - mačka", "a"], ["kôň - ryba - medveď", "b"], ["osol - včelička - vlk", "c"]],
        "answer": "c"
    },
    {
        "question": "Záver tejto zimy priniesol mínusové teploty, ktoré ... a prekvapili celé Slovensko.",
        "options": [["potrpeli", "a"], ["potrápili", "b"], ["týrali", "c"]],
        "answer": "b"
    },
    {
        "question": "Jánošíkove diery sú domovom mnohých vzácnych a ... zvierat i rastlín.",
        "options": [["pohrozených", "a"], ["zhrozených", "b"], ["ohrozených", "c"]],
        "answer": "c"
    },
    {
        "question": "Jedna z architektonicky najzaujímavejších stavieb Bratislavy je ... budova Slovenského rozhlasu na Mýtnej ulici.",
        "options": [["nepochybne", "a"], ["nevyhnutne", "b"], ["neodkladne", "c"]],
        "answer": "a"
    },
    {
        "question": "Lanovku na Lomnický štít dnes berieme ako ... .",
        "options": [["predpoklad", "a"], ["pravdivosť", "b"], ["samozrejmosť", "c"]],
        "answer": "c"
    },
    {
        "question": "Mnoho ľudí počas svojho života pochybuje o tom, či vykonávajú prácu, na ktorú sú ... .",
        "options": [["predurčení", "a"], ["predpovedaní", "b"], ["zvolení", "c"]],
        "answer": "a"
    },
    {
        "question": "Najväčším ... pre turistov je samotný Slovenský raj.",
        "options": [["blahom", "a"], ["lákadlom", "b"], ["ťahom", "c"]],
        "answer": "b"
    },
    {
        "question": "Ľudia neustále vymýšľajú nové a nové veci, ktoré by nám mohli uľahčiť a zjednodušiť život, aby sme nemuseli až tak tvrdo pracovať a ...",
        "options": [["namáhať sa", "a"], ["nádejať sa", "b"], ["míňať", "c"]],
        "answer": "a"
    }
]

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {
        "score": 0,
        "current_q": 0,
        "answers": [],
        "name": ""
    }
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привіт!Напиши ,будь ласка, своє ім'я та прізвище?"
    )
    return

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_data:
        await update.message.reply_text("Спочатку напишіть /start")
        return

    name = update.message.text.strip()
    user_data[user_id]["name"] = name

    await update.message.reply_text(
        f"Радий знайомству, {name}! 🖐️\n\n"
        "Вас чекає тест зі словацької мови. У кожному запитанні буде один правильний варіант відповіді.\n"
        "Обирайте варіант, натискаючи на кнопки під запитанням.\n\n"
        "Успіхів!"
    )

    await send_question(update, context)


async def send_question(update_or_callback, context):
    user_id = update_or_callback.effective_user.id
    current_q = user_data[user_id]["current_q"]

    if current_q < len(questions):
    #if current_q < 2:
        q = questions[current_q]
        buttons = [
            [InlineKeyboardButton(text=opt[0], callback_data=opt[1])]
            for opt in q["options"]
        ]
        markup = InlineKeyboardMarkup(buttons)
        await context.bot.send_message(
            chat_id=update_or_callback.effective_chat.id,
            text=f"{current_q + 1}. {q['question']}",
            reply_markup=markup
        )
    else:
        await finish_test(update_or_callback, context)

def evaluate_level(score, total):
    percent = score / total
    if percent == 1:
        return "C1–C2 (вільне володіння)\nРекомендований курс: Advanced або SpeakingClub\nДля запису на курси напишіть менеджерці Ірині:\n@iireeennn"
    elif percent >= 0.7:
        return "B1–B2 (середній рівень)\nРекомендований курс: Intermediate\nДля запису на курси напишіть менеджерці Ірині:\n@iireeennn"
    elif percent >= 0.4:
        return "A2 (початковий рівень)\nРекомендований курс: Beginner\nДля запису на курси напишіть менеджерці Ірині:\n@iireeennn"
    else:
        return "A1 (базовий рівень)\nРекомендований курс: Beginner\nДля запису на курси напишіть менеджерці Ірині:\n@iireeennn"

async def handle_answer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    current_q = user_data[user_id]["current_q"]
    selected = query.data
    correct = questions[current_q]["answer"]

    user_data[user_id]["answers"].append({
        "question": questions[current_q]["question"],
        "selected": selected,
        "correct": correct
    })

    if selected == correct:
        user_data[user_id]["score"] += 1

    user_data[user_id]["current_q"] += 1
    await send_question(update, context)


async def finish_test(update, context):
    user_id = update.effective_user.id
    score = user_data[user_id]["score"]
    total = len(questions)
    level = evaluate_level(score, total)
    name = user_data[user_id]["name"]

    log = StringIO()
    writer = csv.writer(log)
    writer.writerow(["Запитання", "Ваша відповідь", "Правильна відповідь", "Правильно?"])

    for ans in user_data[user_id]["answers"]:
        writer.writerow([
            ans["question"],
            ans["selected"],
            ans["correct"],
            "Так" if ans["selected"] == ans["correct"] else "Ні"
        ])
    log.seek(0)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Тест завершено!\n📊 Результат: {score}/{total}\n🏷️ Рівень: {level}"
    )
    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=InputFile(log, filename="results.csv"),
        caption="Ось файл з правильними відповідями:"
    )

    log.seek(0)
    await context.bot.send_message(
        chat_id= "YOUR_ID",
        text=f"🧑 Ім'я: {name}\n📊 Результат: {score}/{total}\n🏷️ Рівень: {level}"
    )
    await context.bot.send_document(
        chat_id="YOUR_ID",
        document=InputFile(log, filename=f"{name}_results.csv"),
        caption=f"Результати тесту від {name}"
    )


if __name__ == '__main__':
    app = ApplicationBuilder().token("TOKEN_NUM").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_name))

    app.add_handler(CallbackQueryHandler(handle_answer_callback))

    app.run_polling()

