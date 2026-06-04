import os
import django

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cftracker.settings")
django.setup()

from sheet.models import (
    user,
    submission,
    question,
    UserDifficultyStats,
    UserTopicStats
)
from sheet.essentials import create_user_ach
from django.test import RequestFactory


def main():
    print("=" * 80)
    print("CF TRACKER DEBUG SCRIPT")
    print("=" * 80)

    # Ask user for handle
    handle = input("Enter user handle to debug: ").strip()

    # Get user
    try:
        u = user.objects.get(handle=handle)
    except user.DoesNotExist:
        print(f"ERROR: User with handle '{handle}' not found!")
        return

    print(f"\n✅ Found user: {u.first_name} {u.last_name} (@{u.handle})")
    print(f"   - Rating: {u.rating}")
    print(f"   - Max rating: {u.MaxRating}")
    print(f"   - Rank: {u.rank}")
    print(f"   - Solved count: {u.solved_count}")

    # Check submissions
    print("\n" + "-" * 80)
    print("SUBMISSIONS")
    print("-" * 80)
    all_subs = submission.objects.filter(solver=u)
    ok_subs = all_subs.filter(verdict="OK")
    print(f"Total submissions: {all_subs.count()}")
    print(f"OK submissions: {ok_subs.count()}")

    if ok_subs.exists():
        first_ok = ok_subs.first()
        print(f"\nFirst OK submission:")
        print(f"  - Problem: {first_ok.problem}")
        print(f"  - Problem rating: {first_ok.problem.rating}")
        print(f"  - Problem tags: {first_ok.problem.tags}")

    # Check stats objects
    print("\n" + "-" * 80)
    print("USER STATS OBJECTS")
    print("-" * 80)
    # Check difficulty stats
    try:
        diff_stats = u.difficulty
        print("✅ UserDifficultyStats exists")
        print(f"  Easy: {diff_stats.easy}")
        print(f"  Medium: {diff_stats.medium}")
        print(f"  Hard: {diff_stats.hard}")
    except Exception as e:
        print(f"❌ UserDifficultyStats missing: {e}")
        print("   Creating it...")
        diff_stats, created = UserDifficultyStats.objects.get_or_create(user=u)
        print(f"   Created: {created}")

    # Check topic stats
    try:
        topic_stats = u.topic_wise
        print("\n✅ UserTopicStats exists")
        print(f"  Graphs: {topic_stats.graphs}")
        print(f"  DP: {topic_stats.dp}")
        print(f"  Greedy: {topic_stats.greedy}")
        print(f"  Binary Search: {topic_stats.binary_search}")
        print(f"  Data Structures: {topic_stats.data_structures}")
        print(f"  Math: {topic_stats.math}")
        print(f"  Strings: {topic_stats.strings}")
        print(f"  DFS: {topic_stats.dfs}")
        print(f"  Shortest Paths: {topic_stats.shortest_paths}")
        print(f"  Trees: {topic_stats.trees}")
        print(f"  Two Pointer: {topic_stats.two_pointer}")
        print(f"  Sliding Window: {topic_stats.sliding_window}")
        print(f"  Implementation: {topic_stats.implementation}")
        print(f"  DSU: {topic_stats.dsu}")
        print(f"  Bitmasks: {topic_stats.bitmasks}")
    except Exception as e:
        print(f"\n❌ UserTopicStats missing: {e}")
        print("   Creating it...")
        topic_stats, created = UserTopicStats.objects.get_or_create(user=u)
        print(f"   Created: {created}")

    # Test create_user_ach
    print("\n" + "-" * 80)
    print("RUNNING create_user_ach")
    print("-" * 80)
    factory = RequestFactory()
    request = factory.get('/')
    request.user = u

    try:
        response = create_user_ach(request)
        print(f"✅ create_user_ach succeeded!")
        print(f"   Response: {response}")
    except Exception as e:
        print(f"❌ create_user_ach failed: {e}")
        import traceback
        traceback.print_exc()
        return

    # Refresh data and show final stats
    print("\n" + "-" * 80)
    print("FINAL STATS AFTER create_user_ach")
    print("-" * 80)
    u.refresh_from_db()
    diff_stats.refresh_from_db()
    topic_stats.refresh_from_db()

    print(f"Solved count: {u.solved_count}")
    print(f"\nDifficulty stats:")
    print(f"  Easy: {diff_stats.easy}")
    print(f"  Medium: {diff_stats.medium}")
    print(f"  Hard: {diff_stats.hard}")

    print(f"\nTopic stats:")
    print(f"  Graphs: {topic_stats.graphs}")
    print(f"  DP: {topic_stats.dp}")
    print(f"  Greedy: {topic_stats.greedy}")
    print(f"  Binary Search: {topic_stats.binary_search}")
    print(f"  Data Structures: {topic_stats.data_structures}")
    print(f"  Math: {topic_stats.math}")
    print(f"  Strings: {topic_stats.strings}")
    print(f"  DFS: {topic_stats.dfs}")
    print(f"  Shortest Paths: {topic_stats.shortest_paths}")
    print(f"  Trees: {topic_stats.trees}")
    print(f"  Two Pointer: {topic_stats.two_pointer}")
    print(f"  Sliding Window: {topic_stats.sliding_window}")
    print(f"  Implementation: {topic_stats.implementation}")
    print(f"  DSU: {topic_stats.dsu}")
    print(f"  Bitmasks: {topic_stats.bitmasks}")

    print("\n" + "=" * 80)
    print("DONE!")
    print("=" * 80)


if __name__ == "__main__":
    main()
