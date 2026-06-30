# NxtUp
- Building a personalized problem recommender for competitive programmers. 
- Shows Analytics and dashboard with more relevant statistics.
- Two tracks of questions to solve problems, Blind Order for building intuition and Topic Wise for custom practice.
— analyzes Codeforces problems using semantic meaning via vector embeddings and retrievals techniques for best possible results.
- Context compression for prompts to reduce "Lost in the Middle" phenomenon. Read More [Research Paper](https://cs.stanford.edu/~nfliu/papers/lost-in-the-middle.tacl2023.pdf)
- Recommends 9  Practice problems (3+6), detecting WA/TLE patterns, past unsolved problems and even previously solved hard problems for revision.
- Integrated live Codeforces API for submission tracking and rating updates.
- Link to Video Documentation Playlist on YT [Link](https://youtube.com/playlist?list=PLkHIX4YjBbcfoa-Umc7mYKgEAq1Hi5OQx&si=fGXJGU6xvON_AnK8)

## Tech Stack Used (Currently being used)
- Frontend : HTML, CSS, JavaScript
- Backend : Python (Django)
- Database : SQL
- AI : ChromaDB (Vector Embeddings & Vector DB) and RAGs
- APIs : Ollama 9B Instant (GroqCloud Hosted), GEMMA-4 31B (Nvidia Hosted), Codeforces API (platform hosted)
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
<img width="1204" height="894" alt="image" src="https://github.com/user-attachments/assets/3ffa018d-3b54-43dc-8c35-9b5f923c9741" />
<img width="1204" height="557" alt="image" src="https://github.com/user-attachments/assets/5c69e7e4-f14a-4b7e-8ab7-a100287b32e3" />

### 2. Blind Order Sheet
- Approx 300 Questions from A2OJ Ladders integrated right into the platform, with synced progress.
- Ability to filter questions effortlessly.

<img width="1204" height="795" alt="image" src="https://github.com/user-attachments/assets/9569dd39-b10b-48c5-bcd8-4caa61ea6f3c" />
<img width="1206" height="869" alt="image" src="https://github.com/user-attachments/assets/36ad3f81-9eb7-4238-a55f-c9d21b769b05" />

### 3. Recommendations
- Skill Map, showing user's proficiency in each tag
- 3 Recommended problems on weakest topic (for directly attacking weak spots)
- 6 Curated Problems for general practice
- Each problem also carries explanation to how it helps bridge the gap.
- List of Unsolved Problems and Spaced Repetition
<img width="1206" height="853" alt="image" src="https://github.com/user-attachments/assets/7c6d2c0d-1472-45c0-b289-5f0c1ba013dd" />
<img width="1208" height="878" alt="image" src="https://github.com/user-attachments/assets/51d44482-d0cf-4400-b6c8-998091104e69" />

## Code for Vector Embeddings
<img width="929" height="860" alt="image" src="https://github.com/user-attachments/assets/7470a10f-5a27-4198-bda1-ba774ccc0cf0" />


## Core Math Logic (For Context Compression)
- 5 Worded algorithmic summary of the core mathematical logic used to solve the problem, this strips away the story.
- EG : Binary Search on 2D Array, DP on trees
<img width="1533" height="857" alt="image" src="https://github.com/user-attachments/assets/38807eb5-e6ae-4146-bad7-8b7731561668" />

## Dataset from Hugging Face
- Contains approximately 10k problems ranging from all ratings across all tags. [Link to Dataset](https://huggingface.co/datasets/open-r1/codeforces)
<img width="1477" height="894" alt="image" src="https://github.com/user-attachments/assets/6493d4af-59f4-4b26-97e7-16a914bafc0b" />

### Work In Progress — Local Execution Only

**This project is not expected to work on other devices yet.** 
 To keep the repository lightweight, several **large databases** and **essential configuration files** have been omitted from this remote repository. The project currently relies on hardcoded local assets and environment structures.

Watch Demo/Documentation [Link](https://youtube.com/playlist?list=PLkHIX4YjBbcfoa-Umc7mYKgEAq1Hi5OQx&si=fGXJGU6xvON_AnK8)

