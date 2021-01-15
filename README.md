# Quiz-App-2021
Link to the app: **[Quiz-App-2021](https://quiz-app-2021.herokuapp.com/)**

This is a quiz app, that has the following features:

1. Questions with 4 options each (the number of options can vary without impacting the stability of the app)
2. Instant feedback after submission
3. Result board that shows the result of everyone who has completed the test

## How it works
The app does not require login for ease of use. It only requires a **unique** username. Users can also not come back to complete the test since login credentials are not collected.

### Database

Besides the default tables created by Django, four custom tables were created for the apps operations.

![ScreenShot](/quiz/static/quiz/img/markdown_screenshots/quiz_app_db_model.png)

**TestDetail:** This table holds the test details like username, score and test times

**Question:** This table holds only the question text

**Option:** This table holds the text for options, and a boolean for the answer. All these are tied back to a question through the question id

**Response:** This table holds the users choice/option for each question along with the test_id which is unique to each user/test attempt. The answer filled in this table enables me to show the user the right anser for each question, when they are reviewing their test. See test result feedback image for more understanding.

## Screenshots of the app during use
![ScreenShot](/quiz/static/quiz/img/markdown_screenshots/quiz_app_homepage.png)
*Home page*

![ScreenShot](/quiz/static/quiz/img/markdown_screenshots/quiz_app_test_page.png)
*Test page*

![ScreenShot](/quiz/static/quiz/img/markdown_screenshots/quiz_app_answer_all_questions.png)
*Answer all questions alert when user tries to submit without answering all questions*

![ScreenShot](/quiz/static/quiz/img/markdown_screenshots/quiz_app_test_result_feedback.png)
*Feedback page, where users can see the answers as well as their choices*

![ScreenShot](/quiz/static/quiz/img/markdown_screenshots/quiz_app_result_board.png)
*Result board, where all test scores are displayed, but not sorted by highest to lowest*