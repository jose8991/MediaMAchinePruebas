import os
import instaloader
import shutil
from datetime import datetime, timedelta
from instaloader import Profile, Post


def date_filter(date_min, date_max):
    def date_filter_inner(post: Post):
        return True if date_min <= post.date <= date_max else False
    return date_filter_inner


def main():
    instance = instaloader.Instaloader(download_geotags=True, download_comments=True)

    instance.login(user="_fernandrez_", passwd="Soleloen1987")

    now = datetime.now()
    fdago = now - timedelta(days=5)

    users = {
        "fernandrez":date_filter(fdago, now),
        "efegiraldoh":date_filter(fdago, now),
        "laantifitness_":date_filter(fdago, now),
        "mateofernandezpanesgourmet":date_filter(fdago, now),
        "villa_estefania_":date_filter(fdago, now),
        "fincalasnubes":date_filter(fdago, now),
        "ecohoteltierradeagua":date_filter(fdago, now),
        "naturalecohotel":date_filter(fdago, now),
        "carolinagelen":date_filter(fdago, now),
        "sinculpaporfavor":date_filter(fdago, now),
        "amalia.eats":date_filter(fdago, now),
        "mafe.eats":date_filter(fdago, now),
        "rewax_si":date_filter(fdago, now),
    }

    for user, dates in users.items():
        if os.path.exists(user):
            user_file = [f for f in os.listdir(user) if f.startswith(user) and f.endswith(".xz")][0]
            if user_file:
                y,m,d = now.year, str(now.month).zfill(2), str(now.day).zfill(2)
                if os.path.exists(f"{user}/{user_file}") and not os.path.exists(f"{user}/{y}{m}{d}_{user_file}"):
                    shutil.copy(f"{user}/{user_file}", f"{user}/{y}{m}{d}_{user_file}")
        instance.download_profile(profile_name=user, download_stories=False, download_tagged=False, post_filter=date_filter(*dates))


if __name__ == "__main__":
    main()
