import hashlib
import random
import argparse
import sys


def calculate_participant_hash(participants):
    """
    Calculates the SHA-256 hash of the sorted participant list.

    Args:
        participants (list): List of participant names.

    Returns:
        str: The hex digest of the hash.
    """
    # Canonicalize by sorting
    candidates = sorted(participants)
    # Use a newline separator to prevent concatenation collisions
    # e.g., ["Alice", "Bob"] vs ["Ali", "ceBob"]
    raw_string = "\n".join(candidates)
    return hashlib.sha256(raw_string.encode("utf-8")).hexdigest()


def get_fair_shuffle(participants, future_salt):
    """
    Shuffles a list of participants deterministically based on a future salt.

    Args:
        participants (list): List of unique participant names/IDs.
        future_salt (str): A string derived from a future public signal.

    Returns:
        tuple: (shuffled_list, participant_hash, seed_int)
    """
    # Validate future_salt
    if not future_salt or not str(future_salt).strip():
        raise ValueError("Future salt cannot be empty or whitespace.")

    # Canonicalize the participant list by sorting.
    # This ensures that the input order in the file doesn't affect the outcome,
    # making the process robust against scrambling the input file.
    candidates = sorted(participants)

    # Calculate Participant Hash (for commitment verification)
    participant_hash = calculate_participant_hash(participants)

    # 1. Deterministic Random Seed
    # Combine all participants and the salt to create a unique seed string.
    # Note: We reconstruct the raw string here to ensure it matches the hash logic
    # We use the same newline separator for consistency
    raw_string = "\n".join(candidates) + str(future_salt)
    
    # Generate a SHA-256 hash
    seed_hash = hashlib.sha256(raw_string.encode("utf-8")).hexdigest()
    
    # Convert the full digest to an integer to use as the seed
    seed_int = int(seed_hash, 16)
    
    # 2. Shuffle
    # Initialize the random number generator with our deterministic seed
    rng = random.Random(seed_int)
    
    # Create a copy to shuffle.
    shuffled_list = candidates.copy()
    rng.shuffle(shuffled_list)
    
    return shuffled_list, participant_hash, seed_int


def load_participants(file_path):
    """Reads participants from a file, one per line."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # Read lines, strip whitespace, and filter out empty lines
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Conduct a fair, deterministic lucky draw using a future signal."
    )

    parser.add_argument(
        "file",
        help="Path to the text file containing the list of participants (one per line).",
    )

    parser.add_argument(
        "signal",
        help="The future public signal (e.g., Bitcoin price, stock index). Treated as a string.",
    )

    parser.add_argument(
        "-n",
        "--top",
        type=int,
        default=3,
        help="Number of winners to display (default: 3).",
    )

    args = parser.parse_args()

    # Load participants
    participants = load_participants(args.file)
    print(f"Loaded {len(participants)} participants from '{args.file}'.")

    # Run the fair shuffle
    try:
        shuffled_results, participant_hash, seed_int = get_fair_shuffle(
            participants, args.signal
        )
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Output results
    print(f"\n--- Fair Lucky Draw Results ---")
    print(f"Future Signal: '{args.signal}'")
    print(f"Total Participants: {len(participants)}")
    print(f"Participant Hash: {participant_hash}")
    print(f"Seed:             {seed_int}")
    print("-" * 30)

    print(f"Top {args.top} Winners:")
    for i, winner in enumerate(shuffled_results[: args.top], 1):
        print(f"{i}. {winner}")

    print("-" * 30)
    # print(f"Full Shuffled List: {shuffled_results}") # Uncomment if full list is needed


if __name__ == "__main__":
    main()
