from django_rq import job

@job
def new_event_worker(params):
    print('hello')