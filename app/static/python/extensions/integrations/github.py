from github import Github, ApplicationOAuth

# First course a Github instance:


g = Github("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")

# Then play with your Github objects:
for repo in g.get_user().get_repos():
    print(repo.name)

g = ApplicationOAuth.ApplicationOAuth()
g.get_access_token()
