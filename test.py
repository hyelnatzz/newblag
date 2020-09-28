from datetime import datetime


t = datetime.strptime('2020-09-26 00:06:28', '%Y-%m-%d %H:%M:%S')
f_t = datetime.strftime(t, '%B %d, %Y at %I:%M%p')

print(f_t)