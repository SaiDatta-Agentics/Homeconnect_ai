import uuid
from datetime import datetime, timedelta
from app.database import SessionLocal, engine, Base
from app.models import User, Property, Enquiry, ChatMessage, SiteVisit, Notification, ActivityLog
from app.services.auth_service import hash_password

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(User).count() > 0: db.close(); return
    now = datetime.utcnow()

    users = [
        User(id="admin1", email="admin@homeconnect.ai", hashed_password=hash_password("admin123"), full_name="Sarah Mitchell", phone="(416) 555-0100", role="admin", avatar_color="#2563eb"),
        User(id="mgr1", email="james@homeconnect.ai", hashed_password=hash_password("demo1234"), full_name="James Anderson", phone="(512) 555-0200", role="sales_manager", avatar_color="#059669"),
        User(id="agent1", email="emily@homeconnect.ai", hashed_password=hash_password("demo1234"), full_name="Emily Chen", phone="(604) 555-0300", role="sales_agent", avatar_color="#d97706"),
        User(id="agent2", email="marcus@homeconnect.ai", hashed_password=hash_password("demo1234"), full_name="Marcus Johnson", phone="(416) 555-0400", role="sales_agent", avatar_color="#dc2626"),
        User(id="cust1", email="john@example.com", hashed_password=hash_password("customer1"), full_name="John Cooper", phone="(512) 555-1001", role="customer", avatar_color="#7c3aed"),
        User(id="cust2", email="lisa@example.com", hashed_password=hash_password("customer1"), full_name="Lisa Park", phone="(604) 555-1002", role="customer", avatar_color="#db2777"),
        User(id="cust3", email="mike@example.com", hashed_password=hash_password("customer1"), full_name="Mike Torres", phone="(416) 555-1003", role="customer", avatar_color="#0891b2"),
    ]
    db.add_all(users); db.flush()

    props = [
        Property(id="p01", name="Maple Ridge 3BR Townhome", project_name="Maple Ridge Estates", property_type="Townhome", total_area_sqft=1800, price_usd=589000, price_per_sqft=327, bedrooms=3, bathrooms=3, total_floors=3, facing="South", status="available", location="North Toronto", address="142 Maple Ridge Blvd", city="Toronto", state="Ontario", country="Canada", zip_code="M2K 1B1", mls_id="MLS-TR-4521", year_built=2025, lot_size_sqft=2200, hoa_monthly=380, amenities="Community Center, Walking Trails, Dog Park, Playground, Tennis Courts", completion_date="Spring 2026", description="Modern 3-bed townhome with open-concept living, quartz countertops, and smart home features.", parking=2),
        Property(id="p02", name="Maple Ridge 4BR Detached", project_name="Maple Ridge Estates", property_type="Detached", total_area_sqft=2800, price_usd=899000, price_per_sqft=321, bedrooms=4, bathrooms=4, total_floors=2, facing="East", status="available", location="North Toronto", address="288 Maple Ridge Dr", city="Toronto", state="Ontario", country="Canada", zip_code="M2K 1B3", mls_id="MLS-TR-4522", year_built=2025, lot_size_sqft=5500, hoa_monthly=280, amenities="Community Center, Walking Trails, Tennis Courts", completion_date="Spring 2026", description="Spacious family home with finished basement, double garage, and backyard.", parking=2),
        Property(id="p03", name="Maple Ridge Executive Home", project_name="Maple Ridge Estates", property_type="Detached", total_area_sqft=3600, price_usd=1250000, price_per_sqft=347, bedrooms=5, bathrooms=5, total_floors=2, facing="South", status="available", location="North Toronto", address="50 Maple Crest Lane", city="Toronto", state="Ontario", country="Canada", zip_code="M2K 1B5", mls_id="MLS-TR-4523", year_built=2025, lot_size_sqft=8000, hoa_monthly=350, amenities="Private Pool, Community Center, Walking Trails", completion_date="Summer 2026", description="Premium executive home with chef's kitchen, home office, and resort-style backyard.", parking=3),
        Property(id="p04", name="Sunset Valley Ranch", project_name="Sunset Valley Homes", property_type="Ranch", total_area_sqft=2100, price_usd=425000, price_per_sqft=202, bedrooms=3, bathrooms=2, total_floors=1, facing="West", status="available", location="SW Austin", address="1205 Sunset Valley Dr", city="Austin", state="Texas", country="USA", zip_code="78735", mls_id="MLS-AUS-8901", year_built=2024, lot_size_sqft=7000, hoa_monthly=150, amenities="Pool & Spa, Fitness Center, Hiking Trails, BBQ Pavilion", completion_date="Ready Now", description="Single-story ranch with open floor plan, hill country views, and covered patio.", parking=2),
        Property(id="p05", name="Sunset Valley Colonial", project_name="Sunset Valley Homes", property_type="Colonial", total_area_sqft=3200, price_usd=625000, price_per_sqft=195, bedrooms=4, bathrooms=4, total_floors=2, facing="East", status="available", location="SW Austin", address="1340 Valley Vista Way", city="Austin", state="Texas", country="USA", zip_code="78735", mls_id="MLS-AUS-8902", year_built=2024, lot_size_sqft=9500, hoa_monthly=175, amenities="Pool, Fitness Center, Sports Courts, Nature Preserve", completion_date="Ready Now", description="Classic colonial with grand entry, bonus room, and premium lot backing to greenbelt.", parking=3),
        Property(id="p06", name="Sunset Valley Custom", project_name="Sunset Valley Homes", property_type="Custom Build", total_area_sqft=4200, price_usd=895000, price_per_sqft=213, bedrooms=5, bathrooms=5, total_floors=2, facing="South", status="available", location="SW Austin", address="1500 Hilltop Circle", city="Austin", state="Texas", country="USA", zip_code="78735", mls_id="MLS-AUS-8903", year_built=2025, lot_size_sqft=12000, hoa_monthly=200, amenities="Pool, Fitness Center, Tennis, Nature Preserve, Dog Park", completion_date="Summer 2025", description="Luxury custom home on premium hilltop lot with panoramic views.", parking=3),
        Property(id="p07", name="Pacific Crest 1BR Condo", project_name="Pacific Crest Residences", property_type="Condo", total_area_sqft=650, price_usd=649000, price_per_sqft=998, bedrooms=1, bathrooms=1, floor_number=8, total_floors=25, facing="West", status="available", location="Downtown Vancouver", address="1888 Pacific St, Unit 805", city="Vancouver", state="British Columbia", country="Canada", zip_code="V6G 2V1", mls_id="MLS-VAN-3301", year_built=2026, hoa_monthly=420, amenities="Rooftop Pool, Sky Lounge, Yoga Studio, Concierge, EV Charging", completion_date="Fall 2026", description="Sleek 1-bed with floor-to-ceiling windows and stunning ocean views.", parking=1),
        Property(id="p08", name="Pacific Crest 2BR Condo", project_name="Pacific Crest Residences", property_type="Condo", total_area_sqft=980, price_usd=949000, price_per_sqft=968, bedrooms=2, bathrooms=2, floor_number=15, total_floors=25, facing="North", status="available", location="Downtown Vancouver", address="1888 Pacific St, Unit 1501", city="Vancouver", state="British Columbia", country="Canada", zip_code="V6G 2V1", mls_id="MLS-VAN-3302", year_built=2026, hoa_monthly=520, amenities="Rooftop Pool, Sky Lounge, Co-working, Concierge, Bike Storage", completion_date="Fall 2026", description="Mountain-view 2-bed corner unit with den and in-suite laundry.", parking=1),
        Property(id="p09", name="Pacific Crest Penthouse", project_name="Pacific Crest Residences", property_type="Penthouse", total_area_sqft=2100, price_usd=2250000, price_per_sqft=1071, bedrooms=3, bathrooms=3, floor_number=25, total_floors=25, facing="West", status="available", location="Downtown Vancouver", address="1888 Pacific St, PH1", city="Vancouver", state="British Columbia", country="Canada", zip_code="V6G 2V1", mls_id="MLS-VAN-3303", year_built=2026, hoa_monthly=850, amenities="Private Terrace, Rooftop Pool, Sky Lounge, Concierge", completion_date="Fall 2026", description="Signature penthouse with wraparound terrace and 270° ocean/mountain views.", parking=2),
        Property(id="p10", name="Maple Ridge 3BR Semi", project_name="Maple Ridge Estates", property_type="Semi-Detached", total_area_sqft=2200, price_usd=729000, price_per_sqft=331, bedrooms=3, bathrooms=3, total_floors=2, facing="West", status="available", location="North Toronto", address="166 Maple Ridge Blvd", city="Toronto", state="Ontario", country="Canada", zip_code="M2K 1B2", mls_id="MLS-TR-4524", year_built=2025, lot_size_sqft=3200, hoa_monthly=300, amenities="Community Center, Walking Trails, Playground", completion_date="Spring 2026", description="Semi-detached with modern finishes, rooftop terrace, and attached garage.", parking=1),
    ]
    db.add_all(props); db.flush()

    BUYERS = [
        ("John Cooper", "(512) 555-1001", "john@example.com", "website", "Ranch", "$400K-$550K", "visit_booked", "agent1", "cust1"),
        ("Lisa Park", "(604) 555-1002", "lisa@example.com", "website", "2BR Condo", "$800K-$1M", "qualified", "mgr1", "cust2"),
        ("Mike Torres", "(416) 555-1003", "mike@example.com", "website", "Townhome", "$550K-$700K", "contacted", "agent2", "cust3"),
        ("David Chen", "(512) 555-2001", "david.c@email.com", "website", "Colonial", "$600K-$750K", "new", None, None),
        ("Rachel Kim", "(604) 555-2002", "rachel.k@email.com", "phone", "Penthouse", "$2M+", "escalated", "mgr1", None),
        ("Tom Wilson", "(416) 555-2003", "tom.w@email.com", "website", "Detached", "$850K-$1.1M", "contacted", "agent1", None),
        ("Sarah Lopez", "(512) 555-2004", "sarah.l@email.com", "website", "Ranch", "$425K-$500K", "visit_booked", "agent2", None),
        ("Brian Patel", "(604) 555-2005", "brian.p@email.com", "phone", "1BR Condo", "$600K-$750K", "qualified", "agent1", None),
        ("Jessica Brown", "(416) 555-2006", "jess.b@email.com", "website", "Executive Home", "$1.2M-$1.5M", "contacted", "mgr1", None),
        ("Kevin O'Brien", "(512) 555-2007", "kevin.o@email.com", "website", "Custom Build", "$800K-$1M", "new", None, None),
        ("Amanda White", "(604) 555-2008", "amanda.w@email.com", "website", "2BR Condo", "$900K-$1.1M", "visit_booked", "agent1", None),
        ("Chris Taylor", "(416) 555-2009", "chris.t@email.com", "phone", "Townhome", "$580K-$650K", "converted", "agent2", None),
        ("Nicole Adams", "(512) 555-2010", "nicole.a@email.com", "website", "Colonial", "$575K-$650K", "new", None, None),
        ("Robert Garcia", "(604) 555-2011", "robert.g@email.com", "website", "Penthouse", "$1.8M-$2.5M", "qualified", "mgr1", None),
        ("Emma Davis", "(416) 555-2012", "emma.d@email.com", "website", "Semi-Detached", "$700K-$800K", "contacted", "agent1", None),
    ]
    for i, (name, phone, email, src, interest, budget, status, agent, cid) in enumerate(BUYERS):
        db.add(Enquiry(id=f"enq-{i+1:03d}", customer_id=cid, buyer_name=name, buyer_phone=phone, buyer_email=email,
                       source=src, status=status, property_interest=interest, budget_range=budget, assigned_to=agent,
                       priority="urgent" if status=="escalated" else "high" if status in ("qualified","visit_booked") else "medium",
                       message_count=4 if status != "new" else 1, created_at=now - timedelta(days=15-i, hours=i*2)))
    db.flush()

    chats = [
        ("enq-001", "buyer", "Hi, looking for a 3-bed ranch in Austin area"), ("enq-001", "agent", "Welcome! Our Sunset Valley Ranch is perfect — 2,100 sqft, 3 bed/2 bath at $425K. Hill country views! Want to schedule a tour?"),
        ("enq-002", "buyer", "What 2BR condos do you have in Vancouver?"), ("enq-002", "agent", "Pacific Crest has a gorgeous 2BR on the 15th floor — 980 sqft at $949K. Mountain views, in-suite laundry. Corner unit!"),
        ("enq-005", "buyer", "Can you negotiate on the penthouse price?"), ("enq-005", "agent", "⚠ For pricing discussions, I'm connecting you with our Sales Director. You'll hear back within 15 minutes."),
        ("enq-006", "buyer", "Tell me about the 4-bed detached in Toronto"), ("enq-006", "agent", "Maple Ridge 4BR Detached — 2,800 sqft on a 5,500 sqft lot. Finished basement, double garage, backs onto walking trails. $899K!"),
    ]
    for eid, sender, content in chats:
        db.add(ChatMessage(id=str(uuid.uuid4()), enquiry_id=eid, sender=sender, content=content, message_type="escalation" if "⚠" in content else "text"))
    db.flush()

    visits_data = [
        ("enq-001", "cust1", "John Cooper", "(512) 555-1001", "p04", "Sunset Valley Ranch", 1, "scheduled", "agent1"),
        ("enq-002", None, "Lisa Park", "(604) 555-1002", "p08", "Pacific Crest 2BR", 2, "confirmed", "mgr1"),
        ("enq-007", None, "Sarah Lopez", "(512) 555-2004", "p05", "Sunset Valley Colonial", 1, "scheduled", "agent2"),
        ("enq-011", None, "Amanda White", "(604) 555-2008", "p08", "Pacific Crest 2BR", 3, "scheduled", "agent1"),
        ("enq-003", "cust3", "Mike Torres", "(416) 555-1003", "p01", "Maple Ridge Townhome", -2, "completed", "agent2"),
        ("enq-012", None, "Chris Taylor", "(416) 555-2009", "p01", "Maple Ridge Townhome", -5, "completed", "agent2"),
    ]
    slot = 60
    for eid, cid, name, phone, pid, pname, day_off, status, agent in visits_data:
        a = next(u for u in users if u.id == agent)
        dt = now + timedelta(days=day_off, hours=10)
        db.add(SiteVisit(id=str(uuid.uuid4()), enquiry_id=eid, customer_id=cid, buyer_name=name, buyer_phone=phone,
                         property_id=pid, property_name=pname, scheduled_date=dt, end_time=dt+timedelta(minutes=slot),
                         status=status, assigned_agent=agent, agent_name=a.full_name,
                         rating=4 if status == "completed" else None, feedback="Great property, very interested!" if status == "completed" else ""))
    db.flush()

    for title, body, cat in [
        ("New enquiry from Kevin O'Brien", "Custom Build, $800K–1M", "enquiry"),
        ("Tour booked: John Cooper", "Sunset Valley Ranch — tomorrow 10 AM", "visit"),
        ("⚠ Escalation: Rachel Kim", "Price negotiation on Penthouse", "escalation"),
        ("Chris Taylor converted!", "Maple Ridge Townhome sold", "info"),
        ("Tour confirmed: Lisa Park", "Pacific Crest 2BR — in 2 days", "visit"),
    ]:
        db.add(Notification(id=str(uuid.uuid4()), title=title, body=body, category=cat))

    for actor, action, etype, eid, details in [
        ("agent", "New enquiry via AI chat", "enquiry", "enq-013", "Nicole Adams — Colonial"),
        ("agent", "Tour auto-booked", "visit", "", "John Cooper — Sunset Valley Ranch"),
        ("agent", "Enquiry escalated", "enquiry", "enq-005", "Rachel Kim — price negotiation"),
        ("staff", "Tour completed", "visit", "", "Mike Torres — Maple Ridge Townhome"),
        ("staff", "Sale closed", "enquiry", "enq-012", "Chris Taylor — Maple Ridge Townhome"),
        ("system", "Agent uptime: 99.98%", "", "", "24/7 availability maintained"),
    ]:
        db.add(ActivityLog(id=str(uuid.uuid4()), actor=actor, action=action, entity_type=etype, entity_id=eid, details=details))

    db.commit(); db.close()
    print("Seeded: 7 users, 10 properties, 15 enquiries, 6 visits")

if __name__ == "__main__": seed()
