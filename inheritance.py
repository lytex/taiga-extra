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

logging.info('Getting tasks ...')
tasks = api.tasks.list(project=project.id)
task_dict = {x.id: x.name for x in project.list_task_statuses()}


status = [x.name for x in project.list_task_statuses()]
status2 = [x.name for x in project.list_user_story_statuses()]
assert status == status2, "Task statuses and user statuses must be the same"

total = len(user_stories)

for story in user_stories:
    childs = [x for x in tasks if x.user_story == story.id]
    # Assume statuses are ordered from "less" done to "more" done
    index = len(status)-1 if childs else status.index(user_story_dict[story.status])
    for task in childs:
        if task.user_story == story.id:
            next_index = status.index(task_dict[task.status])
            if next_index < index:
                index = next_index
        
        for story_tag in story.tags:
            if not task.tags.count(story_tag):
                logging.debug(f'{task.subject} is inheriting tag {story_tag} from\n\t{story.subject}')
                task.tags.append(story_tag)
                send(task.update)
                
    new_status = user_story_dict_inv[status[index]]
    if story.status != new_status:
        logging.debug(f'{story.subject} is updating from status {user_story_dict[story.status]} to {status[index]} ')
        story.status = new_status
        send(story.update)


    