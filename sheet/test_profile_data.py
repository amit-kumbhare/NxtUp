from sheet.models import user
# import os
# import django

# # Set up Django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cftracker.settings")
# django.setup()

# Get your user
u = user.objects.get(handle="Northmen")

# Print Difficulty Stats
print("\n=== Difficulty Stats ===")
print("Easy:", u.difficulty.easy)
print("Medium:", u.difficulty.medium)
print("Hard:", u.difficulty.hard)

# Print Topic-wise Stats
print("\n=== Topic-wise Stats ===")
print("Graphs:", u.topic_wise.graphs)
print("DP:", u.topic_wise.dp)
print("Greedy:", u.topic_wise.greedy)
print("Binary Search:", u.topic_wise.binary_search)
print("Data Structures:", u.topic_wise.data_structures)
print("Math:", u.topic_wise.math)
print("Strings:", u.topic_wise.strings)
print("DFS and Similar:", u.topic_wise.dfs)
print("Shortest Paths:", u.topic_wise.shortest_paths)
print("Trees:", u.topic_wise.trees)
print("Two Pointer:", u.topic_wise.two_pointer)
print("Sliding Window:", u.topic_wise.sliding_window)
print("Implementation:", u.topic_wise.implementation)
print("DSU:", u.topic_wise.dsu)
print("Bitmasks:", u.topic_wise.bitmasks)