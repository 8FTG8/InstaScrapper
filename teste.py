import instaloader

ig = instaloader.Instaloader()

user = input("Enter de Instagram username: ")

ig.download_profile(user)