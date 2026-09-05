"""
Smart Study Planner
--------------------
A console-based program to log, review, and analyse study sessions
across different subjects over a semester. Data is saved to and
loaded from a text file (study_log.txt) so it persists between runs.
"""

import os

DATA_FILE = "study_log.txt"


# ---------------------------------------------------------------------
# c) classify_session(duration)
# ---------------------------------------------------------------------
def classify_session(duration):
    """Classify a session's length based on its duration in minutes."""
    # duration is expected to already be a valid positive number here
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


# ---------------------------------------------------------------------
# g) load_sessions() / save_sessions()
# ---------------------------------------------------------------------
def load_sessions():
    """
    Load sessions from study_log.txt into a list of dictionaries.
    If the file does not exist yet (first ever run), return an empty list
    instead of crashing.
    """
    sessions = []

    # If the file has never been created, there is nothing to load.
    if not os.path.exists(DATA_FILE):
        return sessions

    with open(DATA_FILE, "r") as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue  # skip blank lines

            # Each line is stored as: subject|topic|date|duration
            parts = line.split("|")
            if len(parts) != 4:
                continue  # skip any malformed/corrupted line

            subject, topic, date, duration_text = parts
            try:
                duration = float(duration_text)
            except ValueError:
                continue  # skip lines with a bad duration value

            session = {
                "subject": subject,
                "topic": topic,
                "date": date,
                "duration": duration
            }
            sessions.append(session)

    return sessions


def save_sessions(sessions):
    """Save every session in the list to study_log.txt, overwriting it."""
    with open(DATA_FILE, "w") as file:
        for s in sessions:
            # Using | as a separator since subject/topic are unlikely to contain it
            line = s["subject"] + "|" + s["topic"] + "|" + s["date"] + "|" + str(s["duration"])
            file.write(line + "\n")


# ---------------------------------------------------------------------
# b) add_session()
# ---------------------------------------------------------------------
def add_session(sessions):
    """Prompt the user for session details and add them to the list."""
    print("\n--- Add a Study Session ---")
    subject = input("Subject: ").strip()
    topic = input("Topic covered: ").strip()
    date = input("Date / day label (e.g. Monday or 2026-09-04): ").strip()

    # Keep asking until the user gives a valid positive number for duration
    duration = None
    while duration is None:
        raw_duration = input("Duration in minutes: ").strip()
        try:
            value = float(raw_duration)
            if value <= 0:
                print("Duration must be a positive number. Try again.")
            else:
                duration = value
        except ValueError:
            print("That's not a valid number. Try again.")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration
    }
    sessions.append(session)
    print("Session added successfully!\n")


# ---------------------------------------------------------------------
# d) view_sessions()
# ---------------------------------------------------------------------
def view_sessions(sessions):
    """Display every logged session in a neatly formatted table."""
    print("\n--- All Study Sessions ---")
    if len(sessions) == 0:
        print("No sessions have been logged yet.\n")
        return

    # Header row
    print("{:<15}{:<15}{:<10}{:<10}{:<10}".format(
        "Subject", "Topic", "Date", "Minutes", "Type"))
    print("-" * 60)

    for s in sessions:
        session_type = classify_session(s["duration"])
        print("{:<15}{:<15}{:<10}{:<10}{:<10}".format(
            s["subject"], s["topic"], s["date"], s["duration"], session_type))
    print()


# ---------------------------------------------------------------------
# e) search_by_subject(subject)
# ---------------------------------------------------------------------
def search_by_subject(sessions):
    """Search and display all sessions for a given subject (case-insensitive)."""
    print("\n--- Search Sessions by Subject ---")
    subject = input("Enter subject name to search: ").strip()

    # Case-insensitive match
    matches = []
    for s in sessions:
        if s["subject"].lower() == subject.lower():
            matches.append(s)

    if len(matches) == 0:
        print("No sessions found for subject '" + subject + "'.\n")
        return

    print("{:<15}{:<15}{:<10}{:<10}{:<10}".format(
        "Subject", "Topic", "Date", "Minutes", "Type"))
    print("-" * 60)

    total_minutes = 0
    for s in matches:
        session_type = classify_session(s["duration"])
        print("{:<15}{:<15}{:<10}{:<10}{:<10}".format(
            s["subject"], s["topic"], s["date"], s["duration"], session_type))
        total_minutes = total_minutes + s["duration"]

    print("-" * 60)
    print("Total time spent on " + subject + ": " + str(total_minutes) + " minutes "
          + "(" + str(round(total_minutes / 60, 2)) + " hours)\n")


# ---------------------------------------------------------------------
# f) study_statistics()
# ---------------------------------------------------------------------
def study_statistics(sessions):
    """Compute and display overall study statistics."""
    print("\n--- Study Statistics ---")
    if len(sessions) == 0:
        print("No sessions have been logged yet.\n")
        return

    total_minutes = 0
    subject_totals = {}  # subject name -> total minutes

    for s in sessions:
        total_minutes = total_minutes + s["duration"]

        subject = s["subject"]
        if subject in subject_totals:
            subject_totals[subject] = subject_totals[subject] + s["duration"]
        else:
            subject_totals[subject] = s["duration"]

    # Overall total
    total_hours = total_minutes / 60
    print("Total hours studied overall: " + str(round(total_hours, 2)) + " hours\n")

    # Per-subject totals
    print("Hours studied per subject:")
    for subject in subject_totals:
        hours = subject_totals[subject] / 60
        print("  " + subject + ": " + str(round(hours, 2)) + " hours")

    # Weakest subject (least total time)
    weakest_subject = None
    weakest_minutes = None
    for subject in subject_totals:
        if weakest_minutes is None or subject_totals[subject] < weakest_minutes:
            weakest_minutes = subject_totals[subject]
            weakest_subject = subject

    print("\nWeakest area (least total study time): " + weakest_subject
          + " (" + str(round(weakest_minutes / 60, 2)) + " hours)")

    # Longest single session
    longest_session = sessions[0]
    for s in sessions:
        if s["duration"] > longest_session["duration"]:
            longest_session = s

    print("Longest session recorded: " + longest_session["subject"] + " - "
          + longest_session["topic"] + " (" + str(longest_session["duration"])
          + " minutes, " + classify_session(longest_session["duration"]) + ")\n")


# ---------------------------------------------------------------------
# a) main() - menu-driven interface
# ---------------------------------------------------------------------
def main():
    # Load any sessions saved from a previous run
    sessions = load_sessions()

    while True:
        print("========== SMART STUDY PLANNER ==========")
        print("1. Add a study session")
        print("2. View all sessions")
        print("3. Search sessions by subject")
        print("4. View statistics")
        print("5. Save and exit")
        print("===========================================")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            search_by_subject(sessions)
        elif choice == "4":
            study_statistics(sessions)
        elif choice == "5":
            save_sessions(sessions)
            print("Sessions saved to " + DATA_FILE + ". Goodbye!")
            break
        else:
            # Reject invalid choices without crashing
            print("Invalid choice. Please enter a number from 1 to 5.\n")


if __name__ == "__main__":
    main()
