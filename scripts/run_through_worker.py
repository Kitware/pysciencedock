import celery
import json
import analytics_tasks.metabolomics as mb


celeryapp = celery.Celery(
    'girder_worker',
    backend='mongodb://localhost/metabolomics_worker',
    broker='mongodb://localhost/metabolomics_worker')

dockerSpec = mb.pretreat(_mode='json')
dockerSpec['pull_image'] = False
dockerResult = celeryapp.send_task('girder_worker.run', [dockerSpec], dict(
    inputs=dict(
        data=dict(data='a,b\n1,1\n1,2'),
        centering=dict(data=mb.CENTERING_MEAN)
    ),
    cleanup=False,
    validate=False,
    auto_convert=False
))
print json.dumps(dockerResult.get(), indent=2)
