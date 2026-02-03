from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()

# Find all users
all_users = User.objects.all().order_by('username', 'id')
print(f"Total users in database: {all_users.count()}\n")

# Print all users
for user in all_users:
    print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")

# Find duplicates by email
duplicates = User.objects.values('email').annotate(count=Count('id')).filter(count__gt=1, email__isnull=False).exclude(email='')
print(f"\n\nDuplicate emails found: {duplicates.count()}")
for dup in duplicates:
    users_with_email = User.objects.filter(email=dup['email'])
    print(f"Email: {dup['email']}, Count: {dup['count']}")
    for u in users_with_email:
        print(f"  - ID: {u.id}, Username: {u.username}")
        
# Delete duplicates keeping only the first one
deleted_count = 0
for dup in duplicates:
    users_with_email = User.objects.filter(email=dup['email']).order_by('id')
    # Keep first, delete rest
    for user in users_with_email[1:]:
        print(f"Deleting duplicate: ID {user.id}, Username {user.username}, Email {user.email}")
        user.delete()
        deleted_count += 1

print(f"\nDeleted {deleted_count} duplicate users")
print(f"Final user count: {User.objects.count()} users")
