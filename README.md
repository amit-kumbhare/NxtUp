# NxtUp
- Building a personalized problem recommender for competitive programmers 
- Shows Analytics and dashboard with more relevant statistics.
- Two tracks of questions to solve problems, Blind Order for building intuition and Topic Wise for custom practice.
— analyzes Codeforces problems using tag-based difficulty modeling to match problems to a user's current skill gap.
- "Bridge Curriculum" -> detects WA/TLE patterns and auto-generates a targeted 3-problem sequence to close knowledge gaps; 
- Recommends 6 Additional Practice problems, past unsolved problems and even previously solved hard problems for revision.
- Integrated live Codeforces API for submission tracking and rating updates.

## Tech Stack Used (Currently being used)
- Frontend : HTML, CSS, JavaScript
- Backend : Python (Django)
- Database : SQL
- AI : ChromaDB (Vector Embeddings & Vector DB) and RAGs
- APIs : Ollama 9B Instant (GroqCloud Hosted), GEMMA-4 31B IT (Nvidia Hosted), Codeforces API (platform hosted)
- Deployment : Yet to be made
- Task Scheduling : Yet to be made


## Preview Photos
### 1. Profile Page with your Codeforces Information
- Synced to codeforces via API every 30 minutes
- Two heatmaps for progress tracking
<img width="1308" height="907" alt="image" src="https://github.com/user-attachments/assets/78a2eb33-1323-4d0a-b7ed-4bc0863f01e7" />

### 2. Single login solution to access your progress
<img width="1304" height="884" alt="image" src="https://github.com/user-attachments/assets/3639daf4-52ec-47a2-b62f-569c652f06f6" />

### 3. Blind Order Sheet
- Approx 300 Questions from A2OJ Ladders integrated right into the platform, with synced progress.
<img width="1289" height="775" alt="image" src="https://github.com/user-attachments/assets/cb0bfbcb-5789-4606-948b-15f929cc4247" />

### 4. Topic Wise Sheet (synced with blind order)
- Ability to filter questions effortlessly.
<img width="1302" height="813" alt="image" src="https://github.com/user-attachments/assets/217a61d2-c03f-455a-bf34-ce06ab02b838" />

### 3. Recommendations
- Skill Map, showing user's proficiency in each tag
- 3 Recommended problems on weakest topic (for directly attacking weak spots)
- 6 Curated Problems for general practice
- List of Unsolved Problems and Spaced Repetition
<img width="1282" height="818" alt="image" src="https://github.com/user-attachments/assets/98ee6243-6c38-45f8-b7a8-bfb3a6afdcda" />
<img width="1305" height="833" alt="image" src="https://github.com/user-attachments/assets/b5df1ae7-0326-4eb8-8c21-bbfff791bc9d" />


