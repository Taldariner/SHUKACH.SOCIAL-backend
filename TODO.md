### SHUKACH.SOCIAL

List of a TODO tasks, sorted more or less in priority of implementation in order to make SHUKACH.SOCIAL a minimally valuable functionally.

- [x] Update database models, add first parsed news ID for channels (for reversed parsing) and pipelined status and post ID for news (for potential delayed pipelining).
- [x] Add and test a simple reversed parser for Telegram, in order to be able to parse olds news in the future.
- [x] Update links in navbar, make navigation on website seamless (without hand-editing URLs in browser address bar).
- [x] Make a robust search form for news filtering, as well as divide search results into multiple pages with a 50 news on each page (for example).
- [x] Make a proper export system that will take into account a current news search query, and not export full database (at least - current search form fields).
- [x] Optimize (parallelize) parsers (for Telegram, for start, for example) and test how many channels the system can parse seamlessly (at least, on my laptop). Can use popular Ukrainian channels for this.
- [x] Add text processing pipeline, try to connect it to parsers, optimize and test if they can work together properly. If no - think on how to implement a delayed pipelining in a best possible way. Maybe add a separate database table to store already collected keys and assings them to text in some more or less intelligent way.
- [x] Improve authorization system, make different types of users (clients, coders and client coders, for example) and add special possibilities to each type (to encode texts by hands by themselves, for example). 
- [ ] Add paid subscription mechanism for users to be able to use system, as well as personal cabinet for users to manage their stuff (I suppose?).
- [x] Update database and data models to a document-oriented system implementation, as it looks much more suitable for our needs, at least at first glance (but I am not 100% sure about that and I still need to look into it in more detail of course, I suppose).
- [ ] Try to write and add parsers for new social medias to the system - both text and video-oriented.
- [ ] Measure the bandwidth of the system, the loads it can handle, and the potential parsing rate. Try to optimize it as much as possible and re-measure it to determine the number of sources (channels)/posts per day that the system can handle, which we can present to our clients.
- [ ] Add possibility to parse additional posts information, like views or reactions, using something like repetitive parsing. And, probably, update database model for this again now, or 3 steps before.
- [ ] Find a good UI/UX designer/frontend programmer and update all website interfaces to more robust version. Also make all things across the website like resonant news information panes on main page work properly.
- [ ] Upload and deploy it on the server, test, fix all possible bugs and problems, measure performance and optimize, polish and make a really production-ready.
