# Fair Lucky Draw

A simple, auditable, and authentic tool for conducting fair lucky draws using future public signals.

## Why this tool?

Traditional lucky draws are often "black boxes" – you never know if the organizer manipulated the result. This tool implements a **Commitment Scheme** to ensure absolute fairness:

1.  **Verifiable Logic:** The code is open source and deterministic.
2.  **Unpredictable Entropy:** The result depends on a **future public signal** (e.g., Bitcoin closing price, Stock Index) that is unknown at the time of commitment.

## How to Use (The Protocol)

To conduct a fair draw, follow these two phases:

### Phase 1: The Commitment (Before the Event)

1.  **Prepare the List:** Create a text file (e.g., `candidates.txt`) with one participant name per line.
2.  **Choose the Signal:** Publicly announce the **future signal** source.
    - _Example:_ "We will use the last 2 digits of the Bitcoin USD closing price on CoinMarketCap for the 10 PM - 11 PM trading window tonight."
3.  **Publish:** Publish the full list file and this repository to all participants.
    - _Note:_ Once published, the list **cannot** be changed.

### Phase 2: The Reveal (After the Event)

1.  **Get the Signal:** Wait for the event time to pass and retrieve the signal value.
    - _Example:_ Bitcoin price is `$98,765.43` -> Signal is `43`.
2.  **Run the Script:** Run the script with the participant file and the signal.

## Usage

```bash
# Basic usage (defaults to top 3 winners)
python fair_draw.py candidates.txt "43"

# Specify number of winners (e.g., top 5)
python fair_draw.py candidates.txt "43" -n 5

# Get help
python fair_draw.py --help
```

### Examples

**Example 1: Using signal "43", picking top 3**

```bash
python fair_draw.py candidates.txt "43" -n 3
```

Output:

```text
--- Fair Lucky Draw Results ---
Future Signal: '43'
Total Participants: 10
Participant Hash: 548c9eec1d21f4f5ff02254266c19c794d4196724535f1da57b8fee701fd8121
Seed:             47567774649538936044369692665710261716550568601311273110448917217524192329811
------------------------------
Top 3 Winners:
1. Grace
2. Heidi
3. Charlie
------------------------------
```

**Example 2: Using a different signal "99.99", picking top 3**

Notice how the winners change completely with a different signal.

```bash
python fair_draw.py candidates.txt "99.99" -n 3
```

Output:

```text
--- Fair Lucky Draw Results ---
Future Signal: '99.99'
Total Participants: 10
Participant Hash: 548c9eec1d21f4f5ff02254266c19c794d4196724535f1da57b8fee701fd8121
Seed:             64878408961966585079329822692674089190204533965471390227971372916984257242512
------------------------------
Top 3 Winners:
1. Grace
2. Heidi
3. Bob
------------------------------
```

**Example 3: Using signal "43", picking top 5**

The order remains consistent with Example 1, just revealing more winners.

```bash
python fair_draw.py candidates.txt "43" -n 5
```

Output:

```text
--- Fair Lucky Draw Results ---
Future Signal: '43'
Total Participants: 10
Participant Hash: 548c9eec1d21f4f5ff02254266c19c794d4196724535f1da57b8fee701fd8121
Seed:             47567774649538936044369692665710261716550568601311273110448917217524192329811
------------------------------
Top 5 Winners:
1. Grace
2. Heidi
3. Charlie
4. Ivan
5. Frank
------------------------------
```

### Input File Format (`candidates.txt`)

```text
Alice
Bob
Charlie
...
```

## Testing

To ensure the logic is correct and robust, you can run the included unit tests:

```bash
python test_fair_draw.py
```

The tests verify:

- **Determinism:** Same input + same signal = same result.
- **Order Independence:** Input file order does not affect the outcome.
- **Signal Sensitivity:** Changing the signal changes the result.
- **Duplicate Handling:** Duplicates are handled correctly (changing the seed).

## Algorithm

1.  **Seed Generation:** `SHA-256(sorted(participants) + signal_string)` -> Integer.

2.  **Shuffle:** `random.shuffle(sorted(participants))` seeded with the generated integer.

**Key Features:**

- **Order Independent:** The order of names in the input file does _not_ matter. `Alice, Bob` and `Bob, Alice` produce the exact same result.

- **Duplicate Sensitive:** If a name appears twice in the file, it is treated as two entries (increasing that person's probability). The seed will also change, resulting in a completely different shuffle.
