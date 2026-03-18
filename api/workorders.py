from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json, math, datetime

DEPARTMENTS = ["Engineering","Sales","Marketing","Finance","HR","Operations","Support","Legal","Product","Design"]
STATUSES = ["Open","In Progress","Resolved","Closed","Pending"]
PRIORITIES = ["Low","Medium","High","Critical"]
CATEGORIES = ["Bug Fix","Feature Request","Maintenance","Inquiry","Complaint","Upgrade","Installation","Training"]
ASSIGNEES = ["Alice Johnson","Bob Smith","Charlie Brown","Diana Prince","Edward Norton","Fiona Apple","George Lucas","Helen Troy","Ivan Petrov","Julia Roberts"]

def generate_records(total=10050):
    records = []
    base_date = datetime.datetime(2024, 1, 1)
    for i in range(1, total + 1):
        created = base_date + datetime.timedelta(hours=i)
        records.append({
            "id": i,
            "orderNo": f"WO-{10000+i}",
            "title": f"Work order {i} - {CATEGORIES[i % len(CATEGORIES)]} for {DEPARTMENTS[i % len(DEPARTMENTS)]}",
            "status": STATUSES[i % len(STATUSES)],
            "priority": PRIORITIES[i % len(PRIORITIES)],
            "category": CATEGORIES[i % len(CATEGORIES)],
            "department": DEPARTMENTS[i % len(DEPARTMENTS)],
            "assignee": ASSIGNEES[i % len(ASSIGNEES)],
            "createdAt": created.strftime("%Y-%m-%d %H:%M:%S"),
            "updatedAt": (created + datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
        })
    return records

ALL_RECORDS = generate_records(10050)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        page = max(1, int(params.get("pageIndex", [1])[0]))
        size = min(1000, max(1, int(params.get("pageSize", [100])[0])))
        total = len(ALL_RECORDS)
        start = (page - 1) * size
        data = {
            "success": True,
            "data": ALL_RECORDS[start:start+size],
            "pageIndex": page,
            "pageSize": size,
            "TotalRecords": total,
            "TotalPages": math.ceil(total / size),
        }
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
