from app.repositories.client_repository import (
    create_client,
    get_clients_for_user,
    get_client_by_id,
    update_client,
    delete_client
)


def create_client_for_user(user_id, data):
    return create_client(user_id, data)


def get_user_clients(user_id):
    return get_clients_for_user(user_id)


def get_user_client(user_id, client_id):
    client = get_client_by_id(user_id, client_id)
    if not client:
        return None, 'Client not found'
    return client, None


def update_user_client(user_id, client_id, data):
    client = update_client(user_id, client_id, data)
    if not client:
        return None, 'Client not found'
    return client, None


def remove_user_client(user_id, client_id):
    deleted = delete_client(user_id, client_id)
    if not deleted:
        return False, 'Client not found'
    return True, None

