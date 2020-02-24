from taiga import TaigaAPI
import config as c

api = TaigaAPI()

api.auth(
    username=c.TAIGA_USER,
    password=c.TAIGA_PASSWORD
)

print('Initializing connection and authenticating ...', flush=True)
project = api.projects.get_by_slug(c.PROJECT_SLUG)

print('Getting user stories ...', flush=True)
user_stories = api.user_stories.list(project=project.id)
user_story_dict_inv = {x.name: x.id for x in project.list_user_story_statuses()}

print('Getting tasks ...', flush=True)
tasks = api.tasks.list(project=project.id)
task_dict = {x.id: x.name for x in project.list_task_statuses()}


status = [x.name for x in project.list_task_statuses()]
status2 = [x.name for x in project.list_user_story_statuses()]
assert status == status2, "Task statuses and user statuses must be the same"

for story in user_stories:
    # Assume statuses are ordered from "less" done to "more" done
    index = len(status)-1
    for task in tasks:
        if task.user_story == story.id:
            next_index = status.index(task_dict[task.status])
            if next_index < index:
                index = next_index
        
        for story_tag in story.tags:
            if not task.tags.count(story_tag):
                task.tags.append(story_tag)
                task.update()


                
    story.status = user_story_dict_inv[status[index]]
    story.update()


    