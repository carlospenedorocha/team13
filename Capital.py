import datetime
from google.cloud import datastore
import utility

# datastore_client = datastore.Client()

# kind = 'capitals'
# name = '11111'
# task_key = datastore_client.key(kind, name)
# task = datastore.Entity(key=task_key)
# task['country'] = str('Buy Milk')
# datastore_client.put(task)


def create_client(project_id):
    print "project id is <%s>" % project_id
    pid = datastore.Client(project_id)

    print "pid is <%s>" % pid
    return pid

def add_task(client, description):
    key = client.key('Task')

    task = datastore.Entity(
        key, exclude_from_indexes=['description'])

    task.update({
        'created': datetime.datetime.utcnow(),
        'description': str(description),
        'done': False
    })

    client.put(task)

    return task.key

def mark_done(client, task_id):
    with client.transaction():
        key = client.key('Task', task_id)
        task = client.get(key)

        if not task:
            raise ValueError(
                'Task {} does not exist.'.format(task_id))

        task['done'] = True

        client.put(task)

def find_task(client):
    query = client.query(kind='Task')
    query.add_filter('done', '=', False)
    for task in query.fetch():
        print "task is <%s>" % task

def delete_task(client, task_id):
    key = client.key('Task', task_id)
    client.delete(key)

client = create_client(utility.project_id())
#task = add_task(client, "Buy Milk")
#print "task is <%s>" % task
#mark_done(client, task.id)
find_task(client)
