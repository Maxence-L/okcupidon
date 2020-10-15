from dataparser import parse_profile

with open('profile.html') as file:
    print(parse_profile(1111, file))
