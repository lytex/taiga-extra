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

logging.info('Initializing connection and authenticating ...')
project = api.projects.get_by_slug(c.PROJECT_SLUG)

logging.info('Getting user stories ...')
user_stories = api.user_stories.list(project=project.id)
user_story_dict = {x.id: x.name for x in project.list_user_story_statuses()}
user_story_dict_inv = {x.name: x.id for x in project.list_user_story_statuses()}

current_sprints = list(filter(lambda x: not x.closed, project.milestones))
current_sprints = sorted(current_sprints, key=lambda x: x.id)

assert len(current_sprints) >= 2, "There must be at least 2 active sprints to migrate to a new sprint"
new_sprint = current_sprints[-1]
old_sprint = current_sprints[-2]


old_user_stories = list(filter(lambda x: x.milestone == old_sprint.id, user_stories))

for story in old_user_stories:
    if user_story_dict[story.status] != c.DONE_SLUG:
        logging.debug(f'{story.subject}: adding to new sprint {new_sprint.name}')
        story.milestone = new_sprint.id
        send(story.update)