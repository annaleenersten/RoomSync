# Sprint 2 Report
Video Link: https://www.youtube.com/watch?v=9uLT8_k5SOc 

## What's New (User Facing)
- Users can now edit and update their profile preferences (budget, location, lifestyle) directly through the interface.  
- Persistent data storage now ensures profile updates are saved between sessions.  
- The matching algorithm has been implemented and ranks potential roommates by compatibility.  
- The website now features fully functional navigation between login, profile, and matches pages.  
- The frontend layout has been improved with improved styling for better usability and consistency.  
- Dynamic rendering ensures that data from the backend database is properly displayed on all pages.  

## Work Summary (Developer Facing)
Sprint 2 focused on expanding core functionality and connecting the backend to the frontend to produce a usable prototype.  
The backend team enhanced the SQLite schema and developed queries to support persistent profile data, user matching, and profile editing.  
The matching algorithm was completed and integrated with Flask routes to display compatibility scores on the matches page.  
The frontend team refactored HTML templates to route dynamically through Flask instead of static `.html` links, improving site navigation.  
Both teams collaborated to ensure data consistency and proper rendering of user information, resulting in a complete user flow from registration to viewing matches.  

## Unfinished Work
Some UI elements, such as displaying contact information, still need to be integrated.  
Deployment setup is also scheduled for the next sprint using Railroad for temporary hosting and testing.  


## Completed Issues/User Stories

Here are links to the issues that we completed in this sprint:
* https://github.com/annaleenersten/RoomSync/issues/6
* https://github.com/annaleenersten/RoomSync/issues/8
* https://github.com/annaleenersten/RoomSync/issues/9
* https://github.com/annaleenersten/RoomSync/issues/10
* https://github.com/annaleenersten/RoomSync/issues/19
* https://github.com/annaleenersten/RoomSync/issues/21
* https://github.com/annaleenersten/RoomSync/issues/23
* https://github.com/annaleenersten/RoomSync/issues/24
* https://github.com/annaleenersten/RoomSync/issues/26
* https://github.com/annaleenersten/RoomSync/issues/30

## Code Files for Review
Please review the following code files, which were actively developed during this sprint, for quality:
* [base.html](https://github.com/annaleenersten/RoomSync/blob/main/code/frontend/templates/base.html)
* [login.html](https://github.com/annaleenersten/RoomSync/blob/main/code/frontend/templates/login.html)
* [matches.html](https://github.com/annaleenersten/RoomSync/blob/main/code/frontend/templates/matches.html)
* [register.html](https://github.com/annaleenersten/RoomSync/blob/main/code/frontend/templates/register.html)
* [profile.html](https://github.com/annaleenersten/RoomSync/blob/main/code/frontend/templates/profile.html)
* [app.py](https://github.com/annaleenersten/RoomSync/blob/main/code/backend/app.py)
* [database.py](https://github.com/annaleenersten/RoomSync/blob/main/code/backend/database.py)
* [matching.py](https://github.com/annaleenersten/RoomSync/blob/main/code/backend/mathching.py)

## Retrospective Summary
Here's what went well
* The team successfully implemented key backend and database features, resulting in a functional prototype with persistent data and a working matching system.  
* Collaboration improved across all roles — backend, frontend, and design — with consistent communication during development and debugging.   
* Regular meetings helped track progress, identify blockers, and ensure feature alignment with our user stories.  

Here's what we'd like to improve
* Improve coordination between the Flask backend and the HTML frontend templates to ensure consistent user flow and data rendering.   
* Dedicate more time to automated testing and validation to ensure new changes don’t break existing functionality.  

Here are changes we plan to implement in the next sprint
* Begin integrating the Flask backend with the finalized frontend templates to create a unified experience.  
* Expand user profile features to include profile editing and better match filtering logic.  
* Define measurable acceptance criteria for all new features and link each Kanban issue to its corresponding pull request.  
* Start preparing for deployment setup (local Docker testing or cloud deployment) to support the project’s final presentation.  