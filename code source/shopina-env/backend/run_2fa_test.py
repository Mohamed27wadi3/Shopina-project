from django.contrib.auth import get_user_model
from users.services.user_service import UserService
User = get_user_model()
email = 'ghrib27wadi@gmail.com'
u = User.objects.filter(email=email).first()
if not u:
    u = User.objects.create_user(username='ghrib27wadi', email=email, password='TestPass123!')
    print('Created user', u.email)
else:
    print('Found user', u.email)
svc = UserService()
otp = svc.start_two_factor(u)
print('Returned OTP:', otp)
