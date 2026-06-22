# NxtUp
- Building a personalized problem recommender for competitive programmers. 
- Shows Analytics and dashboard with more relevant statistics.
- Two tracks of questions to solve problems, Blind Order for building intuition and Topic Wise for custom practice.
— analyzes Codeforces problems using semantic meaning via vector embeddings and retrievals techniques for best possible results.
- Context compression for prompts to reduce "Lost in the Middle" phenomenon. Read More [Research Paper](https://cs.stanford.edu/~nfliu/papers/lost-in-the-middle.tacl2023.pdf)
- Recommends 9  Practice problems (3+6), detecting WA/TLE patterns, past unsolved problems and even previously solved hard problems for revision.
- Integrated live Codeforces API for submission tracking and rating updates.

## Tech Stack Used (Currently being used)
- Frontend : HTML, CSS, JavaScript
- Backend : Python (Django)
- Database : SQL
- AI : ChromaDB (Vector Embeddings & Vector DB) and RAGs
- APIs : Ollama 9B Instant (GroqCloud Hosted), GEMMA-4 31B IT (Nvidia Hosted), Codeforces API (platform hosted)
- Deployment : Yet to be made
- Task Scheduling : Yet to be made

## System Design Architecture of Recommendation Engine
<img width="1648" height="797" alt="flow" src="https://github.com/user-attachments/assets/054752f5-90d0-46aa-95dd-6246df24d071" />

## Need of this project ?
- Pasting past submission history into LLM each day is tiring.
- LLMs suck at huge context history, meaning chats won't be useful after few weeks
- Hallucinations !! LLMs are notorious for giving non-existent problems 

## Preview Photos
### 1. Profile Page with your Codeforces Information
- Synced to codeforces via API every 30 minutes
- Two heatmaps for progress tracking
<img width="1308" height="907" alt="image" src="https://github.com/user-attachments/assets/78a2eb33-1323-4d0a-b7ed-4bc0863f01e7" />

### 2. Blind Order Sheet
- Approx 300 Questions from A2OJ Ladders integrated right into the platform, with synced progress.
- Ability to filter questions effortlessly.
<img width="1289" height="775" alt="image" src="https://github.com/user-attachments/assets/cb0bfbcb-5789-4606-948b-15f929cc4247" />
<img width="1302" height="813" alt="image" src="https://github.com/user-attachments/assets/217a61d2-c03f-455a-bf34-ce06ab02b838" />

### 3. Recommendations
- Skill Map, showing user's proficiency in each tag
- 3 Recommended problems on weakest topic (for directly attacking weak spots)
- 6 Curated Problems for general practice
- Each problem also carries explanation to how it helps bridge the gap.
- List of Unsolved Problems and Spaced Repetition
<img width="1282" height="818" alt="image" src="https://github.com/user-attachments/assets/98ee6243-6c38-45f8-b7a8-bfb3a6afdcda" />
<img width="1305" height="833" alt="image" src="https://github.com/user-attachments/assets/b5df1ae7-0326-4eb8-8c21-bbfff791bc9d" />

## Code for Vector Embeddings
<img width="929" height="860" alt="image" src="https://github.com/user-attachments/assets/7470a10f-5a27-4198-bda1-ba774ccc0cf0" />


## Core Math Logic (For Context Compression)
- 5 Worded algorithmic summary of the core mathematical logic used to solve the problem, this strips away the story.
- EG : Binary Search on 2D Array, DP on trees
<img width="1533" height="857" alt="image" src="https://github.com/user-attachments/assets/38807eb5-e6ae-4146-bad7-8b7731561668" />

## Dataset from Hugging Face
- Contains approximately 10k problems ranging from all ratings across all tags. [Link to Dataset](https://huggingface.co/datasets/open-r1/codeforces)
<img width="1477" height="894" alt="image" src="https://github.com/user-attachments/assets/6493d4af-59f4-4b26-97e7-16a914bafc0b" />





