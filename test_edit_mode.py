from app import create_app
app = create_app()
with app.test_client() as client:
    resp = client.get('/inventory/edit/1?user=TestUser')
    print('Edit page status:', resp.status_code)
    content = resp.data.decode('utf-8')
    if 'Edit Item' in content and 'Cancel Edit' in content:
        print('Edit mode UI correct!')
    else:
        print('Edit mode issue')
    if 'toggleAddForm' not in content or 'display: none' in content:
        print('Toggle button hidden in edit mode!')
    else:
        print('Toggle button visibility issue')