from django.core.management.base import BaseCommand
from django.conf import settings
from sell.models import Profile
import os
import shutil

class Command(BaseCommand):
    help = 'Move profile image files from nested media/media path to correct media path and update DB entries'

    def handle(self, *args, **options):
        src_dir = os.path.join(settings.MEDIA_ROOT, 'media', 'courses', 'profiles')
        dest_dir = os.path.join(settings.MEDIA_ROOT, 'courses', 'profiles')

        if not os.path.exists(src_dir):
            self.stdout.write(self.style.WARNING(f"Source directory does not exist: {src_dir}. Nothing to move."))
        else:
            os.makedirs(dest_dir, exist_ok=True)
            files = os.listdir(src_dir)
            for fname in files:
                src = os.path.join(src_dir, fname)
                dest = os.path.join(dest_dir, fname)
                try:
                    shutil.move(src, dest)
                    self.stdout.write(self.style.SUCCESS(f"Moved {src} -> {dest}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to move {src}: {e}"))

        # Update DB entries
        updated = 0
        for p in Profile.objects.all():
            if p.profile_image and p.profile_image.name.startswith('media/'):
                old_name = p.profile_image.name
                new_name = old_name.replace('media/', '', 1)
                p.profile_image.name = new_name
                p.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"Updated Profile id={p.id} image from {old_name} -> {new_name}"))

        self.stdout.write(self.style.NOTICE(f"Done. Files moved and {updated} DB entries updated."))
