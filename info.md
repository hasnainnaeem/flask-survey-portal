
Reviews:
Statement, type
type 1: positive
type 0: negative
type 2: anxious
type 3: angry

Questions:
statement, type, min, max
type 1: study1
type 2: sutdy 2
min: left linkart
max: right likart
9-scale likart
5th point: neutral

A user can attempt only study 1 or 2. Make sure to check if user data is already added to 'users' table.

STUDY1:
Load all 3 positive reviews.
Load 1 negative review, type 0.
Load 1 angry review, type 2,
Load 1 anxious review, type 3.

* Make sure to balance the review loads so that all reviews are shown to equal number of users.

Creating Form:
Positive reviews should always appear on places: 1, 3, and 5.

For each review, load Question of type 1.

Save response in table 'study_one'.


STUDY2:
Use the review:

"I feel so worried as I’m writing this!Ordered a laptop battery (12 cell) and RAM. I received a 6 cell battery and the incorrect RAM. I returned the products to this merchant three weeks ago (and they were received), but still have not received my refund. Let me tell you: I’m very irritated."

Creating Form:

Load all questions of type 2.
Then load all questions of type 1.

Save response in table 'study_Two'.

Better add an option for the user to view the review.