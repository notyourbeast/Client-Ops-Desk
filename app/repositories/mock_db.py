from datetime import datetime
from bson import ObjectId
from typing import Dict, List, Any, Optional


class MockCollection:
    def __init__(self, name: str):
        self.name = name
        self._data: List[Dict] = []

    def find_one(self, filter: Dict) -> Optional[Dict]:
        for doc in self._data:
            match = True
            for key, value in filter.items():
                doc_value = doc.get(key)
                if isinstance(value, ObjectId) or isinstance(doc_value, ObjectId):
                    if str(doc_value) != str(value):
                        match = False
                        break
                elif doc_value != value:
                    match = False
                    break
            if match:
                return doc.copy()
        return None

    def find(self, filter: Optional[Dict] = None, sort=None):
        results = self._data.copy()
        
        if filter:
            filtered = []
            for doc in results:
                match = True
                for key, value in filter.items():
                    doc_value = doc.get(key)
                    if isinstance(value, dict):
                        if '$ne' in value:
                            if isinstance(value['$ne'], ObjectId) or isinstance(doc_value, ObjectId):
                                if str(doc_value) == str(value['$ne']):
                                    match = False
                            elif doc_value == value['$ne']:
                                match = False
                        elif '$gte' in value:
                            if doc_value < value['$gte']:
                                match = False
                        elif '$lte' in value:
                            if doc_value > value['$lte']:
                                match = False
                    elif isinstance(value, ObjectId) or isinstance(doc_value, ObjectId):
                        if str(doc_value) != str(value):
                            match = False
                            break
                    elif doc_value != value:
                        match = False
                        break
                if match:
                    filtered.append(doc)
            results = filtered

        if sort:
            field, direction = list(sort.items())[0]
            reverse = direction == -1
            results.sort(key=lambda x: x.get(field, ''), reverse=reverse)

        return MockCursor(results)

    def insert_one(self, document: Dict) -> 'MockInsertResult':
        if '_id' not in document:
            document['_id'] = ObjectId()
        self._data.append(document.copy())
        return MockInsertResult(document['_id'])

    def update_one(self, filter: Dict, update: Dict) -> 'MockUpdateResult':
        doc = None
        doc_index = -1
        for i, d in enumerate(self._data):
            match = True
            for key, value in filter.items():
                doc_value = d.get(key)
                if isinstance(value, ObjectId) or isinstance(doc_value, ObjectId):
                    if str(doc_value) != str(value):
                        match = False
                        break
                elif doc_value != value:
                    match = False
                    break
            if match:
                doc = d
                doc_index = i
                break
        
        if doc:
            if '$set' in update:
                for key, value in update['$set'].items():
                    doc[key] = value
                self._data[doc_index] = doc
            matched = 1
            modified = 1
        else:
            matched = 0
            modified = 0
        return MockUpdateResult(matched, modified)

    def delete_one(self, filter: Dict) -> 'MockDeleteResult':
        for i, doc in enumerate(self._data):
            match = True
            for key, value in filter.items():
                doc_value = doc.get(key)
                if isinstance(value, ObjectId) or isinstance(doc_value, ObjectId):
                    if str(doc_value) != str(value):
                        match = False
                        break
                elif doc_value != value:
                    match = False
                    break
            if match:
                self._data.pop(i)
                return MockDeleteResult(1)
        return MockDeleteResult(0)


class MockCursor:
    def __init__(self, data: List[Dict]):
        self._data = data

    def sort(self, *args, **kwargs):
        return self

    def __iter__(self):
        return iter(self._data)

    def __list__(self):
        return self._data


class MockInsertResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id


class MockUpdateResult:
    def __init__(self, matched_count, modified_count):
        self.matched_count = matched_count
        self.modified_count = modified_count


class MockDeleteResult:
    def __init__(self, deleted_count):
        self.deleted_count = deleted_count


class MockDatabase:
    def __init__(self):
        self._collections: Dict[str, MockCollection] = {}

    def __getitem__(self, name: str) -> MockCollection:
        if name not in self._collections:
            self._collections[name] = MockCollection(name)
        return self._collections[name]

    def __getattr__(self, name: str) -> MockCollection:
        return self[name]


_mock_db = None


def get_mock_db():
    global _mock_db
    if _mock_db is None:
        _mock_db = MockDatabase()
        _init_demo_data(_mock_db)
    return _mock_db


def _init_demo_data(db: MockDatabase):
    from bson import ObjectId
    from werkzeug.security import generate_password_hash
    
    demo_user_id = ObjectId()
    
    users = db.users
    users.insert_one({
        '_id': demo_user_id,
        'email': 'demo@example.com',
        'password_hash': generate_password_hash('demo'),
        'name': 'Demo User',
        'created_at': datetime.utcnow()
    })

    clients = db.clients
    client_id = ObjectId()
    clients.insert_one({
        '_id': client_id,
        'user_id': demo_user_id,
        'name': 'Acme Corp',
        'email': 'contact@acme.com',
        'phone': '+1-555-0100',
        'company': 'Acme Corporation',
        'notes': 'Main client',
        'created_at': datetime.utcnow()
    })

    projects = db.projects
    project_id = ObjectId()
    projects.insert_one({
        '_id': project_id,
        'user_id': demo_user_id,
        'client_id': client_id,
        'title': 'Website Redesign',
        'description': 'Complete website overhaul',
        'status': 'in-progress',
        'hourly_rate': 75.0,
        'deadline': None,
        'created_at': datetime.utcnow()
    })

    time_logs = db.time_logs
    time_logs.insert_one({
        '_id': ObjectId(),
        'user_id': demo_user_id,
        'project_id': project_id,
        'start_time': datetime.utcnow(),
        'end_time': datetime.utcnow(),
        'duration_minutes': 120
    })

    invoices = db.invoices
    invoices.insert_one({
        '_id': ObjectId(),
        'user_id': demo_user_id,
        'project_id': project_id,
        'total_hours': 2.0,
        'amount_due': 150.0,
        'status': 'unpaid',
        'due_date': None,
        'created_at': datetime.utcnow()
    })

