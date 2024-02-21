import re
import csv

# Open the file
with open("outputFB.txt", "r", encoding="utf-8") as file:
    # Read the contents
    data = file.read()

# Define regular expressions to extract posts, reactions, comments, and shares
post_pattern = re.compile(r"^(.*?)\n(\d+h\s+·.*?)\n(.*?)\nTodas las reacciones:\n(\d+)\n(\d+)\nComentar\nCompartir", re.MULTILINE | re.DOTALL)
reaction_pattern = re.compile(r"Todas las reacciones:\n(\d+)", re.MULTILINE)
comment_pattern = re.compile(r"Todas las reacciones:\n\d+\n(\d+)\nComentar", re.MULTILINE)
share_pattern = re.compile(r"Todas las reacciones:\n\d+\n\d+\n(\d+)\nCompartir", re.MULTILINE)

# Find all posts, reactions, comments, and shares
posts = post_pattern.findall(data)
reactions = reaction_pattern.findall(data)
comments = comment_pattern.findall(data)
shares = share_pattern.findall(data)

# Match each post with its corresponding reactions, comments, and shares
post_data = []
for post, reaction_count, comment_count, share_count in zip(posts, reactions, comments, shares):
    title, _, content, _, _, _ = post
    reaction_count = int(reaction_count)
    comment_count = int(comment_count)
    share_count = int(share_count)
    post_data.append({
        "Title": title.strip(),
        "Reactions": reaction_count,
        "Comments": comment_count,
        "Share": share_count
    })

# Write the data into a CSV file
with open("output.csv", "w", encoding="utf-8", newline="") as csvfile:
    fieldnames = ["Title", "Reactions", "Comments", "Share"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(post_data)

print("CSV file created successfully!")
