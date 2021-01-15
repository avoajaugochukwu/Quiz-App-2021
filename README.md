# Quiz-App-2021
Link to the app: **[Quiz-App-2021](https://quiz-app-2021.herokuapp.com/)**

This is a quiz app, that has the following features:

1. Questions with 4 options each (the number of options can vary without impacting the stability of the app)
2. Instant feedback after submission
3. Result board that shows the result of everyone who has completed the test
4. All test results, the options the user selected alon with the right answer can be viewed at any time by clicking the result button

## How it works
The app does not require login for ease of use. It only requires a **unique** username. Users can also not come back to complete the test since login credentials are not collected.

### Database

Besides the default tables created by Django, four custom tables were created for the apps operations.

![quiz_app_db_model](https://user-images.githubusercontent.com/4976722/104733071-72c47a80-573e-11eb-8bec-54085938278f.PNG)

**TestDetail:** This table holds the test details like username, score and test times

**Question:** This table holds only the question text

**Option:** This table holds the text for options, and a boolean for the answer. All these are tied back to a question through the question id

**Response:** This table holds the users choice/option for each question along with the test_id which is unique to each user/test attempt. The answer filled in this table enables me to show the user the right anser for each question, when they are reviewing their test. See test result feedback image for more understanding.

## Screenshots of the app during use
![quiz_app_homepage](https://user-images.githubusercontent.com/4976722/104733119-866fe100-573e-11eb-96a7-133578bf9ea1.PNG)
*Home page*

![quiz_app_test_page](https://user-images.githubusercontent.com/4976722/104733249-b323f880-573e-11eb-8c5d-839f4b1c31b9.PNG)
*Test page*

![quiz_app_answer_all_questions](https://user-images.githubusercontent.com/4976722/104732916-34c75680-573e-11eb-8bcf-9db21b76c35a.PNG)
*Answer all questions alert when user tries to submit without answering all questions*

![quiz_app_test_result_feedback](https://user-images.githubusercontent.com/4976722/104733322-cdf66d00-573e-11eb-9021-14a6318bc51d.PNG)
*Feedback page, where users can see the answers as well as their choices*

![quiz_app_result_board](https://user-images.githubusercontent.com/4976722/104733183-9be50b00-573e-11eb-8d2c-3dd8420542a8.PNG)
*Result board, where all test scores are displayed, but not sorted by highest to lowest*