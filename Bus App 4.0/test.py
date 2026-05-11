from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")             # anon usually
svc = os.getenv("SUPABASE_SERVICE_KEY")     # service_role

def dbg(resp, tag="resp"):
    print("----", tag, "----")
    print("status_code:", getattr(resp, "status_code", None))
    print("data:", getattr(resp, "data", None))
    print("error:", getattr(resp, "error", None))

client = create_client(url, key)
print("Testing SELECT with anon key")
dbg(client.table('schedules').select('*').limit(1).execute(), "anon select")

if svc:
    admin = create_client(url, svc)
    print("Testing INSERT with service_role key")
    schedule_data = {
        "bus_id": 1,
        "departure_date": "2025-10-06",
        "departure_time": "08:00",
        "available_seats": 40,
        "status": "active"
    }
    dbg(admin.table('schedules').insert(schedule_data).execute(), "service insert")
