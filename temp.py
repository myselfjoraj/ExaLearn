"""
ref = db.reference('/')

# Prepare your data as a dictionary
data = {
  'name': 'John Doe',
  'age': 30,
  'city': 'New York'
}

# Push data to a specific path
ref.push(data)  # Pushes data and generates a unique key

# Or set data to a specific path (overwrites existing data)
ref.child('users').child('uid').set(data)  # Replace 'uid' with a specific user ID

print('Data inserted successfully!')
"""

