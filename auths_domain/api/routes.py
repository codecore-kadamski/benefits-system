from injector import inject
from .views import UserProvider, AuthProvider


@inject(data_provider=UserProvider)
def search(data_provider, data) -> str:
    return data_provider.search_user(data)


@inject(data_provider=UserProvider)
def create(data_provider, data) -> str:
    return data_provider.create_user(data)


@inject(data_provider=UserProvider)
def read(data_provider, user_id) -> str:
    return data_provider.read_user(user_id)


@inject(data_provider=UserProvider)
def update(data_provider, data) -> str:
    return data_provider.update_user(data)


@inject(data_provider=UserProvider)
def delete(data_provider, user_id) -> str:
    return data_provider.delete_product(user_id)


@inject(data_provider=AuthProvider)
def register(data_provider, data) -> str:
    return data_provider.register(data)


@inject(data_provider=AuthProvider)
def login(data_provider, data) -> str:
    return data_provider.login(data)

@inject(data_provider=AuthProvider)
def verify(data_provider) -> str:
    return data_provider.verify()
