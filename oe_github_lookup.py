import os
import requests


os.system("cls" if os.name == "nt" else "clear")


BANNER = r"""
                                                       
  ▄▄▄▄▄                      ▄▄▄▄▄▄▄                   
▄███████▄                   ███▀▀▀▀▀                   
███   ███ ████▄ ▄█▀█▄ ████▄ ███▄▄    ██ ██ ▄█▀█▄ ▄█▀▀▀ 
███▄▄▄███ ██ ██ ██▄█▀ ██ ██ ███      ██▄██ ██▄█▀ ▀███▄ 
 ▀█████▀  ████▀ ▀█▄▄▄ ██ ██ ▀███████  ▀██▀ ▀█▄▄▄ ▄▄▄█▀ 
          ██                           ██              
          ▀▀                         ▀▀▀               

                         GITHUB LOOKUP
"""

print(BANNER)


username = input("GitHub Username > ").strip()


headers = {
    "Accept": "application/vnd.github+json"
}


try:

    user = requests.get(
        f"https://api.github.com/users/{username}",
        headers=headers,
        timeout=10
    )


    if user.status_code != 200:
        print("\n[-] User not found.")
        exit()


    data = user.json()


    repos_req = requests.get(
        f"https://api.github.com/users/{username}/repos?per_page=10",
        headers=headers,
        timeout=10
    )

    repos = repos_req.json()


    title = f"GITHUB LOOKUP — {data['login']}"


    email = data.get("email")

    if not email:
        email = "Not public"


    lines = [

        f"USERNAME        : {data['login']}",
        f"USER ID         : {data['id']}",
        f"NAME            : {data['name'] or 'N/A'}",
        f"EMAIL           : {email}",
        f"BIO             : {data['bio'] or 'N/A'}",
        f"LOCATION        : {data['location'] or 'N/A'}",
        f"COMPANY         : {data['company'] or 'N/A'}",
        f"FOLLOWERS       : {data['followers']}",
        f"FOLLOWING       : {data['following']}",
        f"PUBLIC REPOS    : {data['public_repos']}",
        f"PROFILE         : {data['html_url']}"

    ]


    repo_lines = []


    for repo in repos:

        repo_name = repo["name"]
        owner = repo["owner"]["login"]


        repo_lines.append(
            f"REPO : {repo_name}"
        )

        repo_lines.append(
            f"URL  : {repo['html_url']}"
        )


        commits = requests.get(
            f"https://api.github.com/repos/{owner}/{repo_name}/commits?per_page=3",
            headers=headers,
            timeout=10
        ).json()



        if isinstance(commits, list):

            for commit in commits:

                commit_data = commit.get(
                    "commit",
                    {}
                )

                author = commit_data.get(
                    "author"
                ) or {}


                repo_lines.append(
                    f"SHA     : {commit['sha'][:8]}"
                )

                repo_lines.append(
                    f"AUTHOR  : {author.get('name','N/A')}"
                )

                repo_lines.append(
                    f"EMAIL   : {author.get('email','N/A')}"
                )

                repo_lines.append(
                    f"DATE    : {author.get('date','N/A')}"
                )


                message = commit_data.get(
                    "message",
                    "N/A"
                ).replace("\n", " ")


                repo_lines.append(
                    f"MESSAGE : {message[:60]}"
                )

                repo_lines.append("")


        repo_lines.append("-" * 30)



    section = "REPOSITORIES + COMMITS"


    longest = max(
        len(title),
        len(section),
        *(len(x) for x in lines),
        *(len(x) for x in repo_lines)
    )


    padding = 2
    width = longest + padding * 2



    def box(line=""):

        return (
            "│"
            + " " * padding
            + line.ljust(longest)
            + " " * padding
            + "│"
        )


    print()

    print("┌" + "─" * width + "┐")

    print(
        box(
            title.center(longest)
        )
    )

    print("├" + "─" * width + "┤")


    for line in lines:
        print(box(line))


    print("├" + "─" * width + "┤")


    print(
        box(
            section.center(longest)
        )
    )


    for line in repo_lines:
        print(box(line))


    print("└" + "─" * width + "┘")



except requests.exceptions.RequestException as e:

    print(
        f"\n[-] Network Error: {e}"
    )


except Exception as e:

    print(
        f"\n[-] Error: {e}"
    )


input("\nPress ENTER to exit...")