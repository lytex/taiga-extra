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

current_sprint = list(filter(lambda x: not x.closed, project.milestones))[0]

current_user_stories = list(filter(lambda x: x.milestone == current_sprint.id, user_stories))

tag = 'current_sprint'

for story in current_user_stories:
    story_with_tag = list(filter(lambda x: x[0] == tag, story.tags))
    if not story_with_tag:
        story.tags.append([tag, None])
        story.update()    


old_user_stories = list(filter(lambda x: x.milestone != current_sprint.id, user_stories))

for story in old_user_stories:
    story_with_tag = list(filter(lambda x: x[0] == tag, story.tags))
    if story_with_tag:
        story.milestone = current_sprint.id
        story.update()
