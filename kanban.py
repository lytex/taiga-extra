from taiga import TaigaAPI
import config as c
import logging
from send import send

logging.basicConfig(level=logging.DEBUG)

api = TaigaAPI()

api.auth(
    username=c.TAIGA_USER,
    password=c.TAIGA_PASSWORD
)

logger.info('Initializing connection and authenticating ...')
project = api.projects.get_by_slug(c.PROJECT_SLUG)

logger.info('Getting user stories ...')
user_stories = api.user_stories.list(project=project.id)

current_sprint = list(filter(lambda x: not x.closed, project.milestones))[0]

current_user_stories = list(filter(lambda x: x.milestone == current_sprint.id, user_stories))

tag = 'current_sprint'

for story in current_user_stories:
    story_with_tag = list(filter(lambda x: x[0] == tag, story.tags))
    if not story_with_tag:
        logging.debug(f'{story.subject}: adding tag {tag}')
        story.tags.append([tag, None])
        send(story.update)


old_user_stories = list(filter(lambda x: x.milestone != current_sprint.id, user_stories))

for story in old_user_stories:
    story_with_tag = list(filter(lambda x: x[0] == tag, story.tags))
    if story_with_tag:
        logging.debug(f'{story.subject}: adding to current sprint {current_sprint.name}')
        story.milestone = current_sprint.id
        send(story.update)
