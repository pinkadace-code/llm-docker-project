# LLM Docker Project

Rīks kas izmanto AI lai analizētu datubāzi un atbildētu uz jautājumiem latviešu valodā.

## Sastāvdaļas

- **main.py** — savienojas ar datubāzi, ģenerē kontekstu un SQL vaicājumus
- **ui.py** — tīmekļa interfeiss jautājumu uzdošanai
- **Groq AI** — LLM modelis (llama-3.3-70b-versatile)
- **MySQL** — datubāze (direct_payments)

## Prasības

- Docker Desktop
- Groq API atslēga
- MySQL datubāze

## Instalācija

1. Klonē repository:
```bash
   git clone https://github.com/pinkadace-code/llm-docker-project
   cd llm-docker-project
```

2. Izveido `.env` failu:
GROQ_API_KEY=tava_atslēga
DB_HOST=datubāzes_adrese
DB_PORT=3306
DB_USER=lietotājvārds
DB_PASSWORD=parole
DB_NAME=datubāzes_nosaukums


3. Palaid Docker:
```bash
   docker compose up --build
```

4. Atver pārlūkā:
http://localhost:5000

## Izmantotās bibliotēkas

- mysql-connector-python
- groq
- pandas
- matplotlib
- seaborn
- flask

## AI modelis

- **Pakalpojums:** Groq API
- **Modelis:** llama-3.3-70b-versatile