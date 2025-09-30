import anthropic
import pandas as pd
import numpy as np
from tqdm import tqdm

tqdm.pandas()

api_key = "your anthropic api key"


data = pd.read_excel("contact_with_mail_content.xlsx")

email = {
    "BNP Paribas": "bnpparibas.com",
    "SGCIB": "sg-cib.com",
    "CACIB": "ca-cib.com",
    "HSBC": "hsbc.com",
    "Natixis": "natixis.com",
    "Morgan Stanley": "morganstanley.com",
    "Bank of America": "bofa.com",
    "Citi": "citi.com",
    "UBS": "ubs.com",
    "ODDO BHF": "oddo-bhf.com",
    "Barclays": "barclays.com",
}


def create_email(row):
    entreprise = row["Entreprise"]
    mail = row["Prenom"].lower() + row["Nom"].lower() + "@" + email[entreprise]
    return mail


# data["email"] = data.progress_apply(create_email, axis=1)


# data.to_excel("./contact_with_mail.xlsx")


def prompt_mail(prenom, nom, entreprise, poste):
    prompt = f"<context>  Je suis étudiant à CentraleSupélec, passionné par la finance de marché et la finance quantitative.  Je suis actuellement Data Scientist chez Crédit Agricole CIB, où je développe des modèles prédictifs en utilisant le Machine Learning appliqué aux activités de marché.  Je mène notamment un projet de recherche sur l’utilisation des réseaux de neurones et leurs applications aux produits dérivés de taux.  Je maîtrise Python et ses principales librairies (numpy, pandas, scikit-learn, PyTorch).  Je recherche un stage de 6 mois à partir du 01/03/2026.</context>  <task>  Reformule le mail de candidature ci-dessous afin qu’il soit plus fluide, concis et naturel, tout en conservant un ton professionnel et respectueux.  Personnalise le mail en fonction du poste et de l’entreprise indiqués.  Ne te contente pas de remplacer les variables : réorganise si nécessaire, et propose une version différente mais équivalente. Tu peux garder la même amorce, mais adapte la au poste.  Exemple initial (à reformuler) :  'Bonjour Monsieur Mouawad,  Je vous adresse ma candidature pour un stage de six mois en quant trading au sein de votre équipe chez HSBC, à compter de mars 2026, dans le cadre de mon second stage de césure.  Actuellement Data Scientist au sein de Crédit Agricole CIB, je mène des recherches sur les réseaux de neurones et leurs applications aux produits de taux. Cette expérience m’a permis de consolider mes compétences en Python (modélisation quantitative, développement d’outils analytiques, machine learning), tout en me donnant une première exposition à l’intersection entre technologie et marchés.  Je souhaite désormais évoluer vers une expérience plus directement orientée marché, où je pourrais mettre à profit mes compétences techniques pour contribuer à vos projets de trading quantitatif.  Vous trouverez ci-joint mon CV. Je reste à votre disposition pour toute information complémentaire.  Bien cordialement,  Amin Belfkira.'  </task>  <information>  Prénom : {prenom}, Nom : {nom}, Poste : {poste}, Entreprise : {entreprise}  </information>  <response>  Renvoie uniquement le mail reformulé, sans autre texte.  </response>"

    return prompt


def prompt_cv(entreprise, poste):

    prompt = f"You will be adapting a French CV header to match a specific job position and company. Here is the original CV header that needs to be adapted:'CentraleSupélec engineering student with strong skills in Python, data science, and quantitative finance, eager to join Barclays Rates Structuring team to contribute to innovative product design, market analysis, and quantitative research on interest rate derivatives.' Here is the job position of the recruiter. You should adapt the header for a job/position in his team:<poste> {poste} </poste> Here is the company you should adapt the header for:<entreprise> {entreprise}</entreprise> Your task is to reformulate and adapt this CV header to be tailored specifically for the given position and company. Follow these guidelines: - Keep the core qualifications (CentraleSupélec engineering student, Python, data science, quantitative finance) as they are valuable assets - Replace 'Barclays Rates Structuring team' with the specific company and position provided- Adapt the specific contributions mentioned (innovative product design, market analysis, quantitative research on interest rate derivatives) to match what would be relevant for the new position and company- Maintain the same enthusiastic and professional tone- Keep the header concise and impactful- Write in the same language as the original (French or English, depending on the context) Important: Return ONLY the adapted header, nothing else. Do not include any explanations, comments, or additional text. "

    return prompt


def create_cv_header(row):
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": prompt_cv(row["Entreprise"], row["Poste"]),
            }
        ],
    )
    print(message.content[0].text)
    return message.content[0].text


def create_email_content(row):
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": prompt_mail(
                    row["Prenom"], row["Nom"], row["Entreprise"], row["Poste"]
                ),
            }
        ],
    )
    print(message.content[0].text)
    return message.content[0].text


# data["content"] = data.progress_apply(create_email_content, axis=1)

data["cv_header"] = data.progress_apply(create_cv_header, axis=1)


data.to_excel("./contact_cv_header.xlsx")
