import os
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.core.management import call_command
from dotenv import load_dotenv
import json

class Command(BaseCommand):
     help = "Seeds the database with initial data"

     def handle(self, *args, **kwargs):
          load_dotenv(override=True)
          
          SEED_PASSWORD = os.getenv("SEED_PASSWORD")

          if not SEED_PASSWORD:
               raise PermissionError("You are not permitted to do this action.")

          with open("seed_data.json", "r") as file:
               data = json.load(file)

          for entry in data:
               if entry["model"] == "auth.user":
                    entry["fields"]["password"] = make_password(SEED_PASSWORD)

          with open("seed_data.json", "w") as file:
               json.dump(data, file, indent=5)

          call_command("migrate")
          call_command("loaddata", "seed_data.json")

          self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))