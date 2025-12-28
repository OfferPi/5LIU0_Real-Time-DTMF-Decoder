# Libraries import
import argparse
import random
import time

def main():
    # Setup argument parsing (only -r is required)
    parser = argparse.ArgumentParser(description="Print 20 numbers (0-9) with random intervals (1-4s).")
    parser.add_argument('-r', '--run', type=int, required=True, help="Run integer (used as seed)")
    
    args = parser.parse_args()

    # Set the seed based only on the run number
    random.seed(args.run)

    # Print header information
    print(f"--- Starting sequence for Run: {args.run} ---")
    print(f"--- Numbers: 0-9 | Interval: 1.0s - 4.0s ---")

    # Generate and print 20 numbers
    for i in range(1, 21):
        # Generate number between 0 and 9
        output_number = random.randint(0, 9)
        
        # Calculate random interval: Between 1 and 4 seconds
        interval = random.uniform(1, 4)

        # Print the output immediately
        print(f"[{i}/20] Value: {output_number} (Next in {interval:.2f}s)", flush=True)

        # Wait for the interval (skip waiting after the last number)
        if i < 20:
            time.sleep(interval)

    print("--- Done ---")

if __name__ == "__main__":
    main()
