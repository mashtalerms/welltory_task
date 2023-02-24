import openai
import csv
import os


# Authenticate with OpenAI API
openai.api_key = "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"

# Define function to score a review
def score_review(review):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=(f"I would give this review a score between 1 and 10, with 10 being the most positive and 1 being the most negative.\n\nReview: {review}\nScore:"),
        max_tokens=1,
    )

    return int(response.choices[0].text.strip())

# Define function to analyze a CSV file of reviews
def analyze_reviews(file_path):
    # Define path for analyzed file
    file_dir, file_name = os.path.split(file_path)
    analyzed_file_path = os.path.join(file_dir, f"{os.path.splitext(file_name)[0]}_analyzed.csv")

    # Open input and output files
    with open(file_path, "r") as input_file, open(analyzed_file_path, "w", newline="") as output_file:
        # Define CSV readers and writers
        reader = csv.DictReader(input_file)
        fieldnames = reader.fieldnames + ["rate"]
        writer = csv.DictWriter(output_file, fieldnames)

        # Write header row to output file
        writer.writeheader()

        # Loop through reviews and score them
        for row in reader:
            row["rate"] = score_review(row["review"])
            writer.writerow(row)

    # Sort analyzed file by rating
    with open(analyzed_file_path, "r") as analyzed_file:
        reader = csv.DictReader(analyzed_file)
        sorted_rows = sorted(reader, key=lambda row: int(row["rate"]), reverse=True)

    # Write sorted rows to analyzed file
    with open(analyzed_file_path, "w", newline="") as analyzed_file:
        writer = csv.DictWriter(analyzed_file, fieldnames)
        writer.writeheader()
        for row in sorted_rows:
            writer.writerow(row)

    print(f"Analysis complete. Results written to {analyzed_file_path}")

# Call the function to analyze a file
file_path = "reviews.csv"
analyze_reviews(file_path)
