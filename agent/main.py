#!/usr/bin/env python3
"""
Main script to run the Language Learning Agent.
Generates lesson plans from foreign language monologues using Google Gemini.
"""

import sys
from lesson_agent import LanguageLearningAgent


def main():
    """Main entry point for the language learning agent"""

    # Example monologue in Spanish
    example_spanish = """
    Hola, me llamo María y vivo en Madrid. Todos los días, me levanto a las siete de la mañana.
    Primero, me ducho y me visto. Luego, desayuno café con tostadas. Después del desayuno,
    voy al trabajo en metro. Trabajo en una oficina en el centro de la ciudad. Me gusta mi trabajo
    porque mis compañeros son muy simpáticos. A mediodía, como con mis colegas en un restaurante
    cerca de la oficina. Por la tarde, si tengo tiempo, voy al gimnasio o doy un paseo por el parque.
    Regreso a casa alrededor de las siete de la tarde. Por la noche, preparo la cena, veo la
    televisión o leo un libro. Me acuesto a las once de la noche. Los fines de semana, me gusta
    salir con mis amigos, ir al cine o visitar museos.
    """

    # Example monologue in French
    example_french = """
    Bonjour! Je m'appelle Pierre et j'habite à Paris. Je suis étudiant à l'université.
    Chaque jour, je me réveille à huit heures. Avant de partir, je prends mon petit-déjeuner.
    J'aime manger des croissants avec du café. Ensuite, je vais à l'université en vélo.
    Mes cours commencent à neuf heures et finissent à cinq heures de l'après-midi.
    J'étudie la littérature française et l'histoire. Le soir, je fais mes devoirs à la bibliothèque.
    Quelquefois, je rencontre mes amis au café. Nous discutons de nos études et de nos projets.
    Le week-end, j'aime visiter les musées ou me promener le long de la Seine.
    """

    print("Language Learning Lesson Plan Generator")
    print("=" * 80)
    print("\nSelect an example or provide your own monologue:")
    print("1. Spanish example (daily routine)")
    print("2. French example (student life)")
    print("3. Enter custom monologue")
    print("4. Load from file")

    choice = input("\nEnter your choice (1-4): ").strip()

    monologue = None

    if choice == "1":
        monologue = example_spanish
        print("\nUsing Spanish example monologue...")
    elif choice == "2":
        monologue = example_french
        print("\nUsing French example monologue...")
    elif choice == "3":
        print("\nEnter your monologue (press Ctrl+D or Ctrl+Z when finished):")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            monologue = "\n".join(lines)
    elif choice == "4":
        filepath = input("Enter file path: ").strip()
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                monologue = f.read()
            print(f"\nLoaded monologue from {filepath}")
        except FileNotFoundError:
            print(f"Error: File '{filepath}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    else:
        print("Invalid choice")
        sys.exit(1)

    if not monologue or not monologue.strip():
        print("Error: No monologue provided")
        sys.exit(1)

    try:
        print("\nInitializing Language Learning Agent...")
        agent = LanguageLearningAgent()

        print("Generating lesson plan (this may take a moment)...\n")
        lesson_plan = agent.generate_lesson_plan(monologue)

        formatted_output = agent.format_lesson_plan(lesson_plan)
        print(formatted_output)

        # Optionally save to file
        save = input("\nWould you like to save this lesson plan to a file? (y/n): ").strip().lower()
        if save == 'y':
            filename = input("Enter filename (default: lesson_plan.txt): ").strip()
            if not filename:
                filename = "lesson_plan.txt"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(formatted_output)
            print(f"\nLesson plan saved to {filename}")

    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        print("\nPlease ensure you have set the GOOGLE_API_KEY environment variable.")
        print("You can copy .env.example to .env and add your API key.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError generating lesson plan: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
