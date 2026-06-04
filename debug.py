import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cftracker.settings")
django.setup()

from sheet.models import submission, user, question
from sheet.services import all_submissions

# 1. Get our user
u = user.objects.get(handle="Northmen")

# 2. Fetch *all* submissions from CF directly
class MockRequest:
    def __init__(self, user):
        self.user = user
        self.method = "POST"
        self.GET = {}
        self.POST = {}
mock_request = MockRequest(u)
cf_submissions = all_submissions(mock_request)

print(f"Total CF submissions fetched: {len(cf_submissions)}")

# 3. Count ONLY unique OK problems from CF
cf_ok = set()
for sub in cf_submissions:
    if sub["verdict"] == "OK":
        prob_id = f"{sub['id']}{sub['index']}"
        cf_ok.add(prob_id)

print(f"CF unique OK problems: {len(cf_ok)}")

# 4. Our DB count
our_ok = set(
    submission.objects.filter(solver=u, verdict="OK")
    .values_list('problem__problem_id', flat=True)
)
print(f"Our DB unique OK problems: {len(our_ok)}")
print(f"Missing: {cf_ok - our_ok}")
print(f"Extra: {our_ok - cf_ok}")

# Check for gym problems in CF submissions
print("\nGym problems (contestId > 100000):")
gym_ok = set()
for sub in cf_submissions:
    if sub["verdict"] == "OK" and sub["id"] > 100000:
        prob_id = f"{sub['id']}{sub['index']}"
        gym_ok.add(prob_id)
        print(f"  {prob_id}: {sub['name']}")
print(f"Total gym OK problems: {len(gym_ok)}")