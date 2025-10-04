# Sprint 1 Report
Video Link: https://www.youtube.com/watch?v=HfMPRY2lThI 

## What's New (User Facing)
* Basic user registration (username & password, password hashed with SHA-256)
* Login page and authentication with stored hashed passwords
* Profile setup page where users can add and save roommate preferences
* Simple list of roommate match profiles displayed after login
* Website Navigation
* Login and register forms

## Work Summary (Developer Facing)

This sprint was focused on creating the foundation for the RoomSync project. We set up the GitHub repository in accordance with the class guidance, created and maintained a Kanban board to keep track of our work and progress, and implemented the foundational features for our project. The backend team constructed the database schema, utilized secure password hashing with SHA-256, and created routes for registration, login, and profile setup using Python Flask. Many of these features were demonstrated eith...

## Unfinished Work

Our main focus for Sprint 1 was to develop a solid plan and demonstrate basic functionality of our features, and we accomplished that goal. All features have basic functionality, and are set to be improved during Sprint 2. 

## Completed Issues/User Stories

Here are links to the issues that we completed in this sprint:
* https://github.com/annaleenersten/RoomSync/issues/8
* https://github.com/annaleenersten/RoomSync/issues/21
* https://github.com/annaleenersten/RoomSync/issues/9
* https://github.com/annaleenersten/RoomSync/issues/6
* https://github.com/annaleenersten/RoomSync/issues/19


## Code Files for Review
Please review the following code files, which were actively developed during this sprint, for quality:
* [base.html](https://github.com/annaleenersten/RoomSync/blob/main/code/frontend/templates/base.html)
* [login.html](https://github.com/annaleenersten/RoomSync/blob/main/code/frontend/templates/login.html)
* [matches.html](https://github.com/annaleenersten/RoomSync/blob/main/code/frontend/templates/matches.html)
* [register.html](https://github.com/annaleenersten/RoomSync/blob/main/code/frontend/templates/register.html)
* [profile.html](https://github.com/annaleenersten/RoomSync/blob/main/code/frontend/templates/profile.html)
* [app.py](https://github.com/annaleenersten/RoomSync/blob/main/code/backend/app.py)
* [auth_utils.py](https://github.com/annaleenersten/RoomSync/blob/main/code/backend/auth_utils.py)
* [database.py](https://github.com/annaleenersten/RoomSync/blob/main/code/backend/database.py)

## Retrospective Summary
Here's what went well:
* The team made enough progress to have a clear idea of the scope of the project and the features we want to add by the end of the semester.   
* We clarified roles and responsibilities of each team member 
* We created the initial project structure (repo, kanban, skeleton code) before starting any real features
* We established weekly meetings to plan and discuss progress/issues

Here's what we'd like to improve:
* We will work on integrating the frontend and backend code 
* More small and descriptive commits to keep track of changes 

Here are changes we plan to implement in the next sprint:
* For the next sprint we will assign issues to pull requests and include user stories for every issue added to the kanban 
* We will start writing clearer acceptance criteria for tasks so it’s easier to know when an issue is “done.”
